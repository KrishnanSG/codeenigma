import shutil
import subprocess
from pathlib import Path
from typing import Optional

import rich

from codeenigma.bundler.base import IBundler


class PoetryBundler(IBundler):
    @staticmethod
    def remove_readme_before_build(pyproject_path: Path):
        with open(pyproject_path) as f:
            content = f.read()

        with open(pyproject_path, "w") as f:
            f.write(content.replace('readme = "README.md"', ""))

    def create_wheel(
        self, module_path: Path, output_dir: Optional[Path] = None, **kwargs
    ):
        # check if the pyproject.toml is in poetry format
        if not (module_path.parent / "pyproject.toml").exists():
            raise FileNotFoundError(f"pyproject.toml not found in {module_path.parent}")

        # check if the pyproject.toml is in poetry format
        with open(module_path.parent / "pyproject.toml", "rb") as f:
            import tomllib

            content = tomllib.load(f)
            try:
                version = content["tool"]["poetry"]["version"]
            except KeyError as e:
                raise Exception(
                    "Invalid pyproject.toml file, not in poetry format"
                ) from e

        if kwargs.get("remove_readme", True):
            self.remove_readme_before_build(module_path.parent / "pyproject.toml")

        rich.print("[bold blue]Building wheel using poetry[/bold blue]")
        subprocess.run(
            ["poetry", "build", "-f", "wheel"],
            cwd=str(module_path.parent),
            check=True,
        )

        wheel_file = list((module_path.parent / "dist").glob(f"*{version}*.whl"))[-1]
        final_wheel_location = wheel_file

        if output_dir:
            output_dir.mkdir(exist_ok=True)
            final_wheel_location = output_dir / wheel_file.name
            shutil.move(wheel_file, final_wheel_location)

        rich.print(
            f"[green]✓ Wheel built successfully ({final_wheel_location})[/green]"
        )
        return final_wheel_location

    def create_extension(
        self, module_path: Path, output_dir: Optional[Path] = None, **kwargs
    ) -> Path:
        if (module_path.parent / "setup.py").exists():
            location = module_path.parent

        elif (module_path / "setup.py").exists():
            location = module_path
        else:
            raise FileNotFoundError(
                f"setup.py not found in {module_path.parent} or {module_path}"
            )

        rich.print("[bold blue]Building extension using poetry[/bold blue]")
        try:
            subprocess.run(
                ["poetry", "run", "python", "setup.py", "build_ext", "--inplace"],
                cwd=str(location),
                check=True,
            )
        except subprocess.CalledProcessError:
            import sys

            subprocess.run(
                [sys.executable, "setup.py", "build_ext", "--inplace"],
                cwd=str(location),
                check=True,
            )

        so_file = list(location.glob("*.so"))[-1]
        # clean up intermediate files
        shutil.rmtree(location / "build")

        final_so_location = so_file
        if output_dir:
            output_dir.mkdir(exist_ok=True)
            shutil.move(so_file, output_dir / so_file.name)
            final_so_location = output_dir / so_file.name

        rich.print(
            f"[green]✓ Extension built successfully ({final_so_location})[/green]"
        )
        return final_so_location

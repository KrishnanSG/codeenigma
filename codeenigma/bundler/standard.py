import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import rich

from codeenigma.bundler.base import IBundler


class StandardBundler(IBundler):  # pragma: no cover
    """
    A bundler that uses standard Python packaging tools (setuptools) and is compatible with uv.
    Works with setup.py or pyproject.toml (setuptools backend).
    """

    @staticmethod
    def _check_for_setuptools_project(project_root: Path):
        status = False
        if (project_root / "setup.py").exists():
            status = True

        elif (project_root / "pyproject.toml").exists():
            try:
                with open(project_root / "pyproject.toml", "rb") as f:
                    import tomllib

                    content = tomllib.load(f)
                    build_backend = content.get("build-system", {}).get(
                        "build-backend", ""
                    )
                    status = "setuptools" in build_backend
            except KeyError:
                status = False

        if not status:
            raise ValueError(
                "Project does not appear to be a setuptools project. "
                "Cannot build extensions without setuptools."
            )

    def create_wheel(
        self, module_path: Path, output_dir: Optional[Path] = None, **kwargs
    ):
        self._check_for_setuptools_project(module_path.parent)
        rich.print("[bold blue]Building wheel using standard setuptools[/bold blue]")
        try:
            # First try with uv if available
            subprocess.run(
                ["uv", "pip", "wheel", "--no-deps", "-e", "."],
                cwd=str(module_path.parent),
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fall back to pip if uv is not available
            subprocess.run(
                ["pip", "install", "build"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [sys.executable, "-m", "build", "--wheel"],
                cwd=str(module_path.parent),
                check=True,
                capture_output=True,
            )

        wheel_file = list((module_path.parent / "dist").glob("*.whl"))[-1]
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
    ):
        # Build the extension in-place
        self._check_for_setuptools_project(module_path.parent)
        if (module_path.parent / "setup.py").exists():
            location = module_path.parent

        elif (module_path / "setup.py").exists():
            location = module_path

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

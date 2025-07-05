import os
import platform
import shutil
from collections.abc import Sequence
from pathlib import Path
from string import Template
from typing import Optional

import rich

from codeenigma import __version__
from codeenigma.bundler import IBundler
from codeenigma.extensions.base import IExtension
from codeenigma.runtime.base import IRuntimeBuilder
from codeenigma.strategies import BaseObfuscationStrategy


class CythonRuntimeBuilder(IRuntimeBuilder):
    def __init__(
        self,
        strategy: BaseObfuscationStrategy,
        bundler: IBundler,
        extensions: Optional[Sequence[IExtension]] = None,
    ):
        super().__init__(strategy, bundler, extensions=extensions)

    @staticmethod
    def create_cython_setup(output_path: Path):
        """Generates a setup.py file for compiling the codeenigma.pyx file"""
        rich.print(
            "[bold blue]Creating setup.py file for compiling the codeenigma.pyx file [/bold blue]"
        )
        with open(Path(__file__).parent / "setup.py.template", encoding="utf-8") as f:
            template = Template(f.read())

        setup_code = template.safe_substitute({"version": repr(__version__)})
        with open(output_path / "setup.py", "w", encoding="utf-8") as f:
            f.write(setup_code)

    @staticmethod
    def create_init_file(output_path: Path):
        """Creates the __init__.py file"""
        rich.print(
            "[bold blue]Creating codeenigma_runtime/__init__.py file[/bold blue]"
        )
        with open(Path(__file__).parent / "init.py.template", encoding="utf-8") as f:
            template = Template(f.read())

        init_code = template.safe_substitute({"platform": repr(platform.system())})
        with open(output_path / "__init__.py", "w", encoding="utf-8") as f:
            f.write(init_code)

    @staticmethod
    def create_pyproject_toml(so_file_path: str, output_path: Path):
        """Creates the pyproject.toml file"""
        rich.print(
            "[bold blue]Creating pyproject.toml file for codeenigma_runtime pkg[/bold blue]"
        )
        with open(
            Path(__file__).parent / "pyproject.toml.template", encoding="utf-8"
        ) as f:
            template = Template(f.read())

        pyproject_content = template.safe_substitute(
            {"version": repr(__version__), "so_file_path": str(so_file_path)}
        )
        with open(output_path / "pyproject.toml", "w", encoding="utf-8") as f:
            f.write(pyproject_content)

    def prepare_runtime_code(self, runtime_pyx_path: Path):
        with open(runtime_pyx_path, "w", encoding="utf-8") as f:
            code = self.strategy.get_runtime_code()

            for extension in self.extensions:
                code += extension.get_code()

            f.write(code)

    def build(self, output_dir: Path):
        """Builds the runtime package"""

        rich.print("[bold blue]Building the runtime package[/bold blue]")

        # Building the .so extension
        # Step 1: Creates the codeenigma.pyx and setup files
        output_dir.mkdir(exist_ok=True)
        self.prepare_runtime_code(output_dir / "codeenigma_runtime.pyx")
        self.create_cython_setup(output_dir)

        # Step 2: Compiles the codeenigma.pyx file using the bundler to .so
        so_file = self.bundler.create_extension(output_dir)

        # Clean up intermediate files
        for temp_file in [
            "setup.py",
            "codeenigma_runtime.pyx",
            "codeenigma_runtime.c",
        ]:
            try:
                os.remove(output_dir / temp_file)
            except FileNotFoundError:
                pass
        shutil.rmtree(output_dir / "build", ignore_errors=True)

        # Packing into codeenigma_runtime wheel

        rich.print("[bold blue]\nPacking the runtime package[/bold blue]")
        # Step 3: Creates the __init__.py file
        Path(output_dir / "codeenigma_runtime").mkdir(exist_ok=True)
        shutil.move(so_file, output_dir / "codeenigma_runtime" / so_file.name)
        self.create_init_file(output_dir / "codeenigma_runtime")

        # Step 4: Creates a pyproject.toml file
        self.create_pyproject_toml(f".codeenigma_runtime/{so_file.name}", output_dir)

        # Step 5. Generates wheel using the bundler
        self.bundler.create_wheel(output_dir / "codeenigma_runtime", output_dir)

        rich.print("[green]✓ Runtime package built successfully[/green]")

import os
import shutil
from pathlib import Path
from shutil import rmtree
from string import Template

import rich

from codeenigma.runtime.base import IRuntimeBuilder
from codeenigma.strategies import BaseObfuscationStrategy


class Orchestrator:
    """Main orchestrator class for CodeEnigma's obfuscation process.

    This class handles the complete workflow of obfuscating Python modules,
    including file processing, code transformation, and runtime environment setup.
    """

    def __init__(
        self,
        module_path: Path,
        strategy: BaseObfuscationStrategy,
        runtime_builder: IRuntimeBuilder,
        output_dir: Path = Path("cedist"),
    ):
        self.module_path = Path(module_path)
        self.strategy = strategy
        self.runtime_builder = runtime_builder
        self.output_dir = Path(output_dir)

    def _create_obfuscation_file(self, file_path: Path, output_path: Path) -> None:
        """Creates an obfuscated version of a single Python file.

        This method takes a Python file, obfuscates its contents, and wraps it
        in a secure execution environment.

        Args:
            file_path: Path to the source Python file to obfuscate.
            output_path: Path where the obfuscated file should be saved.

        Note:
            The generated file will import and use the codeenigma_runtime module
            to securely execute the obfuscated code.
        """
        secure_code = self.strategy.obfuscate(file_path)

        with open(
            Path(__file__).parent / "executor.py.template", encoding="utf-8"
        ) as f:
            template = Template(f.read())

        runtime_embedded_code = template.safe_substitute(
            {"filename": file_path.name, "secure_code": secure_code}
        )

        # Write the obfuscated module
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(runtime_embedded_code)

    def _process_file(self, file_path: Path) -> None:
        """Processes a single Python file and obfuscates it.

        Args:
            file_path: Path to the Python file to process.
        """
        try:
            # Get relative path for module structure
            rel_path = file_path.relative_to(self.module_path.parent)
            output_path = self.output_dir / rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            self._create_obfuscation_file(file_path, output_path)

        except Exception as e:
            rich.print(f"[red]Error processing {file_path}: {e}[/red]")
            raise

    def run_obfuscation(self):
        """Orchestrates the complete obfuscation process for the target module"""
        py_files = list(self.module_path.glob("**/*.py"))
        if not py_files:
            rich.print("[yellow]No Python files found to obfuscate.[/yellow]")
            return

        for idx, py_file in enumerate(py_files):
            rich.print(
                f"[white]({idx + 1}/{len(py_files)}) Obfuscating {py_file}[/white]"
            )
            self._process_file(py_file)

    def build_obfuscated_wheel(self):
        """Builds the obfuscated wheel for the module"""
        if not (self.module_path.parent / "pyproject.toml").exists():
            rich.print(
                "[yellow]Skipping obfuscated wheel build, since no pyproject.toml found in the module. Hence can't build obfuscated module into wheel. Consider creating a pyproject.toml file in the module directory. Refer pep621 or poetry for more details.[/yellow]"
            )
            rich.print(
                f"[white]You can build the wheel manually later too. You can find the obfuscated module in the {self.output_dir} directory.[/white]"
            )
            return 0

        shutil.copy(
            self.module_path.parent / "pyproject.toml",
            self.output_dir / "pyproject.toml",
        )
        self.runtime_builder.bundler.create_wheel(
            self.output_dir / self.module_path.name, self.output_dir, remove_readme=True
        )

        # remove pyproject.toml
        os.remove(self.output_dir / "pyproject.toml")

    def run(self):
        # Base Checks
        if not self.module_path.exists():
            raise FileNotFoundError(f"Module path not found: {self.module_path}")

        if self.output_dir.exists():
            rmtree(self.output_dir)
            rich.print(
                "[yellow]Output directory cleaned prior to obfuscation.[/yellow]\n"
            )

        rich.print("[bold magenta][1/3] Starting obfuscation process...[/bold magenta]")
        self.run_obfuscation()

        rich.print("[bold magenta]\n[2/3] Creating runtime package...[/bold magenta]")
        self.runtime_builder.build(self.output_dir)

        rich.print(
            "[bold magenta]\n[3/3] Creating wheel for obfuscated module...[/bold magenta]"
        )
        self.build_obfuscated_wheel()

        # Cleanup
        shutil.rmtree(self.output_dir / "dist", ignore_errors=True)

        rich.print("[green]✓ Obfuscation completed successfully[/green]")

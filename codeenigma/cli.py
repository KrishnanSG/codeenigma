"""
CLI interface for CodeEnigma orchestrator.
"""

from datetime import UTC, datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from codeenigma import __version__
from codeenigma.orchestrator import Orchestrator

app = typer.Typer(
    name="codeenigma",
    help="CodeEnigma: Securely obfuscate and distribute your Python code.",
    add_completion=True,
)
console = Console()


def display_banner():
    """Display a nice CLI banner."""
    console.print(
        Panel.fit(
            f"""[bold green]A simple, secure and FOSS python code obfuscator using AES and Base64, executed on Cython built runtime for added security. Each file is obfuscated separately using a unique key generated during the initialization.[/bold green]
[bold yellow]License:[/bold yellow] MIT
[bold yellow]Author:[/bold yellow] KrishnanSG
[bold yellow]Version:[/bold yellow] {__version__}""",
            title="🚀 [bold cyan]Welcome to CodeEnigma[/bold cyan]",
            border_style="bright_magenta",
        )
    )


@app.command()
def obfuscate(
    module_path: str = typer.Argument(
        ..., help="Path to the Python module to obfuscate"
    ),
    expiration_date: str = typer.Option(
        None,
        "--expiration",
        "-e",
        help="Expiration date for the obfuscated code (YYYY-MM-DD)",
    ),
    output_dir: str = typer.Option(
        "dist", "--output", "-o", "--dist", help="Output directory for obfuscated files"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Obfuscate a Python module and its dependencies."""
    display_banner()

    module_path = Path(module_path)
    if not module_path.exists():
        console.print(
            f"[bold red]Error: Module path '{module_path}' does not exist[/bold red]"
        )
        raise typer.Exit(1)

    if not module_path.is_dir():
        console.print(
            "[bold red]Error: Module path must be a directory containing Python files[/bold red]"
        )
        raise typer.Exit(1)

    if expiration_date:
        try:
            expiration_date = datetime.fromisoformat(expiration_date)
        except ValueError:
            console.print(
                "[bold red]Error: Invalid expiration date format. Please use YYYY-MM-DD HH:MM:SS+0000[/bold red]"
            )
            raise typer.Exit(1) from None

    if expiration_date and expiration_date < datetime.now(tz=UTC):
        console.print(
            "[bold red]Error: Expiration date must be in the future[/bold red]"
        )
        raise typer.Exit(1)

    orchestrator = Orchestrator(
        str(module_path), output_dir, expiration_date=expiration_date
    )

    try:
        if verbose:
            console.print("\n[bold]Starting obfuscation process...[/bold]")
        orchestrator.obfuscate_module()

        if verbose:
            console.print(
                "\n[bold green]Obfuscation completed successfully![/bold green]"
            )
            console.print(f"Output files saved to: {Path(output_dir).resolve()}")

    except Exception as e:
        console.print(f"\n[bold red]Error during obfuscation:[/bold red] {str(e)}")
        raise typer.Exit(1) from None


@app.command()
def version():
    """Show the version of CodeEnigma."""
    console.print(f"CodeEnigma CLI v{__version__}")


if __name__ == "__main__":
    app()

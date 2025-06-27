"""
CLI interface for PyCodeEnigma orchestrator.
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from codeenigma.orchestrator import Orchestrator

app = typer.Typer(name="codeenigma", add_completion=True)
console = Console()


def display_banner():
    """Display a nice CLI banner."""
    console.print(
        Panel.fit(
            """[bold green]A simple, secure and FOSS python code obfuscator using AES and Base64, executed on Cython built runtime for added security. Each file is obfuscated separately using a unique ke generated during the initialization.[/bold green]
[bold yellow]License:[/bold yellow] MIT
[bold yellow]Author:[/bold yellow] KrishnanSG
[bold yellow]Version:[/bold yellow] 1.0.0""",
            title=f"🚀 [bold cyan]Welcome to CodeEnigma[/bold cyan]",
            border_style="bright_magenta",
        )
    )

@app.command()
def obfuscate(
    module_path: str = typer.Argument(..., help="Path to the Python module to obfuscate"),
    output_dir: str = typer.Option("dist", "--output", "-o", "--dist", help="Output directory for obfuscated files"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Obfuscate a Python module and its dependencies."""
    display_banner()

    module_path = Path(module_path)
    if not module_path.exists():
        console.print(f"[bold red]Error: Module path '{module_path}' does not exist[/bold red]")
        raise typer.Exit(1)

    if not module_path.is_dir():
        console.print("[bold red]Error: Module path must be a directory containing Python files[/bold red]")
        raise typer.Exit(1)

    orchestrator = Orchestrator(str(module_path), output_dir)

    try:
        if verbose:
            console.print("\n[bold]Starting obfuscation process...[/bold]")
        orchestrator.obfuscate_module()

        if verbose:
            console.print("\n[bold green]Obfuscation completed successfully![/bold green]")
            console.print(f"Output files saved to: {Path(output_dir).resolve()}")

    except Exception as e:
        console.print(f"\n[bold red]Error during obfuscation:[/bold red] {str(e)}")
        raise typer.Exit(1) from None


@app.command()
def version():
    """Show the version of PyCodeEnigma."""
    console.print("CodeEnigma CLI v1.0.0")


if __name__ == "__main__":
    app()

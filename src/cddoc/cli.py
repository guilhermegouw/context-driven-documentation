"""CLI entry point for cddoc."""

import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .init import InitializationError, initialize_project

console = Console()


@click.group()
@click.version_option()
def main():
    """Context-Driven Documentation CLI."""
    pass


@main.command()
@click.argument('path', default='.')
@click.option(
    '--force',
    is_flag=True,
    help='Overwrite existing files (use with caution)',
)
@click.option(
    '--minimal',
    is_flag=True,
    help='Create only essential structure, skip templates',
)
def init(path, force, minimal):
    """Initialize CDD structure in a project.

    PATH: Target directory for initialization (defaults to current directory)

    Examples:
        cdd init .              # Initialize in current directory
        cdd init my-project     # Create and initialize new project
        cdd init --minimal .    # Create structure without templates
    """
    console.print(
        Panel.fit(
            "🚀 [bold]Initializing Context-Driven Documentation[/bold]",
            border_style="blue",
        )
    )

    try:
        # Initialize the project
        result = initialize_project(path, force=force, minimal=minimal)

        # Display results
        console.print()
        _display_results(result)

        # Show next steps
        console.print()
        _display_next_steps(result['path'])

        sys.exit(0)

    except InitializationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


def _display_results(result: dict):
    """Display initialization results in a formatted table.

    Args:
        result: Dictionary containing initialization results
    """
    created_dirs = result.get('created_dirs', [])
    created_files = result.get('created_files', [])
    skipped_files = result.get('skipped_files', [])

    # Create summary table
    table = Table(title="Initialization Summary", show_header=True)
    table.add_column("Item", style="cyan")
    table.add_column("Status", style="green")

    # Add created directories
    for dir_path in created_dirs:
        table.add_row(f"📁 {dir_path}", "✅ Created")

    # Add created files
    for file_path in created_files:
        table.add_row(f"📄 {file_path}", "✅ Created")

    # Add skipped files
    for file_path in skipped_files:
        table.add_row(f"📄 {file_path}", "⚠️  Skipped (exists)")

    if table.row_count > 0:
        console.print(table)
    else:
        console.print(
            "[yellow]ℹ️  All directories and files already exist[/yellow]"
        )


def _display_next_steps(project_path):
    """Display next steps for the user.

    Args:
        project_path: Path where project was initialized
    """
    next_steps = """[bold]Next Steps:[/bold]

1. 📝 Edit [cyan]specs/project.yaml[/cyan] to describe your project
   - Update project name and description
   - Define your tech stack and architecture
   - Set code conventions and standards

2. 🎯 Create your first feature spec:
   [cyan]cdd new your-first-feature[/cyan]

3. 🤖 Use with Claude Code:
   Run [cyan]/sync-docs[/cyan] to load specs into context

4. 📚 Learn more:
   Visit [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    console.print(
        Panel(
            next_steps,
            title="🎉 CDD Initialized Successfully!",
            border_style="green",
        )
    )


if __name__ == '__main__':
    main()

"""CLI entry point for cddoc."""

import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .init import InitializationError, initialize_project
from .new_ticket import TicketCreationError, create_new_ticket

console = Console()


@click.group()
@click.version_option()
def main():
    """Context-Driven Documentation CLI."""
    pass


@main.command()
@click.argument("path", default=".")
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing files (use with caution)",
)
@click.option(
    "--minimal",
    is_flag=True,
    help="Create only essential structure, skip templates",
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
        _display_next_steps(result["path"])

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
    created_dirs = result.get("created_dirs", [])
    created_files = result.get("created_files", [])
    skipped_files = result.get("skipped_files", [])

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

1. 📝 Complete your project constitution in [cyan]CLAUDE.md[/cyan]
   - In Claude Code, run: [cyan]/socrates CLAUDE.md[/cyan]
   - Have a natural conversation with Socrates AI
   - Your constitution will be built through dialogue

2. 🎯 Create your first ticket specification:
   - In Claude Code, run: [cyan]/socrates specs/tickets/your-feature/spec.yaml[/cyan]
   - Socrates will guide you through documenting your feature

3. 🤖 Start development with full context (coming soon):
   - Use your completed specs to build features
   - AI will have complete project context from your documentation

4. 📚 Learn more:
   - Check [cyan]examples/SOCRATES_GUIDE.md[/cyan] for detailed usage
   - Visit [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    console.print(
        Panel(
            next_steps,
            title="🎉 CDD Framework Initialized Successfully!",
            border_style="green",
        )
    )


@main.command()
@click.argument(
    "ticket_type",
    type=click.Choice(["feature", "bug", "spike"], case_sensitive=False),
)
@click.argument("name")
def new(ticket_type, name):
    """Create a new ticket specification file.

    TICKET_TYPE: Type of ticket (feature, bug, or spike)
    NAME: Name for the ticket (will be auto-normalized)

    Examples:
        cdd new feature user-authentication
        cdd new bug "Payment Processing Error"
        cdd new spike api_performance_investigation

    The command will:
    - Normalize the name to lowercase-with-dashes format
    - Create specs/tickets/<type>-<name>/spec.yaml
    - Populate template with current date
    - Show you the next steps
    """
    console.print(
        Panel.fit(
            f"🎫 [bold]Creating {ticket_type.title()} Ticket[/bold]",
            border_style="blue",
        )
    )

    try:
        # Create the ticket
        result = create_new_ticket(ticket_type.lower(), name)

        # Display success
        console.print()
        _display_ticket_success(result)

        sys.exit(0)

    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


def _display_ticket_success(result: dict):
    """Display ticket creation success message.

    Args:
        result: Dictionary containing creation results
    """
    ticket_path = result["ticket_path"]
    normalized_name = result["normalized_name"]
    ticket_type = result["ticket_type"]
    overwritten = result["overwritten"]

    # Create status message
    status = "Overwritten" if overwritten else "Created"

    # Show creation summary
    table = Table(title=f"{status} Successfully", show_header=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Type", ticket_type.title())
    table.add_row("Normalized Name", normalized_name)
    table.add_row("Location", str(ticket_path))
    table.add_row("Spec File", str(ticket_path / "spec.yaml"))

    console.print(table)

    # Show next steps
    next_steps = f"""[bold]Next Steps:[/bold]

1. 📝 Fill out your ticket specification:
   - In Claude Code, run: [cyan]/socrates {ticket_path / "spec.yaml"}[/cyan]
   - Have a natural conversation with Socrates AI
   - Your specification will be built through dialogue

2. 🎯 Generate implementation plan:
   - In Claude Code, run: [cyan]/plan {ticket_path / "spec.yaml"}[/cyan]
   - Planner will analyze your spec and create a detailed plan
   - Review the generated plan: [cyan]{ticket_path / "plan.md"}[/cyan]

3. 🚀 Start implementation:
   - Use the plan.md as your implementation guide
   - Claude will have full context from spec + plan
   - Build with confidence!

4. 📚 Learn more:
   - Visit [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    console.print()
    console.print(
        Panel(
            next_steps,
            title="🎉 Ticket Created Successfully!",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()

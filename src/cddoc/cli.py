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
    installed_commands = result.get("installed_commands", [])
    installed_templates = result.get("installed_templates", [])
    claude_md_created = result.get("claude_md_created", False)

    # Create summary table
    table = Table(title="Initialization Summary", show_header=True)
    table.add_column("Component", style="cyan", width=40)
    table.add_column("Status", style="green", width=20)

    # Add created directories
    for dir_path in created_dirs:
        table.add_row(f"📁 {dir_path}", "✅ Created")

    # Add CLAUDE.md
    if claude_md_created:
        table.add_row("📄 CLAUDE.md", "✅ Created")
    else:
        table.add_row("📄 CLAUDE.md", "⚠️  Already exists")

    # Add framework commands
    for cmd_path in installed_commands:
        table.add_row(f"🤖 {cmd_path}", "✅ Installed")

    # Add templates
    for template_path in installed_templates:
        table.add_row(f"📋 {template_path}", "✅ Installed")

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
    next_steps = """[bold]Your CDD Framework is Ready![/bold]

📁 Structure Created:
   • [cyan]CLAUDE.md[/cyan] - Project constitution (edit this first!)
   • [cyan]specs/tickets/[/cyan] - Active sprint work
   • [cyan]specs/archive/[/cyan] - Completed tickets (auto-archived by /exec)
   • [cyan]docs/features/[/cyan] - Living documentation
   • [cyan].claude/commands/[/cyan] - AI agents (socrates, plan, exec)
   • [cyan].cdd/templates/[/cyan] - Internal templates

🤖 [bold]Meet Socrates - Think Better, Document Faster[/bold]

Stop writing specs alone. Socrates is your thinking partner:
   ✓ Brainstorm through conversation, not forms
   ✓ Uncover edge cases before they become bugs
   ✓ Structure scattered thoughts into clear requirements
   ✓ Stay focused on what matters

Walk in with an idea. Walk out with a complete spec.

🚀 [bold]Quick Start Workflow:[/bold]

1. [yellow]Edit CLAUDE.md[/yellow] - Capture your project's context once, AI understands it forever
   Tip: Brainstorm with [green]/socrates CLAUDE.md[/green] to build it together

2. [yellow]Create a ticket:[/yellow] [green]cdd new feature user-auth[/green]
   Generates a ticket in specs/tickets/

3. [yellow]Gather requirements:[/yellow] [green]/socrates feature-user-auth[/green]
   Brainstorm with Socrates - uncover edge cases, clarify scope, build complete specs

4. [yellow]Generate plan:[/yellow] [green]/plan feature-user-auth[/green]
   Clear spec → Detailed plan → Confident implementation

5. [yellow]Implement:[/yellow] [green]/exec feature-user-auth[/green]
   Clear spec + Detailed plan = AI builds exactly what you need (not what it guesses)

📚 [bold]Learn More:[/bold]
   [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    console.print(
        Panel(
            next_steps,
            title="✅ CDD Framework Initialized",
            border_style="green",
        )
    )


@main.group(invoke_without_command=False)
def new():
    """Create new tickets or documentation."""
    pass


@new.command()
@click.argument("name")
def feature(name):
    """Create a new feature ticket.

    Examples:
        cdd new feature user-authentication
    """
    console.print(
        Panel.fit(
            "🎫 [bold]Creating Feature Ticket[/bold]",
            border_style="blue",
        )
    )

    try:
        result = create_new_ticket("feature", name)
        console.print()
        _display_ticket_success(result)
        sys.exit(0)
    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


@new.command()
@click.argument("name")
def bug(name):
    """Create a new bug ticket.

    Examples:
        cdd new bug "Payment Processing Error"
    """
    console.print(
        Panel.fit(
            "🎫 [bold]Creating Bug Ticket[/bold]",
            border_style="blue",
        )
    )

    try:
        result = create_new_ticket("bug", name)
        console.print()
        _display_ticket_success(result)
        sys.exit(0)
    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


@new.command()
@click.argument("name")
def spike(name):
    """Create a new spike (research) ticket.

    Examples:
        cdd new spike api_performance_investigation
    """
    console.print(
        Panel.fit(
            "🎫 [bold]Creating Spike Ticket[/bold]",
            border_style="blue",
        )
    )

    try:
        result = create_new_ticket("spike", name)
        console.print()
        _display_ticket_success(result)
        sys.exit(0)
    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


@new.command()
@click.argument("name")
def enhancement(name):
    """Create a new enhancement ticket.

    Examples:
        cdd new enhancement improve-error-messages
    """
    console.print(
        Panel.fit(
            "🎫 [bold]Creating Enhancement Ticket[/bold]",
            border_style="blue",
        )
    )

    try:
        result = create_new_ticket("enhancement", name)
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


@new.group()
def documentation():
    """Create documentation files (guides or features)."""
    pass


@documentation.command(name="guide")
@click.argument("name")
def doc_guide(name):
    """Create a new guide documentation file.

    Examples:
        cdd new documentation guide getting-started
    """
    console.print(
        Panel.fit(
            "📚 [bold]Creating Guide Documentation[/bold]",
            border_style="blue",
        )
    )

    try:
        from .new_ticket import (
            TicketCreationError,
            create_new_documentation,
        )

        result = create_new_documentation("guide", name)
        console.print()
        _display_documentation_success(result)
        sys.exit(0)
    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


@documentation.command(name="feature")
@click.argument("name")
def doc_feature(name):
    """Create a new feature documentation file.

    Examples:
        cdd new documentation feature authentication
    """
    console.print(
        Panel.fit(
            "📚 [bold]Creating Feature Documentation[/bold]",
            border_style="blue",
        )
    )

    try:
        from .new_ticket import (
            TicketCreationError,
            create_new_documentation,
        )

        result = create_new_documentation("feature", name)
        console.print()
        _display_documentation_success(result)
        sys.exit(0)
    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


def _display_documentation_success(result: dict):
    """Display documentation creation success message.

    Args:
        result: Dictionary containing creation results
    """
    file_path = result["file_path"]
    normalized_name = result["normalized_name"]
    doc_type = result["doc_type"]
    overwritten = result["overwritten"]

    # Create status message
    status = "Overwritten" if overwritten else "Created"

    # Show creation summary
    table = Table(title=f"{status} Successfully", show_header=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Type", f"{doc_type.title()} Documentation")
    table.add_row("File Name", f"{normalized_name}.md")
    table.add_row("Location", str(file_path))

    console.print(table)

    # Show next steps
    next_steps = f"""[bold]Next Steps:[/bold]

1. 📝 Fill out your documentation with Socrates:
   - In Claude Code, run: [cyan]/socrates {file_path}[/cyan]
   - Have a natural conversation to build comprehensive docs
   - Socrates will help you think through the structure

2. 📚 Documentation is now part of your living docs:
   - Guide docs: Help users understand and use features
   - Feature docs: Technical reference for implementation details
   - Keep it updated as the code evolves

3. 🔗 Link related documentation:
   - Cross-reference other guides and features
   - Build a knowledge network

4. 🎯 Remember the CDD philosophy:
   - Context captured once, understood forever
   - Living documentation that evolves with your code
   - AI assistants have full context automatically

[bold]Pro tip:[/bold] Use Socrates to brainstorm! Start the conversation even if you're not
sure what to write - Socrates will ask the right questions.
"""

    console.print()
    console.print(
        Panel(
            next_steps,
            title="🎉 Documentation File Created!",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()

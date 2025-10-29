"""Socrates: Intelligent conversation-driven documentation assistant."""

from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .handlers import ConstitutionHandler, FileHandler, TicketSpecHandler

console = Console()


class SocratesError(Exception):
    """Raised when Socrates cannot proceed with file operations."""

    pass


def socrates_conversation(file_path: str) -> None:
    """Main entry point for Socrates conversations.

    Args:
        file_path: Path to file for conversation-driven development

    Raises:
        SocratesError: If file operations fail
    """
    try:
        # 1. Validate and resolve file path
        path = Path(file_path).resolve()

        # 2. Detect file type and create appropriate handler
        handler = create_file_handler(path)

        # 3. Read current content
        current_content = handler.read_current_content(path)

        # 4. Start conversation
        console.print(
            Panel.fit(
                "🧠 [bold]Socrates: Intelligent Documentation Assistant[/bold]",
                border_style="blue",
            )
        )

        conversation_data = handler.start_conversation(current_content, path)

        # 5. Update file with results
        update_results = handler.update_file(path, conversation_data)

        # 6. Display results
        display_update_results(update_results)

    except SocratesError as e:
        console.print(f"[red]❌ Socrates Error:[/red] {e}")
        raise
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Conversation cancelled by user[/yellow]")
        raise SocratesError("Conversation cancelled")
    except Exception as e:
        console.print(f"[red]❌ Unexpected Error:[/red] {e}")
        raise SocratesError(f"Failed to complete conversation: {e}")


def create_file_handler(path: Path) -> FileHandler:
    """Create appropriate file handler based on file type.

    Args:
        path: Path to file

    Returns:
        Appropriate FileHandler instance

    Raises:
        SocratesError: If file type is not supported
    """
    # Check for CLAUDE.md constitution file
    if path.name == "CLAUDE.md":
        return ConstitutionHandler()

    # Check for ticket specification YAML files
    elif path.suffix in [".yaml", ".yml"] and "tickets" in path.parts:
        return TicketSpecHandler()

    # Check for command markdown files
    elif path.suffix == ".md" and "commands" in path.parts:
        # CommandHandler not yet implemented
        raise SocratesError(
            "Command markdown files are not yet supported. "
            "Coming in a future release!"
        )

    else:
        # Provide helpful error message
        file_type = path.suffix or "unknown type"
        raise SocratesError(
            f"Unsupported file type: {file_type}\n\n"
            "Socrates currently supports:\n"
            "  • CLAUDE.md - Project constitution files\n"
            "  • specs/tickets/**/*.yaml - Ticket specification files\n"
            "  • .claude/commands/*.md - Command files (coming soon)\n\n"
            f"Your file: {path}"
        )


def display_update_results(results: Dict[str, Any]) -> None:
    """Display what was updated in a beautiful format.

    Args:
        results: Dictionary containing update results
    """
    updates = results.get("updates", [])
    file_path = results.get("file_path", "")
    next_steps = results.get("next_steps", [])

    # Display success message
    console.print()
    console.print(
        Panel.fit(
            f"✅ [bold green]Successfully updated {Path(file_path).name}[/bold green]",
            border_style="green",
        )
    )

    # Create update summary table
    if updates:
        console.print()
        table = Table(
            title="📝 Socrates Updates", show_header=True, show_lines=True
        )
        table.add_column("Section", style="cyan", no_wrap=False)
        table.add_column("Action", style="green", width=12)
        table.add_column("Content Preview", style="yellow", no_wrap=False)

        for update in updates:
            preview = update.get("preview", "")
            # Truncate long previews
            if len(preview) > 60:
                preview = preview[:57] + "..."

            table.add_row(
                update.get("section", ""),
                update.get("action", ""),
                preview,
            )

        console.print(table)

    # Show file location
    console.print()
    console.print(f"📄 [cyan]File saved:[/cyan] {file_path}")

    # Show next steps
    if next_steps:
        console.print()
        console.print(
            Panel(
                "\n".join([f"• {step}" for step in next_steps]),
                title="🎯 Suggested Next Steps",
                border_style="green",
            )
        )

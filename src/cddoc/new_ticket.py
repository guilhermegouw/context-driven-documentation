"""Create new ticket specification files."""

import re
import subprocess
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console

console = Console()


class TicketCreationError(Exception):
    """Raised when ticket creation cannot proceed."""

    pass


def normalize_ticket_name(name: str) -> str:
    """Normalize ticket name to lowercase-with-dashes format.

    Algorithm:
    1. Convert to lowercase
    2. Replace spaces, underscores, and special chars with dashes
    3. Remove duplicate consecutive dashes
    4. Strip leading/trailing dashes

    Examples:
        "User Auth System" → "user-auth-system"
        "payment_processing" → "payment-processing"
        "Feature__Name" → "feature-name"
        "  dash-test  " → "dash-test"

    Args:
        name: Raw ticket name from user input

    Returns:
        Normalized name string
    """
    # Convert to lowercase
    normalized = name.lower()

    # Replace special characters and whitespace with dash
    # Keep only alphanumeric and dash
    normalized = re.sub(r"[^a-z0-9-]+", "-", normalized)

    # Remove duplicate dashes
    normalized = re.sub(r"-+", "-", normalized)

    # Strip leading/trailing dashes
    normalized = normalized.strip("-")

    return normalized


def get_git_root() -> Path:
    """Get git repository root directory.

    Returns:
        Path to git root

    Raises:
        TicketCreationError: If not in a git repository
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        raise TicketCreationError(
            "Not a git repository\n"
            "CDD requires git for version control of documentation.\n"
            "Run: git init"
        )
    except FileNotFoundError:
        raise TicketCreationError(
            "Git not found\n"
            "CDD requires git to be installed.\n"
            "Install git: https://git-scm.com/downloads"
        )


def get_template_path(git_root: Path, ticket_type: str) -> Path:
    """Get path to ticket template file.

    Args:
        git_root: Git repository root path
        ticket_type: Type of ticket (feature/bug/spike)

    Returns:
        Path to template file

    Raises:
        TicketCreationError: If template not found
    """
    template_name = f"{ticket_type}-ticket-template.yaml"
    template_path = git_root / ".cdd" / "templates" / template_name

    if not template_path.exists():
        raise TicketCreationError(
            f"Template not found: {template_name}\n"
            f"Templates are required for ticket creation.\n"
            f"Run: cdd init"
        )

    return template_path


def populate_template_dates(template_content: str) -> str:
    """Replace [auto-generated] placeholders with current date.

    Replaces both 'created: [auto-generated]' and 'updated: [auto-generated]'
    with current date in YYYY-MM-DD format.

    Args:
        template_content: Raw template content

    Returns:
        Template content with dates populated
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Replace [auto-generated] with actual date
    content = template_content.replace("[auto-generated]", current_date)

    return content


def check_ticket_exists(ticket_path: Path) -> bool:
    """Check if ticket directory already exists.

    Args:
        ticket_path: Path to ticket directory

    Returns:
        True if exists, False otherwise
    """
    return ticket_path.exists()


def prompt_overwrite() -> bool:
    """Prompt user whether to overwrite existing ticket.

    Safe default is 'n' (don't overwrite).

    Returns:
        True if user wants to overwrite, False otherwise
    """
    response = click.prompt(
        "Ticket already exists. Overwrite? [y/N]",
        type=str,
        default="n",
        show_default=False,
    ).lower()

    return response in ("y", "yes")


def prompt_new_name(ticket_type: str) -> str | None:
    """Prompt user for a new ticket name.

    User can:
    - Enter a new name (will be normalized automatically)
    - Type 'cancel' to abort
    - Press Ctrl+C to abort

    Args:
        ticket_type: Type of ticket (for display in prompt)

    Returns:
        New name string, or None if user cancels
    """
    console.print(
        "\n[yellow]💡 Tip: Type 'cancel' or press Ctrl+C to abort[/yellow]"
    )

    try:
        new_name = click.prompt(
            f"Enter a different name for the {ticket_type} ticket",
            type=str,
        ).strip()

        if new_name.lower() == "cancel":
            return None

        return new_name

    except click.Abort:
        return None


def create_ticket_file(ticket_path: Path, template_path: Path) -> None:
    """Create ticket directory and spec.yaml file.

    Args:
        ticket_path: Path where ticket should be created
        template_path: Path to template file

    Raises:
        TicketCreationError: If creation fails
    """
    try:
        # Create directory
        ticket_path.mkdir(parents=True, exist_ok=True)

        # Read template
        template_content = template_path.read_text()

        # Populate dates
        content = populate_template_dates(template_content)

        # Write spec.yaml
        spec_file = ticket_path / "spec.yaml"
        spec_file.write_text(content)

    except Exception as e:
        raise TicketCreationError(f"Failed to create ticket: {e}")


def create_new_ticket(ticket_type: str, name: str) -> dict:
    """Create a new ticket specification file.

    Main entry point for ticket creation logic.

    Args:
        ticket_type: Type of ticket (feature/bug/spike)
        name: Ticket name (will be normalized)

    Returns:
        Dictionary with creation results:
        {
            "ticket_path": Path,
            "normalized_name": str,
            "ticket_type": str,
            "overwritten": bool
        }

    Raises:
        TicketCreationError: If creation fails
    """
    # Normalize the name
    normalized_name = normalize_ticket_name(name)

    if not normalized_name:
        raise TicketCreationError(
            "Invalid ticket name\n"
            "Name must contain at least one alphanumeric character.\n"
            "Example: cdd new feature user-authentication"
        )

    # Get git root
    git_root = get_git_root()

    # Get template
    template_path = get_template_path(git_root, ticket_type)

    # Construct ticket path
    folder_name = f"{ticket_type}-{normalized_name}"
    ticket_path = git_root / "specs" / "tickets" / folder_name

    overwritten = False

    # Handle existing ticket with loop
    while check_ticket_exists(ticket_path):
        console.print(
            f"\n[yellow]⚠️  Ticket already exists: {ticket_path}[/yellow]"
        )

        if prompt_overwrite():
            overwritten = True
            break
        else:
            # Prompt for new name
            new_name = prompt_new_name(ticket_type)

            if new_name is None:
                raise TicketCreationError("Ticket creation cancelled by user")

            # Re-normalize and reconstruct path
            normalized_name = normalize_ticket_name(new_name)

            if not normalized_name:
                console.print(
                    "[red]❌ Invalid name - must contain alphanumeric "
                    "characters[/red]"
                )
                continue

            folder_name = f"{ticket_type}-{normalized_name}"
            ticket_path = git_root / "specs" / "tickets" / folder_name

    # Create the ticket
    create_ticket_file(ticket_path, template_path)

    return {
        "ticket_path": ticket_path,
        "normalized_name": normalized_name,
        "ticket_type": ticket_type,
        "overwritten": overwritten,
    }

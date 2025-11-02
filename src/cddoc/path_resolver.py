"""Smart path resolution for slash commands."""

import difflib
from pathlib import Path
from typing import List


class PathResolutionError(Exception):
    """Raised when path cannot be resolved."""

    pass


class PathResolver:
    """Resolves ticket shorthand to full paths with fuzzy matching."""

    TICKETS_DIR = Path("specs/tickets")
    SIMILARITY_THRESHOLD = 0.7  # 70% similarity for fuzzy matching
    MAX_SUGGESTIONS = 3

    @staticmethod
    def resolve(argument: str, target_file: str = "spec.yaml") -> Path:
        """Resolve argument to full file path.

        Supports two modes:
        1. Explicit paths (contains '/' or ends with .md/.yaml) - used as-is
        2. Ticket shorthand (simple name) - resolves to specs/tickets/{name}/{target_file}

        Args:
            argument: User input (ticket name or full path)
            target_file: Target file name (spec.yaml or plan.md)

        Returns:
            Resolved Path object

        Raises:
            PathResolutionError: If ticket not found (with helpful suggestions)

        Examples:
            >>> PathResolver.resolve("feature-auth", "spec.yaml")
            Path("specs/tickets/feature-auth/spec.yaml")

            >>> PathResolver.resolve("CLAUDE.md", "spec.yaml")
            Path("CLAUDE.md")

            >>> PathResolver.resolve("specs/tickets/bug-fix/spec.yaml", "spec.yaml")
            Path("specs/tickets/bug-fix/spec.yaml")
        """
        # Check if this is an explicit path (contains / or file extension)
        if "/" in argument or argument.endswith((".md", ".yaml")):
            # Explicit path - use as-is
            return Path(argument)

        # Ticket shorthand - resolve to specs/tickets/{name}/{target_file}
        resolved_path = PathResolver.TICKETS_DIR / argument / target_file

        # Check if ticket directory exists
        ticket_dir = PathResolver.TICKETS_DIR / argument
        if not ticket_dir.exists():
            # Ticket not found - provide helpful error with fuzzy matching
            similar_tickets = PathResolver.find_similar_tickets(argument)
            error_message = PathResolver.format_not_found_error(
                argument, similar_tickets
            )
            raise PathResolutionError(error_message)

        return resolved_path

    @staticmethod
    def find_similar_tickets(ticket_name: str) -> List[str]:
        """Find similar ticket names using fuzzy matching.

        Scans specs/tickets/ directory for similar ticket names using
        difflib for similarity matching.

        Args:
            ticket_name: Ticket name to match against

        Returns:
            List of similar ticket names (max 3), sorted by similarity

        Examples:
            >>> PathResolver.find_similar_tickets("feat-auth")
            ['feature-auth', 'feature-authentication']
        """
        # Check if tickets directory exists
        if not PathResolver.TICKETS_DIR.exists():
            return []

        # Get all ticket directory names
        try:
            all_tickets = [
                d.name
                for d in PathResolver.TICKETS_DIR.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]
        except (OSError, PermissionError):
            # Handle filesystem errors gracefully
            return []

        # Use difflib to find close matches
        similar = difflib.get_close_matches(
            ticket_name,
            all_tickets,
            n=PathResolver.MAX_SUGGESTIONS,
            cutoff=PathResolver.SIMILARITY_THRESHOLD,
        )

        return similar

    @staticmethod
    def format_not_found_error(
        ticket_name: str, similar_tickets: List[str], command: str = "socrates"
    ) -> str:
        """Format helpful error message with suggestions.

        Follows the three-part error pattern:
        1. Clear error message (what went wrong)
        2. Brief context (suggestions or guidance)
        3. Actionable next step (how to fix it)

        Args:
            ticket_name: Ticket that wasn't found
            similar_tickets: List of similar tickets (may be empty)
            command: Command being used (for suggestion examples)

        Returns:
            Formatted error message string

        Examples:
            >>> PathResolver.format_not_found_error("my-feat", ["feature-my-feat"], "socrates")
            '❌ Ticket not found: my-feat\\n\\nDid you mean:\\n• feature-my-feat → /socrates feature-my-feat\\n\\nOr create it: cdd new feature my-feat'
        """
        error_parts = [f"❌ Ticket not found: {ticket_name}"]

        if similar_tickets:
            # Show suggestions
            error_parts.append("\nDid you mean:")
            for ticket in similar_tickets:
                error_parts.append(f"• {ticket} → /{command} {ticket}")
            error_parts.append(f"\nOr create it: cdd new <type> {ticket_name}")
        else:
            # No suggestions - show creation message
            error_parts.append("\nNo existing tickets found.")
            error_parts.append("Did you forget to create it?\n")
            error_parts.append(f"Run: cdd new feature {ticket_name}")
            error_parts.append(f"     cdd new enhancement {ticket_name}")
            error_parts.append(f"     cdd new bug {ticket_name}")

        return "\n".join(error_parts)

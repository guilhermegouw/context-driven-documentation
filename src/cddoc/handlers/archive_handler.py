"""Archive handler for moving completed tickets to archive."""

import shutil
from pathlib import Path


class ArchiveHandlerError(Exception):
    """Base exception for archive handler errors."""

    pass


class ArchiveHandler:
    """Handler for archiving completed tickets."""

    @staticmethod
    def archive_ticket(ticket_path: Path, archive_base: Path) -> Path:
        """Move a ticket folder to the archive directory.

        Args:
            ticket_path: Path to the ticket folder (e.g., specs/tickets/feature-auth)
            archive_base: Base path for archive (e.g., specs/archive)

        Returns:
            Path to the archived ticket

        Raises:
            ArchiveHandlerError: If ticket doesn't exist or archive fails
        """
        if not ticket_path.exists():
            raise ArchiveHandlerError(
                f"Ticket folder not found: {ticket_path}"
            )

        if not ticket_path.is_dir():
            raise ArchiveHandlerError(
                f"Ticket path is not a directory: {ticket_path}"
            )

        # Create archive directory if it doesn't exist
        archive_base.mkdir(parents=True, exist_ok=True)

        # Destination path
        archive_dest = archive_base / ticket_path.name

        # Check if destination already exists
        if archive_dest.exists():
            raise ArchiveHandlerError(
                f"Archived ticket already exists: {archive_dest}"
            )

        try:
            # Move the entire folder
            shutil.move(str(ticket_path), str(archive_dest))
            return archive_dest
        except Exception as e:
            raise ArchiveHandlerError(f"Failed to archive ticket: {e}")

    @staticmethod
    def restore_ticket(archive_path: Path, tickets_base: Path) -> Path:
        """Restore an archived ticket back to active tickets.

        Args:
            archive_path: Path to the archived ticket (e.g., specs/archive/feature-auth)
            tickets_base: Base path for tickets (e.g., specs/tickets)

        Returns:
            Path to the restored ticket

        Raises:
            ArchiveHandlerError: If archive doesn't exist or restore fails
        """
        if not archive_path.exists():
            raise ArchiveHandlerError(
                f"Archived ticket not found: {archive_path}"
            )

        if not archive_path.is_dir():
            raise ArchiveHandlerError(
                f"Archive path is not a directory: {archive_path}"
            )

        # Create tickets directory if it doesn't exist
        tickets_base.mkdir(parents=True, exist_ok=True)

        # Destination path
        restore_dest = tickets_base / archive_path.name

        # Check if destination already exists
        if restore_dest.exists():
            raise ArchiveHandlerError(
                f"Ticket already exists in active tickets: {restore_dest}"
            )

        try:
            # Move the entire folder back
            shutil.move(str(archive_path), str(restore_dest))
            return restore_dest
        except Exception as e:
            raise ArchiveHandlerError(f"Failed to restore ticket: {e}")

    @staticmethod
    def list_archived_tickets(archive_base: Path) -> list[Path]:
        """List all archived tickets.

        Args:
            archive_base: Base path for archive (e.g., specs/archive)

        Returns:
            List of archived ticket paths
        """
        if not archive_base.exists():
            return []

        return [p for p in archive_base.iterdir() if p.is_dir()]

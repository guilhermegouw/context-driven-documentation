"""Tests for archive handler."""

from pathlib import Path

import pytest

from src.cddoc.handlers.archive_handler import (
    ArchiveHandler,
    ArchiveHandlerError,
)


def test_archive_ticket_success(tmp_path):
    """Test archiving a ticket folder successfully."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"
    ticket_folder = tickets_base / "feature-auth"
    ticket_folder.mkdir(parents=True)

    # Create some files in the ticket
    (ticket_folder / "spec.yaml").write_text("ticket: test")
    (ticket_folder / "plan.md").write_text("# Plan")

    # Act
    result = ArchiveHandler.archive_ticket(ticket_folder, archive_base)

    # Assert
    assert not ticket_folder.exists()  # Original should be gone
    assert result.exists()  # Archive should exist
    assert result == archive_base / "feature-auth"
    assert (result / "spec.yaml").exists()
    assert (result / "plan.md").exists()


def test_archive_ticket_not_found(tmp_path):
    """Test archiving a non-existent ticket folder."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"
    nonexistent_ticket = tickets_base / "missing"

    # Act & Assert
    with pytest.raises(ArchiveHandlerError, match="Ticket folder not found"):
        ArchiveHandler.archive_ticket(nonexistent_ticket, archive_base)


def test_archive_ticket_not_directory(tmp_path):
    """Test archiving a file instead of directory."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    tickets_base.mkdir(parents=True)
    archive_base = tmp_path / "specs" / "archive"

    # Create a file instead of directory
    ticket_file = tickets_base / "feature-auth"
    ticket_file.write_text("not a directory")

    # Act & Assert
    with pytest.raises(ArchiveHandlerError, match="not a directory"):
        ArchiveHandler.archive_ticket(ticket_file, archive_base)


def test_archive_ticket_already_exists(tmp_path):
    """Test archiving when destination already exists."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"

    ticket_folder = tickets_base / "feature-auth"
    ticket_folder.mkdir(parents=True)

    # Create archive destination that already exists
    existing_archive = archive_base / "feature-auth"
    existing_archive.mkdir(parents=True)

    # Act & Assert
    with pytest.raises(ArchiveHandlerError, match="already exists"):
        ArchiveHandler.archive_ticket(ticket_folder, archive_base)


def test_archive_ticket_creates_archive_dir(tmp_path):
    """Test that archive directory is created if it doesn't exist."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"

    ticket_folder = tickets_base / "feature-auth"
    ticket_folder.mkdir(parents=True)
    (ticket_folder / "spec.yaml").write_text("test")

    # Verify archive doesn't exist yet
    assert not archive_base.exists()

    # Act
    result = ArchiveHandler.archive_ticket(ticket_folder, archive_base)

    # Assert
    assert archive_base.exists()
    assert result.exists()


def test_restore_ticket_success(tmp_path):
    """Test restoring an archived ticket successfully."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"

    archive_folder = archive_base / "feature-auth"
    archive_folder.mkdir(parents=True)
    (archive_folder / "spec.yaml").write_text("ticket: test")
    (archive_folder / "plan.md").write_text("# Plan")

    # Act
    result = ArchiveHandler.restore_ticket(archive_folder, tickets_base)

    # Assert
    assert not archive_folder.exists()  # Archive should be gone
    assert result.exists()  # Restored ticket should exist
    assert result == tickets_base / "feature-auth"
    assert (result / "spec.yaml").exists()
    assert (result / "plan.md").exists()


def test_restore_ticket_not_found(tmp_path):
    """Test restoring a non-existent archived ticket."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"
    nonexistent_archive = archive_base / "missing"

    # Act & Assert
    with pytest.raises(ArchiveHandlerError, match="Archived ticket not found"):
        ArchiveHandler.restore_ticket(nonexistent_archive, tickets_base)


def test_restore_ticket_already_exists(tmp_path):
    """Test restoring when destination already exists."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"

    archive_folder = archive_base / "feature-auth"
    archive_folder.mkdir(parents=True)

    # Create ticket that already exists
    existing_ticket = tickets_base / "feature-auth"
    existing_ticket.mkdir(parents=True)

    # Act & Assert
    with pytest.raises(ArchiveHandlerError, match="already exists in active tickets"):
        ArchiveHandler.restore_ticket(archive_folder, tickets_base)


def test_restore_ticket_creates_tickets_dir(tmp_path):
    """Test that tickets directory is created if it doesn't exist."""
    # Arrange
    tickets_base = tmp_path / "specs" / "tickets"
    archive_base = tmp_path / "specs" / "archive"

    archive_folder = archive_base / "feature-auth"
    archive_folder.mkdir(parents=True)
    (archive_folder / "spec.yaml").write_text("test")

    # Verify tickets doesn't exist yet
    assert not tickets_base.exists()

    # Act
    result = ArchiveHandler.restore_ticket(archive_folder, tickets_base)

    # Assert
    assert tickets_base.exists()
    assert result.exists()


def test_list_archived_tickets_empty(tmp_path):
    """Test listing archived tickets when archive doesn't exist."""
    # Arrange
    archive_base = tmp_path / "specs" / "archive"

    # Act
    result = ArchiveHandler.list_archived_tickets(archive_base)

    # Assert
    assert result == []


def test_list_archived_tickets_success(tmp_path):
    """Test listing archived tickets successfully."""
    # Arrange
    archive_base = tmp_path / "specs" / "archive"
    archive_base.mkdir(parents=True)

    # Create some archived tickets
    (archive_base / "feature-auth").mkdir()
    (archive_base / "bug-login").mkdir()
    (archive_base / "spike-research").mkdir()

    # Create a file (should be ignored)
    (archive_base / "readme.txt").write_text("test")

    # Act
    result = ArchiveHandler.list_archived_tickets(archive_base)

    # Assert
    assert len(result) == 3
    ticket_names = [p.name for p in result]
    assert "feature-auth" in ticket_names
    assert "bug-login" in ticket_names
    assert "spike-research" in ticket_names
    assert "readme.txt" not in ticket_names  # Files excluded

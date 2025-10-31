"""Tests for init module."""

from pathlib import Path

import pytest
from cddoc.init import (
    InitializationError,
    check_existing_structure,
    create_directory_structure,
    create_minimal_files,
    initialize_project,
    is_dangerous_path,
    validate_path,
)


def test_initialize_project_creates_structure(tmp_path):
    """Test that initialize_project creates all required directories and files."""
    result = initialize_project(str(tmp_path))

    # Check directories
    expected_dirs = [
        "specs",
        "specs/tickets",
        "specs/archive",
        ".claude",
        ".claude/commands",
        ".claude/agents",
        ".claude/skills",
        ".cddoc",
        ".cddoc/templates",
    ]

    for dir_path in expected_dirs:
        assert (
            tmp_path / dir_path
        ).exists(), f"Directory {dir_path} should exist"
        assert (
            tmp_path / dir_path
        ).is_dir(), f"{dir_path} should be a directory"

    # Check files
    expected_files = [
        "CLAUDE.md",
        ".cddoc/config.yaml",
        ".cddoc/templates/feature-ticket-template.yaml",
        ".cddoc/templates/bug-ticket-template.yaml",
        ".cddoc/templates/spike-ticket-template.yaml",
    ]

    for file_path in expected_files:
        assert (
            tmp_path / file_path
        ).exists(), f"File {file_path} should exist"
        assert (
            tmp_path / file_path
        ).is_file(), f"{file_path} should be a file"

    # Verify result structure
    assert result["path"] == tmp_path
    assert len(result["created_dirs"]) == len(expected_dirs)
    assert len(result["created_files"]) == len(expected_files)
    assert result["existing_structure"] is False


def test_claude_md_content(tmp_path):
    """Test CLAUDE.md content is correct."""
    initialize_project(str(tmp_path))

    claude_md = tmp_path / "CLAUDE.md"
    assert claude_md.exists()

    content = claude_md.read_text()
    assert "# Project Constitution" in content
    assert "## Project Overview" in content
    assert "## Architecture & Design Patterns" in content
    assert "## Technology Stack & Constraints" in content
    assert "## Development Standards" in content
    assert "## Team Conventions" in content
    assert "CDD Framework v0.1.0" in content


def test_config_yaml_content(tmp_path):
    """Test config.yaml content is correct."""
    initialize_project(str(tmp_path))

    config_file = tmp_path / ".cddoc" / "config.yaml"
    assert config_file.exists()

    content = config_file.read_text()
    assert "cdd:" in content
    assert 'version: "0.1.0"' in content
    assert "initialized: true" in content
    assert "prefer_git_root: true" in content
    assert 'default_ticket_type: "feature"' in content
    assert "auto_archive: true" in content


def test_initialize_existing_structure(tmp_path):
    """Test that initialization handles existing structure gracefully."""
    # First initialization
    result1 = initialize_project(str(tmp_path))
    assert (
        len(result1["created_files"]) == 5
    )  # CLAUDE.md + config.yaml + 3 templates

    # Second initialization should skip existing files
    result2 = initialize_project(str(tmp_path))
    assert len(result2["created_files"]) == 0
    assert (
        len(result2["skipped_files"]) == 5
    )  # CLAUDE.md + config.yaml + 3 templates
    assert result2["existing_structure"] is True


def test_check_existing_structure_empty(tmp_path):
    """Test check_existing_structure returns False for empty directory."""
    has_structure, existing = check_existing_structure(tmp_path)
    assert has_structure is False
    assert len(existing) == 0


def test_check_existing_structure_with_dirs(tmp_path):
    """Test check_existing_structure detects existing directories."""
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "tickets").mkdir()

    has_structure, existing = check_existing_structure(tmp_path)
    assert has_structure is True
    assert "specs" in existing
    assert "specs/tickets" in existing


def test_check_existing_structure_with_files(tmp_path):
    """Test check_existing_structure detects existing files."""
    (tmp_path / "CLAUDE.md").write_text("test")

    has_structure, existing = check_existing_structure(tmp_path)
    assert has_structure is True
    assert "CLAUDE.md" in existing


def test_create_directory_structure(tmp_path):
    """Test create_directory_structure creates all directories."""
    created = create_directory_structure(tmp_path)

    expected_dirs = [
        "specs",
        "specs/tickets",
        "specs/archive",
        ".claude",
        ".claude/commands",
        ".claude/agents",
        ".claude/skills",
        ".cddoc",
        ".cddoc/templates",
    ]

    assert len(created) == len(expected_dirs)

    for dir_path in expected_dirs:
        assert (tmp_path / dir_path).exists()
        assert (tmp_path / dir_path).is_dir()


def test_create_minimal_files(tmp_path):
    """Test create_minimal_files creates required files."""
    # Create .cddoc directory first
    (tmp_path / ".cddoc").mkdir()
    (tmp_path / ".cddoc" / "templates").mkdir()

    created, skipped = create_minimal_files(tmp_path)

    assert len(created) == 5
    assert "CLAUDE.md" in created
    assert ".cddoc/config.yaml" in created
    assert ".cddoc/templates/feature-ticket-template.yaml" in created
    assert ".cddoc/templates/bug-ticket-template.yaml" in created
    assert ".cddoc/templates/spike-ticket-template.yaml" in created
    assert len(skipped) == 0

    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".cddoc" / "config.yaml").exists()


def test_create_minimal_files_skips_existing(tmp_path):
    """Test create_minimal_files skips existing files."""
    # Create .cddoc directory and files
    (tmp_path / ".cddoc").mkdir()
    (tmp_path / ".cddoc" / "templates").mkdir()
    (tmp_path / "CLAUDE.md").write_text("existing")
    (tmp_path / ".cddoc" / "config.yaml").write_text("existing")
    (
        tmp_path / ".cddoc" / "templates" / "feature-ticket-template.yaml"
    ).write_text("existing")
    (
        tmp_path / ".cddoc" / "templates" / "bug-ticket-template.yaml"
    ).write_text("existing")
    (
        tmp_path / ".cddoc" / "templates" / "spike-ticket-template.yaml"
    ).write_text("existing")

    created, skipped = create_minimal_files(tmp_path)

    assert len(created) == 0
    assert len(skipped) == 5
    assert "CLAUDE.md" in skipped
    assert ".cddoc/config.yaml" in skipped
    assert ".cddoc/templates/feature-ticket-template.yaml" in skipped
    assert ".cddoc/templates/bug-ticket-template.yaml" in skipped
    assert ".cddoc/templates/spike-ticket-template.yaml" in skipped


def test_is_dangerous_path():
    """Test is_dangerous_path correctly identifies dangerous paths."""
    assert is_dangerous_path(Path("/")) is True
    assert is_dangerous_path(Path("/usr")) is True
    assert is_dangerous_path(Path("/etc")) is True
    assert is_dangerous_path(Path.home()) is True
    assert is_dangerous_path(Path("/tmp/safe-test")) is False


def test_validate_path_dangerous(tmp_path):
    """Test validate_path rejects dangerous paths."""
    with pytest.raises(InitializationError, match="system directory"):
        validate_path(Path("/"))

    with pytest.raises(InitializationError, match="system directory"):
        validate_path(Path("/usr"))


def test_validate_path_no_permission(tmp_path):
    """Test validate_path rejects paths without write permission."""
    # Create a directory without write permissions
    no_write = tmp_path / "no-write"
    no_write.mkdir()
    no_write.chmod(0o444)  # Read-only

    try:
        with pytest.raises(InitializationError, match="No write permission"):
            validate_path(no_write)
    finally:
        # Restore permissions for cleanup
        no_write.chmod(0o755)


def test_initialize_nonexistent_directory(tmp_path):
    """Test initialization creates directory if it doesn't exist."""
    new_dir = tmp_path / "new-project"
    assert not new_dir.exists()

    result = initialize_project(str(new_dir))

    assert new_dir.exists()
    assert result["path"] == new_dir


def test_directory_hierarchy_correct(tmp_path):
    """Test that all directories are created in correct hierarchy."""
    initialize_project(str(tmp_path))

    # specs structure
    assert (tmp_path / "specs").is_dir()
    assert (tmp_path / "specs" / "tickets").is_dir()
    assert (tmp_path / "specs" / "archive").is_dir()

    # .claude structure
    assert (tmp_path / ".claude").is_dir()
    assert (tmp_path / ".claude" / "commands").is_dir()
    assert (tmp_path / ".claude" / "agents").is_dir()
    assert (tmp_path / ".claude" / "skills").is_dir()

    # .cddoc structure
    assert (tmp_path / ".cddoc").is_dir()
    assert (tmp_path / ".cddoc" / "templates").is_dir()


def test_files_have_correct_content_structure(tmp_path):
    """Test that created files have proper structure."""
    initialize_project(str(tmp_path))

    # CLAUDE.md should have all sections
    claude_md = tmp_path / "CLAUDE.md"
    content = claude_md.read_text()
    sections = [
        "# Project Constitution",
        "## Project Overview",
        "## Architecture & Design Patterns",
        "## Technology Stack & Constraints",
        "## Development Standards",
        "## Team Conventions",
    ]
    for section in sections:
        assert (
            section in content
        ), f"Section '{section}' missing from CLAUDE.md"

    # config.yaml should have all top-level keys
    config_yaml = tmp_path / ".cddoc" / "config.yaml"
    content = config_yaml.read_text()
    keys = ["cdd:", "project:", "settings:", "features:"]
    for key in keys:
        assert key in content, f"Key '{key}' missing from config.yaml"


def test_initialize_result_format(tmp_path):
    """Test that initialize_project returns correct result format."""
    result = initialize_project(str(tmp_path))

    # Check all expected keys are present
    assert "path" in result
    assert "created_dirs" in result
    assert "created_files" in result
    assert "skipped_files" in result
    assert "existing_structure" in result

    # Check types
    assert isinstance(result["path"], Path)
    assert isinstance(result["created_dirs"], list)
    assert isinstance(result["created_files"], list)
    assert isinstance(result["skipped_files"], list)
    assert isinstance(result["existing_structure"], bool)

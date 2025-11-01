"""Tests for init module."""

from pathlib import Path

import pytest
from cddoc.init import (
    InitializationError,
    check_existing_structure,
    create_directory_structure,
    generate_claude_md,
    initialize_project,
    install_framework_commands,
    install_templates,
    is_dangerous_path,
    validate_path,
)


def test_initialize_project_creates_structure(tmp_path):
    """Test that initialize_project creates all required directories and files."""
    result = initialize_project(str(tmp_path))

    # Check directories (new structure)
    expected_dirs = [
        "specs/tickets",
        "docs/features",
        ".claude/commands",
        ".cdd/templates",
    ]

    for dir_path in expected_dirs:
        full_path = tmp_path / dir_path
        assert full_path.exists(), f"Directory {dir_path} should exist"
        assert full_path.is_dir(), f"{dir_path} should be a directory"

    # Check .gitkeep files
    assert (tmp_path / "specs" / "tickets" / ".gitkeep").exists()
    assert (tmp_path / "docs" / "features" / ".gitkeep").exists()

    # Check CLAUDE.md
    assert (tmp_path / "CLAUDE.md").exists()

    # Check framework commands
    assert (tmp_path / ".claude" / "commands" / "socrates.md").exists()
    assert (tmp_path / ".claude" / "commands" / "plan.md").exists()
    assert (tmp_path / ".claude" / "commands" / "exec.md").exists()
    assert (tmp_path / ".claude" / "commands" / "exec-auto.md").exists()

    # Check templates
    assert (
        tmp_path / ".cdd" / "templates" / "feature-ticket-template.yaml"
    ).exists()
    assert (
        tmp_path / ".cdd" / "templates" / "bug-ticket-template.yaml"
    ).exists()
    assert (
        tmp_path / ".cdd" / "templates" / "spike-ticket-template.yaml"
    ).exists()

    # Verify result structure
    assert result["path"] == tmp_path
    assert len(result["created_dirs"]) > 0
    assert len(result["installed_commands"]) == 4
    assert len(result["installed_templates"]) >= 7
    assert result["claude_md_created"] is True
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


def test_framework_commands_installed(tmp_path):
    """Test that framework commands are properly installed."""
    initialize_project(str(tmp_path))

    commands_dir = tmp_path / ".claude" / "commands"

    # Check all commands exist
    socrates = commands_dir / "socrates.md"
    plan = commands_dir / "plan.md"
    exec_cmd = commands_dir / "exec.md"
    exec_auto = commands_dir / "exec-auto.md"

    assert socrates.exists()
    assert plan.exists()
    assert exec_cmd.exists()
    assert exec_auto.exists()

    # Verify commands have content
    socrates_content = socrates.read_text()
    assert "Socrates" in socrates_content
    assert "CDD FRAMEWORK COMMAND" in socrates_content
    assert len(socrates_content) > 1000  # Should be substantial


def test_templates_installed(tmp_path):
    """Test that templates are properly installed."""
    initialize_project(str(tmp_path))

    templates_dir = tmp_path / ".cdd" / "templates"

    # Check ticket templates
    assert (templates_dir / "feature-ticket-template.yaml").exists()
    assert (templates_dir / "bug-ticket-template.yaml").exists()
    assert (templates_dir / "spike-ticket-template.yaml").exists()

    # Check plan templates
    assert (templates_dir / "feature-plan-template.md").exists()
    assert (templates_dir / "bug-plan-template.md").exists()
    assert (templates_dir / "spike-plan-template.md").exists()

    # Check constitution template
    assert (templates_dir / "constitution-template.md").exists()

    # Check new living doc template
    assert (templates_dir / "feature-doc-template.md").exists()


def test_initialize_existing_structure(tmp_path):
    """Test that initialization handles existing structure gracefully."""
    # First initialization
    result1 = initialize_project(str(tmp_path))
    assert result1["claude_md_created"] is True
    assert len(result1["installed_commands"]) == 4

    # Second initialization should handle existing structure
    result2 = initialize_project(str(tmp_path))
    assert result2["claude_md_created"] is False  # Already exists
    assert result2["existing_structure"] is True


def test_initialize_with_force_flag(tmp_path):
    """Test that force flag overwrites existing files."""
    # First initialization
    initialize_project(str(tmp_path))

    # Modify CLAUDE.md
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("Modified content")

    # Second initialization with force
    result = initialize_project(str(tmp_path), force=True)
    assert result["claude_md_created"] is True

    # Content should be restored from template
    content = claude_md.read_text()
    assert "Modified content" not in content
    assert "# Project Constitution" in content


def test_check_existing_structure_empty(tmp_path):
    """Test check_existing_structure returns False for empty directory."""
    has_structure, existing = check_existing_structure(tmp_path)
    assert has_structure is False
    assert len(existing) == 0


def test_check_existing_structure_with_dirs(tmp_path):
    """Test check_existing_structure detects existing directories."""
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "tickets").mkdir(parents=True)

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
        "specs/tickets",
        "docs/features",
        ".claude/commands",
        ".cdd/templates",
    ]

    # Check all directories were created
    for dir_path in expected_dirs:
        assert (tmp_path / dir_path).exists()
        assert (tmp_path / dir_path).is_dir()

    # Check .gitkeep files
    assert (tmp_path / "specs" / "tickets" / ".gitkeep").exists()
    assert (tmp_path / "docs" / "features" / ".gitkeep").exists()


def test_install_framework_commands(tmp_path):
    """Test install_framework_commands copies all command files."""
    # Create target directory
    commands_dest = tmp_path / ".claude" / "commands"
    commands_dest.mkdir(parents=True)

    # Install commands
    installed = install_framework_commands(tmp_path)

    # Verify all commands installed
    assert len(installed) == 4
    assert ".claude/commands/socrates.md" in installed
    assert ".claude/commands/plan.md" in installed
    assert ".claude/commands/exec.md" in installed
    assert ".claude/commands/exec-auto.md" in installed

    # Verify files exist
    assert (commands_dest / "socrates.md").exists()
    assert (commands_dest / "plan.md").exists()
    assert (commands_dest / "exec.md").exists()
    assert (commands_dest / "exec-auto.md").exists()


def test_install_templates(tmp_path):
    """Test install_templates copies all template files."""
    # Create target directory
    templates_dest = tmp_path / ".cdd" / "templates"
    templates_dest.mkdir(parents=True)

    # Install templates
    installed = install_templates(tmp_path)

    # Should have at least 8 templates (3 ticket + 3 plan + constitution + feature-doc)
    assert len(installed) >= 8

    # Verify key templates exist
    assert (templates_dest / "constitution-template.md").exists()
    assert (templates_dest / "feature-ticket-template.yaml").exists()
    assert (templates_dest / "feature-doc-template.md").exists()


def test_generate_claude_md(tmp_path):
    """Test generate_claude_md creates CLAUDE.md from template."""
    # Create templates directory and template
    templates_dir = tmp_path / ".cdd" / "templates"
    templates_dir.mkdir(parents=True)
    install_templates(tmp_path)

    # Generate CLAUDE.md
    result = generate_claude_md(tmp_path)
    assert result is True

    # Verify file exists and has content
    claude_md = tmp_path / "CLAUDE.md"
    assert claude_md.exists()

    content = claude_md.read_text()
    assert len(content) > 100
    assert "# Project Constitution" in content


def test_generate_claude_md_skip_existing(tmp_path):
    """Test generate_claude_md skips if CLAUDE.md exists."""
    # Create templates directory
    templates_dir = tmp_path / ".cdd" / "templates"
    templates_dir.mkdir(parents=True)
    install_templates(tmp_path)

    # Create existing CLAUDE.md
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("Existing content")

    # Try to generate (should skip)
    result = generate_claude_md(tmp_path, force=False)
    assert result is False

    # Verify content unchanged
    content = claude_md.read_text()
    assert content == "Existing content"


def test_is_dangerous_path():
    """Test is_dangerous_path correctly identifies dangerous paths."""
    assert is_dangerous_path(Path("/")) is True
    assert is_dangerous_path(Path("/usr")) is True
    assert is_dangerous_path(Path("/etc")) is True
    assert is_dangerous_path(Path.home()) is True
    assert is_dangerous_path(Path("/tmp/safe-test")) is False


def test_validate_path_dangerous():
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

    # docs structure (new)
    assert (tmp_path / "docs").is_dir()
    assert (tmp_path / "docs" / "features").is_dir()

    # .claude structure
    assert (tmp_path / ".claude").is_dir()
    assert (tmp_path / ".claude" / "commands").is_dir()

    # .cdd structure (new)
    assert (tmp_path / ".cdd").is_dir()
    assert (tmp_path / ".cdd" / "templates").is_dir()


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


def test_initialize_result_format(tmp_path):
    """Test that initialize_project returns correct result format."""
    result = initialize_project(str(tmp_path))

    # Check all expected keys are present
    assert "path" in result
    assert "created_dirs" in result
    assert "installed_commands" in result
    assert "installed_templates" in result
    assert "claude_md_created" in result
    assert "existing_structure" in result

    # Check types
    assert isinstance(result["path"], Path)
    assert isinstance(result["created_dirs"], list)
    assert isinstance(result["installed_commands"], list)
    assert isinstance(result["installed_templates"], list)
    assert isinstance(result["claude_md_created"], bool)
    assert isinstance(result["existing_structure"], bool)


def test_gitkeep_files_created(tmp_path):
    """Test that .gitkeep files are created in empty directories."""
    initialize_project(str(tmp_path))

    # Check .gitkeep in user workspace directories
    assert (tmp_path / "specs" / "tickets" / ".gitkeep").exists()
    assert (tmp_path / "docs" / "features" / ".gitkeep").exists()

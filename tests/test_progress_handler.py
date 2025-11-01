"""Tests for progress handler."""

from pathlib import Path

import pytest
import yaml

from src.cddoc.handlers.progress_handler import (
    ProgressData,
    ProgressHandler,
    ProgressHandlerError,
)


def test_read_progress_success(tmp_path):
    """Test reading valid progress.yaml file."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    test_data = {
        "plan_path": "specs/tickets/test/plan.md",
        "spec_path": "specs/tickets/test/spec.yaml",
        "started_at": "2025-11-01T10:00:00Z",
        "updated_at": "2025-11-01T11:00:00Z",
        "status": "in_progress",
        "steps": [],
        "acceptance_criteria": [],
        "files_modified": [],
        "files_created": [],
        "issues": [],
    }
    with open(progress_file, "w") as f:
        yaml.safe_dump(test_data, f)

    # Act
    result = ProgressHandler.read_progress(progress_file)

    # Assert
    assert result["plan_path"] == "specs/tickets/test/plan.md"
    assert result["status"] == "in_progress"
    assert isinstance(result["steps"], list)


def test_read_progress_file_not_found(tmp_path):
    """Test reading non-existent progress file."""
    # Arrange
    missing_file = tmp_path / "nonexistent.yaml"

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Progress file not found"):
        ProgressHandler.read_progress(missing_file)


def test_read_progress_malformed_yaml(tmp_path):
    """Test reading malformed YAML file."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    with open(progress_file, "w") as f:
        f.write("invalid: yaml: content: [[[")

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Invalid YAML format"):
        ProgressHandler.read_progress(progress_file)


def test_read_progress_missing_required_field(tmp_path):
    """Test reading progress file with missing required fields."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    incomplete_data = {"plan_path": "test.md"}  # Missing other required fields
    with open(progress_file, "w") as f:
        yaml.safe_dump(incomplete_data, f)

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Missing required field"):
        ProgressHandler.read_progress(progress_file)


def test_write_progress_creates_file(tmp_path):
    """Test writing progress data creates file successfully."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    data: ProgressData = ProgressHandler.initialize_progress(
        plan_path=Path("specs/tickets/test/plan.md"),
        spec_path=Path("specs/tickets/test/spec.yaml"),
    )

    # Act
    ProgressHandler.write_progress(progress_file, data)

    # Assert
    assert progress_file.exists()
    with open(progress_file, "r") as f:
        saved_data = yaml.safe_load(f)
    assert saved_data["plan_path"] == "specs/tickets/test/plan.md"


def test_write_progress_updates_timestamp(tmp_path):
    """Test that write_progress updates the updated_at timestamp."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    data: ProgressData = ProgressHandler.initialize_progress(
        plan_path=Path("specs/tickets/test/plan.md"),
        spec_path=Path("specs/tickets/test/spec.yaml"),
    )
    old_timestamp = data["updated_at"]

    # Act
    import time

    time.sleep(0.01)  # Ensure timestamp difference
    ProgressHandler.write_progress(progress_file, data)

    # Assert
    # Data dict is modified in place
    assert data["updated_at"] != old_timestamp


def test_initialize_progress_creates_correct_structure(tmp_path):
    """Test initialize_progress creates all required fields."""
    # Arrange
    plan_path = tmp_path / "plan.md"
    spec_path = tmp_path / "spec.yaml"

    # Act
    result = ProgressHandler.initialize_progress(plan_path, spec_path)

    # Assert
    assert result["plan_path"] == str(plan_path)
    assert result["spec_path"] == str(spec_path)
    assert result["status"] == "in_progress"
    assert isinstance(result["steps"], list)
    assert isinstance(result["acceptance_criteria"], list)
    assert isinstance(result["files_modified"], list)
    assert isinstance(result["files_created"], list)
    assert isinstance(result["issues"], list)
    assert "started_at" in result
    assert "updated_at" in result

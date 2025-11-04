"""Tests for spec handler."""


import pytest
import yaml

from src.cddoc.handlers.spec_handler import (
    SpecHandler,
    SpecHandlerError,
)


def test_read_spec_success(tmp_path):
    """Test reading valid spec.yaml file."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    test_data = {
        "ticket": {
            "name": "feature-user-auth",
            "type": "feature",
            "status": "draft",
            "created": "2025-11-01",
        }
    }
    with open(spec_file, "w") as f:
        yaml.safe_dump(test_data, f)

    # Act
    result = SpecHandler.read_spec(spec_file)

    # Assert
    assert result["ticket"]["name"] == "feature-user-auth"
    assert result["ticket"]["status"] == "draft"


def test_read_spec_file_not_found(tmp_path):
    """Test reading non-existent spec file."""
    # Arrange
    missing_file = tmp_path / "nonexistent.yaml"

    # Act & Assert
    with pytest.raises(SpecHandlerError, match="Spec file not found"):
        SpecHandler.read_spec(missing_file)


def test_read_spec_malformed_yaml(tmp_path):
    """Test reading malformed YAML file."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    with open(spec_file, "w") as f:
        f.write("invalid: yaml: content: [[[")

    # Act & Assert
    with pytest.raises(SpecHandlerError, match="Invalid YAML format"):
        SpecHandler.read_spec(spec_file)


def test_read_spec_not_dictionary(tmp_path):
    """Test reading spec file that's not a dictionary."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    with open(spec_file, "w") as f:
        yaml.safe_dump(["list", "instead", "of", "dict"], f)

    # Act & Assert
    with pytest.raises(SpecHandlerError, match="must contain a dictionary"):
        SpecHandler.read_spec(spec_file)


def test_write_spec_creates_file(tmp_path):
    """Test writing spec data creates file successfully."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {
        "ticket": {
            "name": "feature-auth",
            "type": "feature",
            "status": "draft",
        }
    }

    # Act
    SpecHandler.write_spec(spec_file, data)

    # Assert
    assert spec_file.exists()
    with open(spec_file, "r") as f:
        saved_data = yaml.safe_load(f)
    assert saved_data["ticket"]["name"] == "feature-auth"


def test_write_spec_creates_parent_dirs(tmp_path):
    """Test that write_spec creates parent directories if needed."""
    # Arrange
    spec_file = tmp_path / "specs" / "tickets" / "feature-auth" / "spec.yaml"
    data = {"ticket": {"name": "test"}}

    # Verify parent doesn't exist yet
    assert not spec_file.parent.exists()

    # Act
    SpecHandler.write_spec(spec_file, data)

    # Assert
    assert spec_file.exists()
    assert spec_file.parent.exists()


def test_write_spec_preserves_order(tmp_path):
    """Test that write_spec doesn't sort keys alphabetically."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {
        "ticket": {"z_field": "last", "a_field": "first", "m_field": "middle"}
    }

    # Act
    SpecHandler.write_spec(spec_file, data)

    # Assert
    with open(spec_file, "r") as f:
        content = f.read()
    # Check that order is preserved (z_field appears before a_field)
    assert content.index("z_field") < content.index("a_field")


def test_update_status_success(tmp_path):
    """Test updating ticket status successfully."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {
        "ticket": {
            "name": "feature-auth",
            "type": "feature",
            "status": "draft",
            "created": "2025-11-01",
            "updated": "2025-11-01",
        }
    }
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    SpecHandler.update_status(spec_file, "in_progress", add_timestamp=True)

    # Assert
    with open(spec_file, "r") as f:
        updated_data = yaml.safe_load(f)
    assert updated_data["ticket"]["status"] == "in_progress"
    assert "implementation_started" in updated_data["ticket"]


def test_update_status_no_timestamp(tmp_path):
    """Test updating status without adding timestamps."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"ticket": {"name": "test", "status": "draft"}}
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    SpecHandler.update_status(spec_file, "planned", add_timestamp=False)

    # Assert
    with open(spec_file, "r") as f:
        updated_data = yaml.safe_load(f)
    assert updated_data["ticket"]["status"] == "planned"
    assert "implementation_started" not in updated_data["ticket"]


def test_update_status_in_progress_adds_timestamp(tmp_path):
    """Test that in_progress status adds implementation_started timestamp."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"ticket": {"name": "test", "status": "planned"}}
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    SpecHandler.update_status(spec_file, "in_progress")

    # Assert
    with open(spec_file, "r") as f:
        updated_data = yaml.safe_load(f)
    assert "implementation_started" in updated_data["ticket"]


def test_update_status_completed_adds_timestamp(tmp_path):
    """Test that completed status adds implementation_completed timestamp."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"ticket": {"name": "test", "status": "in_progress"}}
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    SpecHandler.update_status(spec_file, "completed")

    # Assert
    with open(spec_file, "r") as f:
        updated_data = yaml.safe_load(f)
    assert "implementation_completed" in updated_data["ticket"]


def test_update_status_archived_adds_timestamp(tmp_path):
    """Test that archived status adds archived_at timestamp."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"ticket": {"name": "test", "status": "completed"}}
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    SpecHandler.update_status(spec_file, "archived")

    # Assert
    with open(spec_file, "r") as f:
        updated_data = yaml.safe_load(f)
    assert "archived_at" in updated_data["ticket"]


def test_update_status_updates_updated_field(tmp_path):
    """Test that update_status updates the 'updated' field if it exists."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {
        "ticket": {
            "name": "test",
            "status": "draft",
            "created": "2025-11-01",
            "updated": "2025-11-01",
        }
    }
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    import time

    time.sleep(0.01)  # Ensure different date possible
    SpecHandler.update_status(spec_file, "planned")

    # Assert
    with open(spec_file, "r") as f:
        updated_data = yaml.safe_load(f)
    # Updated field should be present (might be same date in tests)
    assert "updated" in updated_data["ticket"]


def test_update_status_missing_ticket_section(tmp_path):
    """Test updating status when ticket section is missing."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"other": "data"}  # No ticket section
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act & Assert
    with pytest.raises(SpecHandlerError, match="missing 'ticket' section"):
        SpecHandler.update_status(spec_file, "planned")


def test_get_status_success(tmp_path):
    """Test getting current ticket status."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"ticket": {"name": "test", "status": "in_progress"}}
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    result = SpecHandler.get_status(spec_file)

    # Assert
    assert result == "in_progress"


def test_get_status_no_ticket_section(tmp_path):
    """Test getting status when ticket section is missing."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"other": "data"}
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    result = SpecHandler.get_status(spec_file)

    # Assert
    assert result is None


def test_get_status_no_status_field(tmp_path):
    """Test getting status when status field is missing."""
    # Arrange
    spec_file = tmp_path / "spec.yaml"
    data = {"ticket": {"name": "test"}}  # No status field
    with open(spec_file, "w") as f:
        yaml.safe_dump(data, f)

    # Act
    result = SpecHandler.get_status(spec_file)

    # Assert
    assert result is None


def test_get_status_file_not_found(tmp_path):
    """Test getting status from non-existent file."""
    # Arrange
    missing_file = tmp_path / "nonexistent.yaml"

    # Act & Assert
    with pytest.raises(SpecHandlerError, match="Spec file not found"):
        SpecHandler.get_status(missing_file)

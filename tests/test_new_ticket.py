"""Tests for new_ticket module."""

from datetime import datetime
from unittest.mock import patch

import pytest
from cddoc.new_ticket import (
    TicketCreationError,
    check_ticket_exists,
    create_new_ticket,
    create_ticket_file,
    get_git_root,
    get_template_path,
    normalize_ticket_name,
    populate_template_dates,
)


class TestNormalizeTicketName:
    """Test name normalization logic."""

    def test_lowercase_conversion(self):
        """Test that names are converted to lowercase."""
        assert normalize_ticket_name("UserAuth") == "userauth"
        assert normalize_ticket_name("FEATURE") == "feature"

    def test_spaces_to_dashes(self):
        """Test that spaces are converted to dashes."""
        assert normalize_ticket_name("User Auth System") == "user-auth-system"
        assert normalize_ticket_name("My Feature") == "my-feature"

    def test_underscores_to_dashes(self):
        """Test that underscores are converted to dashes."""
        assert (
            normalize_ticket_name("payment_processing") == "payment-processing"
        )
        assert normalize_ticket_name("user_auth_system") == "user-auth-system"

    def test_special_chars_removed(self):
        """Test that special characters are converted to dashes."""
        assert normalize_ticket_name("feature@name!") == "feature-name"
        assert normalize_ticket_name("user#auth$system") == "user-auth-system"

    def test_duplicate_dashes_removed(self):
        """Test that consecutive dashes are deduplicated."""
        assert normalize_ticket_name("feature--name") == "feature-name"
        assert normalize_ticket_name("user---auth") == "user-auth"
        assert normalize_ticket_name("a__b__c") == "a-b-c"

    def test_leading_trailing_dashes_stripped(self):
        """Test that leading and trailing dashes are removed."""
        assert normalize_ticket_name("  feature  ") == "feature"
        assert normalize_ticket_name("--feature--") == "feature"
        assert normalize_ticket_name("_feature_") == "feature"

    def test_complex_normalization(self):
        """Test complex real-world examples."""
        assert normalize_ticket_name("User Auth System!") == "user-auth-system"
        assert (
            normalize_ticket_name("  Payment__Processing  ")
            == "payment-processing"
        )
        assert (
            normalize_ticket_name("Feature #123: New API")
            == "feature-123-new-api"
        )

    def test_already_normalized(self):
        """Test that already-normalized names pass through."""
        assert normalize_ticket_name("user-auth") == "user-auth"
        assert normalize_ticket_name("feature-name") == "feature-name"

    def test_empty_after_normalization(self):
        """Test names that become empty after normalization."""
        assert normalize_ticket_name("!!!") == ""
        assert normalize_ticket_name("___") == ""
        assert normalize_ticket_name("   ") == ""


class TestGetGitRoot:
    """Test git root detection."""

    def test_not_in_git_repo(self, tmp_path, monkeypatch):
        """Test error when not in a git repository."""
        monkeypatch.chdir(tmp_path)

        with pytest.raises(TicketCreationError, match="Not a git repository"):
            get_git_root()

    def test_git_not_installed(self, monkeypatch):
        """Test error when git is not installed."""
        # Mock subprocess to raise FileNotFoundError
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(TicketCreationError, match="Git not found"):
                get_git_root()

    def test_valid_git_repo(self, tmp_path):
        """Test successful git root detection."""
        # Initialize git repo
        import subprocess

        subprocess.run(
            ["git", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        # Change to subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        # Mock current working directory
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = str(tmp_path) + "\n"
            mock_run.return_value.returncode = 0

            result = get_git_root()
            assert result == tmp_path


class TestGetTemplatePath:
    """Test template path resolution."""

    def test_template_exists(self, tmp_path):
        """Test when template file exists."""
        # Create template
        templates_dir = tmp_path / ".cddoc" / "templates"
        templates_dir.mkdir(parents=True)
        template_file = templates_dir / "feature-ticket-template.yaml"
        template_file.write_text("test")

        result = get_template_path(tmp_path, "feature")
        assert result == template_file
        assert result.exists()

    def test_template_missing(self, tmp_path):
        """Test error when template doesn't exist."""
        with pytest.raises(TicketCreationError, match="Template not found"):
            get_template_path(tmp_path, "feature")

    def test_all_ticket_types(self, tmp_path):
        """Test all three ticket types."""
        templates_dir = tmp_path / ".cddoc" / "templates"
        templates_dir.mkdir(parents=True)

        for ticket_type in ["feature", "bug", "spike"]:
            template_file = (
                templates_dir / f"{ticket_type}-ticket-template.yaml"
            )
            template_file.write_text("test")

            result = get_template_path(tmp_path, ticket_type)
            assert result.exists()


class TestPopulateTemplateDates:
    """Test date population in templates."""

    def test_replaces_auto_generated(self):
        """Test that [auto-generated] is replaced with date."""
        template = """created: [auto-generated]
updated: [auto-generated]"""

        result = populate_template_dates(template)

        # Should not contain placeholder anymore
        assert "[auto-generated]" not in result

        # Should contain current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        assert current_date in result
        assert result.count(current_date) == 2

    def test_preserves_other_content(self):
        """Test that other content is preserved."""
        template = """title: "Test"
created: [auto-generated]
other_field: "value"
updated: [auto-generated]"""

        result = populate_template_dates(template)

        assert 'title: "Test"' in result
        assert 'other_field: "value"' in result

    def test_no_placeholders(self):
        """Test template with no placeholders."""
        template = """title: "Test"
created: 2025-01-01"""

        result = populate_template_dates(template)
        assert result == template


class TestCheckTicketExists:
    """Test ticket existence checking."""

    def test_ticket_exists(self, tmp_path):
        """Test when ticket directory exists."""
        ticket_path = tmp_path / "feature-test"
        ticket_path.mkdir()

        assert check_ticket_exists(ticket_path) is True

    def test_ticket_not_exists(self, tmp_path):
        """Test when ticket directory doesn't exist."""
        ticket_path = tmp_path / "feature-test"

        assert check_ticket_exists(ticket_path) is False


class TestCreateTicketFile:
    """Test ticket file creation."""

    def test_creates_directory_and_file(self, tmp_path):
        """Test that directory and spec.yaml are created."""
        ticket_path = tmp_path / "feature-test"
        template_path = tmp_path / "template.yaml"
        template_path.write_text("created: [auto-generated]")

        create_ticket_file(ticket_path, template_path)

        assert ticket_path.exists()
        assert ticket_path.is_dir()
        assert (ticket_path / "spec.yaml").exists()

    def test_populates_dates(self, tmp_path):
        """Test that dates are populated in created file."""
        ticket_path = tmp_path / "feature-test"
        template_path = tmp_path / "template.yaml"
        template_path.write_text(
            "created: [auto-generated]\nupdated: [auto-generated]"
        )

        create_ticket_file(ticket_path, template_path)

        content = (ticket_path / "spec.yaml").read_text()
        assert "[auto-generated]" not in content

        current_date = datetime.now().strftime("%Y-%m-%d")
        assert current_date in content

    def test_overwrites_existing(self, tmp_path):
        """Test that existing files are overwritten."""
        ticket_path = tmp_path / "feature-test"
        ticket_path.mkdir()
        spec_file = ticket_path / "spec.yaml"
        spec_file.write_text("old content")

        template_path = tmp_path / "template.yaml"
        template_path.write_text("new content")

        create_ticket_file(ticket_path, template_path)

        content = spec_file.read_text()
        assert "new content" in content
        assert "old content" not in content


class TestCreateNewTicket:
    """Test main ticket creation function (integration tests)."""

    def test_successful_creation(self, tmp_path, monkeypatch):
        """Test successful ticket creation flow."""
        # Setup git repo
        import subprocess

        subprocess.run(
            ["git", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        # Create template
        templates_dir = tmp_path / ".cddoc" / "templates"
        templates_dir.mkdir(parents=True)
        template_file = templates_dir / "feature-ticket-template.yaml"
        template_file.write_text("created: [auto-generated]")

        # Change to temp directory so get_git_root returns tmp_path
        monkeypatch.chdir(tmp_path)

        # Create ticket
        result = create_new_ticket("feature", "User Auth System")

        # Verify result
        assert result["ticket_type"] == "feature"
        assert result["normalized_name"] == "user-auth-system"
        assert result["overwritten"] is False

        # Verify file exists
        ticket_path = result["ticket_path"]
        assert ticket_path.exists()
        assert (ticket_path / "spec.yaml").exists()

        # Verify path structure
        assert "feature-user-auth-system" in str(ticket_path)
        assert "specs/tickets" in str(ticket_path)

    def test_invalid_name_all_special_chars(self, tmp_path):
        """Test error when name becomes empty after normalization."""
        # Setup git repo
        import subprocess

        subprocess.run(
            ["git", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        with pytest.raises(TicketCreationError, match="Invalid ticket name"):
            create_new_ticket("feature", "!!!")

    def test_not_in_git_repo(self, tmp_path, monkeypatch):
        """Test error when not in git repository."""
        monkeypatch.chdir(tmp_path)

        with pytest.raises(TicketCreationError, match="Not a git repository"):
            create_new_ticket("feature", "test")

    def test_missing_template(self, tmp_path, monkeypatch):
        """Test error when template doesn't exist."""
        # Setup git repo
        import subprocess

        subprocess.run(
            ["git", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        # Change to temp directory so get_git_root returns tmp_path
        monkeypatch.chdir(tmp_path)

        with pytest.raises(TicketCreationError, match="Template not found"):
            create_new_ticket("feature", "test")


class TestIntegrationScenarios:
    """Integration tests for complete scenarios."""

    def test_all_ticket_types(self, tmp_path, monkeypatch):
        """Test creating all three ticket types."""
        # Setup
        import subprocess

        subprocess.run(
            ["git", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        templates_dir = tmp_path / ".cddoc" / "templates"
        templates_dir.mkdir(parents=True)

        for ticket_type in ["feature", "bug", "spike"]:
            template_file = (
                templates_dir / f"{ticket_type}-ticket-template.yaml"
            )
            template_file.write_text(
                f"type: {ticket_type}\ncreated: [auto-generated]"
            )

        # Change to temp directory so get_git_root returns tmp_path
        monkeypatch.chdir(tmp_path)

        # Create tickets
        for ticket_type in ["feature", "bug", "spike"]:
            result = create_new_ticket(ticket_type, f"test-{ticket_type}")

            assert result["ticket_type"] == ticket_type
            assert result["ticket_path"].exists()
            assert (result["ticket_path"] / "spec.yaml").exists()

    def test_name_normalization_variations(self, tmp_path, monkeypatch):
        """Test various name formats are normalized correctly."""
        # Setup
        import subprocess

        subprocess.run(
            ["git", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        templates_dir = tmp_path / ".cddoc" / "templates"
        templates_dir.mkdir(parents=True)
        template_file = templates_dir / "feature-ticket-template.yaml"
        template_file.write_text("test")

        # Change to temp directory so get_git_root returns tmp_path
        monkeypatch.chdir(tmp_path)

        test_cases = [
            ("User Auth", "user-auth"),
            ("payment_processing", "payment-processing"),
            ("Feature #123", "feature-123"),
            ("  Spaced  Name  ", "spaced-name"),
        ]

        for input_name, expected_normalized in test_cases:
            result = create_new_ticket("feature", input_name)
            assert result["normalized_name"] == expected_normalized

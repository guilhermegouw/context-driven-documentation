"""Tests for Socrates conversation-driven documentation assistant."""

import tempfile
from pathlib import Path

import pytest
import yaml

from cddoc.handlers import ConstitutionHandler, TicketSpecHandler
from cddoc.socrates import SocratesError, create_file_handler


class TestFileHandlerCreation:
    """Test file handler creation and detection."""

    def test_create_handler_for_claude_md(self):
        """Should create ConstitutionHandler for CLAUDE.md files."""
        path = Path("CLAUDE.md")
        handler = create_file_handler(path)
        assert isinstance(handler, ConstitutionHandler)

    def test_create_handler_for_ticket_yaml(self):
        """Should create TicketSpecHandler for ticket YAML files."""
        path = Path("specs/tickets/feature-123/spec.yaml")
        handler = create_file_handler(path)
        assert isinstance(handler, TicketSpecHandler)

    def test_create_handler_for_ticket_yml(self):
        """Should create TicketSpecHandler for ticket YML files."""
        path = Path("specs/tickets/bug-fix/spec.yml")
        handler = create_file_handler(path)
        assert isinstance(handler, TicketSpecHandler)

    def test_unsupported_file_type_raises_error(self):
        """Should raise SocratesError for unsupported file types."""
        path = Path("random-file.txt")
        with pytest.raises(SocratesError) as exc_info:
            create_file_handler(path)
        assert "Unsupported file type" in str(exc_info.value)

    def test_command_file_not_yet_supported(self):
        """Should raise error for command files (not yet implemented)."""
        path = Path(".claude/commands/test.md")
        with pytest.raises(SocratesError) as exc_info:
            create_file_handler(path)
        assert "not yet supported" in str(exc_info.value)


class TestTicketSpecHandler:
    """Test TicketSpecHandler functionality."""

    def test_detect_feature_ticket_from_path(self):
        """Should detect feature ticket type from path."""
        handler = TicketSpecHandler()
        path = Path("specs/tickets/feature-auth/spec.yaml")
        content = {}

        ticket_type = handler.detect_ticket_type(path, content)
        assert ticket_type == "feature"

    def test_detect_bug_ticket_from_path(self):
        """Should detect bug ticket type from path."""
        handler = TicketSpecHandler()
        path = Path("specs/tickets/bug-login/spec.yaml")
        content = {}

        ticket_type = handler.detect_ticket_type(path, content)
        assert ticket_type == "bug"

    def test_detect_spike_ticket_from_path(self):
        """Should detect spike ticket type from path."""
        handler = TicketSpecHandler()
        path = Path("specs/tickets/spike-research/spec.yaml")
        content = {}

        ticket_type = handler.detect_ticket_type(path, content)
        assert ticket_type == "spike"

    def test_detect_ticket_type_from_content(self):
        """Should prioritize ticket type from existing content."""
        handler = TicketSpecHandler()
        path = Path("specs/tickets/something/spec.yaml")
        content = {"ticket": {"type": "bug"}}

        ticket_type = handler.detect_ticket_type(path, content)
        assert ticket_type == "bug"

    def test_read_existing_yaml_content(self):
        """Should read and parse existing YAML file."""
        handler = TicketSpecHandler()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create path with 'tickets' in it to avoid prompting
            tickets_dir = Path(tmpdir) / "specs" / "tickets" / "feature-test"
            tickets_dir.mkdir(parents=True)
            temp_path = tickets_dir / "spec.yaml"

            yaml_content = {
                "title": "Test Feature",
                "user_story": "As a user...",
                "ticket": {"type": "feature"},
            }

            with open(temp_path, 'w') as f:
                yaml.dump(yaml_content, f)

            file_data = handler.read_current_content(temp_path)

            assert file_data['content']['title'] == "Test Feature"
            assert file_data['is_new'] is False
            assert file_data['ticket_type'] == 'feature'

    def test_read_nonexistent_file(self):
        """Should handle non-existent file gracefully."""
        handler = TicketSpecHandler()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tickets" / "new-feature" / "spec.yaml"

            file_data = handler.read_current_content(path)

            assert file_data['content'] == {}
            assert file_data['is_new'] is True
            assert 'ticket_type' in file_data

    def test_update_file_creates_valid_yaml(self):
        """Should create valid YAML with proper structure."""
        handler = TicketSpecHandler()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "spec.yaml"

            conversation_data = {
                'content': {
                    'title': 'Test Feature',
                    'user_story': 'As a user, I want...',
                },
                'updates': [
                    {
                        'section': 'title',
                        'action': 'Added',
                        'preview': 'Test Feature',
                    }
                ],
                'ticket_type': 'feature',
            }

            results = handler.update_file(path, conversation_data)

            assert path.exists()
            assert results['file_path'] == str(path)
            assert len(results['updates']) > 0
            assert len(results['next_steps']) > 0

            # Verify YAML is valid
            with open(path, 'r') as f:
                saved_content = yaml.safe_load(f)
                assert saved_content['title'] == 'Test Feature'
                assert saved_content['ticket']['type'] == 'feature'
                assert 'created' in saved_content['ticket']
                assert 'updated' in saved_content['ticket']


class TestConstitutionHandler:
    """Test ConstitutionHandler functionality."""

    def test_parse_markdown_sections(self):
        """Should parse markdown content into sections."""
        handler = ConstitutionHandler()

        markdown = """# Project Constitution

## Project Overview
This is the overview section.
It has multiple lines.

## Technology Stack & Constraints
Tech stack details here.
"""

        sections = handler.parse_markdown_sections(markdown)

        assert "Project Overview" in sections
        assert "Technology Stack & Constraints" in sections
        assert "multiple lines" in sections["Project Overview"]

    def test_read_existing_constitution(self):
        """Should read existing CLAUDE.md file."""
        handler = ConstitutionHandler()

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.md', delete=False
        ) as f:
            # Write more than 100 characters to be considered "not new"
            content = """# Project Constitution

## Project Overview
This is a test project with enough content to not be considered new.
It has multiple lines and sections to properly test the constitution handler.

## Technology Stack & Constraints
Python, Click, Rich, PyYAML
"""
            f.write(content)
            temp_path = Path(f.name)

        try:
            file_data = handler.read_current_content(temp_path)

            assert file_data['is_new'] is False
            assert "Project Overview" in file_data['sections']
            assert "Technology Stack & Constraints" in file_data['sections']
        finally:
            temp_path.unlink()

    def test_read_empty_constitution(self):
        """Should detect empty constitution as new."""
        handler = ConstitutionHandler()

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.md', delete=False
        ) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            file_data = handler.read_current_content(temp_path)

            assert file_data['is_new'] is True
            assert file_data['sections'] == {}
        finally:
            temp_path.unlink()

    def test_update_file_creates_valid_markdown(self):
        """Should create valid markdown with proper structure."""
        handler = ConstitutionHandler()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "CLAUDE.md"

            conversation_data = {
                'sections': {
                    'Project Overview': 'Test project overview',
                    'Technology Stack & Constraints': 'Python, Click, Rich',
                },
                'updates': [
                    {
                        'section': 'Project Overview',
                        'action': 'Added',
                        'preview': 'Test project',
                    }
                ],
            }

            results = handler.update_file(path, conversation_data)

            assert path.exists()
            assert results['file_path'] == str(path)
            assert len(results['next_steps']) > 0

            # Verify markdown structure
            content = path.read_text()
            assert "# Project Constitution" in content
            assert "## Project Overview" in content
            assert "Test project overview" in content
            assert "## Technology Stack & Constraints" in content

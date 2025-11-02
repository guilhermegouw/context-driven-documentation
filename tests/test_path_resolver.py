"""Unit tests for PathResolver."""

from pathlib import Path
from unittest.mock import patch

import pytest
from cddoc.path_resolver import PathResolutionError, PathResolver


class TestPathResolverBasicResolution:
    """Test basic path resolution functionality."""

    def test_resolve_shorthand_to_spec_yaml(self):
        """Test shorthand resolves to spec.yaml."""
        with patch.object(Path, "exists", return_value=True):
            result = PathResolver.resolve("feature-user-auth", "spec.yaml")
            assert result == Path("specs/tickets/feature-user-auth/spec.yaml")

    def test_resolve_shorthand_to_plan_md(self):
        """Test shorthand resolves to plan.md."""
        with patch.object(Path, "exists", return_value=True):
            result = PathResolver.resolve("feature-user-auth", "plan.md")
            assert result == Path("specs/tickets/feature-user-auth/plan.md")

    def test_resolve_different_target_files(self):
        """Test same ticket name with different target files."""
        with patch.object(Path, "exists", return_value=True):
            spec_result = PathResolver.resolve("bug-fix", "spec.yaml")
            plan_result = PathResolver.resolve("bug-fix", "plan.md")

            assert spec_result == Path("specs/tickets/bug-fix/spec.yaml")
            assert plan_result == Path("specs/tickets/bug-fix/plan.md")


class TestPathResolverExplicitPaths:
    """Test explicit path passthrough."""

    def test_resolve_explicit_relative_path(self):
        """Test paths with / are used as-is."""
        result = PathResolver.resolve(
            "specs/tickets/feature-x/spec.yaml", "spec.yaml"
        )
        assert result == Path("specs/tickets/feature-x/spec.yaml")

    def test_resolve_explicit_absolute_path(self):
        """Test absolute paths are preserved."""
        abs_path = "/home/user/project/specs/tickets/bug/spec.yaml"
        result = PathResolver.resolve(abs_path, "spec.yaml")
        assert result == Path(abs_path)

    def test_resolve_file_with_md_extension(self):
        """Test files ending in .md are used as-is."""
        result = PathResolver.resolve("CLAUDE.md", "spec.yaml")
        assert result == Path("CLAUDE.md")

    def test_resolve_file_with_yaml_extension(self):
        """Test files ending in .yaml are used as-is."""
        result = PathResolver.resolve("custom-config.yaml", "spec.yaml")
        assert result == Path("custom-config.yaml")

    def test_resolve_non_ticket_path(self):
        """Test non-ticket file paths work."""
        result = PathResolver.resolve("docs/features/auth.md", "spec.yaml")
        assert result == Path("docs/features/auth.md")


class TestPathResolverTicketNotFound:
    """Test error handling when ticket doesn't exist."""

    def test_resolve_nonexistent_ticket_raises_error(self):
        """Test PathResolutionError raised when ticket not found."""
        with patch.object(Path, "exists", return_value=False):
            with patch.object(
                PathResolver, "find_similar_tickets", return_value=[]
            ):
                with pytest.raises(PathResolutionError) as exc_info:
                    PathResolver.resolve("nonexistent-ticket", "spec.yaml")

                assert "nonexistent-ticket" in str(exc_info.value)

    def test_error_includes_ticket_name(self):
        """Test error message includes the ticket that wasn't found."""
        with patch.object(Path, "exists", return_value=False):
            with patch.object(
                PathResolver, "find_similar_tickets", return_value=[]
            ):
                with pytest.raises(PathResolutionError) as exc_info:
                    PathResolver.resolve("my-missing-ticket", "spec.yaml")

                error_msg = str(exc_info.value)
                assert "my-missing-ticket" in error_msg
                assert "Ticket not found" in error_msg


class TestFindSimilarTickets:
    """Test fuzzy matching for ticket suggestions."""

    def test_find_similar_tickets_returns_matches(self, tmp_path):
        """Test fuzzy matching finds similar tickets."""
        # Create mock ticket directories
        tickets_dir = tmp_path / "specs" / "tickets"
        tickets_dir.mkdir(parents=True)
        (tickets_dir / "feature-auth").mkdir()
        (tickets_dir / "feature-authentication").mkdir()
        (tickets_dir / "bug-payment").mkdir()

        with patch.object(PathResolver, "TICKETS_DIR", tickets_dir):
            similar = PathResolver.find_similar_tickets("feat-auth")

            # Should find similar tickets
            assert (
                "feature-auth" in similar
                or "feature-authentication" in similar
            )
            # Should not include unrelated tickets
            assert "bug-payment" not in similar

    def test_find_similar_tickets_max_three(self, tmp_path):
        """Test only top 3 suggestions returned."""
        tickets_dir = tmp_path / "specs" / "tickets"
        tickets_dir.mkdir(parents=True)
        (tickets_dir / "feature-auth").mkdir()
        (tickets_dir / "feature-auth-v2").mkdir()
        (tickets_dir / "feature-authentication").mkdir()
        (tickets_dir / "feature-authorize").mkdir()
        (tickets_dir / "feature-auth-system").mkdir()

        with patch.object(PathResolver, "TICKETS_DIR", tickets_dir):
            similar = PathResolver.find_similar_tickets("feature-auth")

            # Should return maximum 3 suggestions
            assert len(similar) <= PathResolver.MAX_SUGGESTIONS

    def test_find_similar_tickets_empty_dir(self, tmp_path):
        """Test handles empty tickets directory."""
        tickets_dir = tmp_path / "specs" / "tickets"
        tickets_dir.mkdir(parents=True)

        with patch.object(PathResolver, "TICKETS_DIR", tickets_dir):
            similar = PathResolver.find_similar_tickets("any-ticket")

            assert similar == []

    def test_find_similar_tickets_nonexistent_dir(self):
        """Test handles nonexistent tickets directory."""
        nonexistent = Path("/nonexistent/path/tickets")

        with patch.object(PathResolver, "TICKETS_DIR", nonexistent):
            similar = PathResolver.find_similar_tickets("any-ticket")

            assert similar == []

    def test_find_similar_tickets_threshold(self, tmp_path):
        """Test similarity threshold filters matches."""
        tickets_dir = tmp_path / "specs" / "tickets"
        tickets_dir.mkdir(parents=True)
        (tickets_dir / "feature-user-auth").mkdir()
        (tickets_dir / "completely-different").mkdir()

        with patch.object(PathResolver, "TICKETS_DIR", tickets_dir):
            # Should find similar (feature-user-auth is similar to feat-auth)
            similar = PathResolver.find_similar_tickets("feat-auth")

            # Should not include tickets below similarity threshold
            assert "completely-different" not in similar


class TestFormatNotFoundError:
    """Test error message formatting."""

    def test_format_error_with_suggestions(self):
        """Test error message includes suggestions."""
        error = PathResolver.format_not_found_error(
            "my-feature",
            ["feature-my-feature", "enhancement-my-features"],
            "socrates",
        )

        assert "my-feature" in error
        assert "feature-my-feature" in error
        assert "/socrates feature-my-feature" in error
        assert "enhancement-my-features" in error

    def test_format_error_without_suggestions(self):
        """Test error message when no suggestions available."""
        error = PathResolver.format_not_found_error("my-feature", [], "plan")

        assert "my-feature" in error
        assert "No existing tickets" in error
        assert "cdd new" in error

    def test_format_error_different_commands(self):
        """Test error adapts to different commands."""
        error_socrates = PathResolver.format_not_found_error(
            "ticket", ["feature-ticket"], "socrates"
        )
        error_plan = PathResolver.format_not_found_error(
            "ticket", ["feature-ticket"], "plan"
        )

        assert "/socrates feature-ticket" in error_socrates
        assert "/plan feature-ticket" in error_plan

    def test_format_error_create_suggestion(self):
        """Test error includes create suggestions."""
        error = PathResolver.format_not_found_error(
            "new-ticket", [], "socrates"
        )

        assert "cdd new feature new-ticket" in error
        assert "cdd new enhancement new-ticket" in error
        assert "cdd new bug new-ticket" in error


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_resolve_empty_argument(self):
        """Test handling of empty string argument."""
        with patch.object(Path, "exists", return_value=False):
            with patch.object(
                PathResolver, "find_similar_tickets", return_value=[]
            ):
                with pytest.raises(PathResolutionError):
                    PathResolver.resolve("", "spec.yaml")

    def test_resolve_ticket_with_dashes(self):
        """Test tickets with multiple dashes."""
        with patch.object(Path, "exists", return_value=True):
            result = PathResolver.resolve("feature-user-auth-v2", "spec.yaml")
            assert result == Path(
                "specs/tickets/feature-user-auth-v2/spec.yaml"
            )

    def test_resolve_ticket_with_numbers(self):
        """Test tickets with numbers."""
        with patch.object(Path, "exists", return_value=True):
            result = PathResolver.resolve("bug-123-fix", "spec.yaml")
            assert result == Path("specs/tickets/bug-123-fix/spec.yaml")

    def test_resolve_path_with_multiple_slashes(self):
        """Test paths with multiple directory levels."""
        result = PathResolver.resolve(
            "docs/guides/getting-started.md", "spec.yaml"
        )
        assert result == Path("docs/guides/getting-started.md")

    def test_find_similar_ignores_hidden_dirs(self, tmp_path):
        """Test hidden directories (starting with .) are ignored."""
        tickets_dir = tmp_path / "specs" / "tickets"
        tickets_dir.mkdir(parents=True)
        (tickets_dir / "feature-auth").mkdir()
        (tickets_dir / ".hidden-ticket").mkdir()

        with patch.object(PathResolver, "TICKETS_DIR", tickets_dir):
            similar = PathResolver.find_similar_tickets("hidden")

            # Should not include hidden directories
            assert ".hidden-ticket" not in similar

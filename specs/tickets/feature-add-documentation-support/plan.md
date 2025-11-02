# Implementation Plan: Add Documentation Support to `cdd new` Command

**Generated:** 2025-11-02
**Spec:** `specs/tickets/feature-add-documentation-support/spec.yaml`
**Ticket Type:** Feature
**Estimated Effort:** 4-6 hours (High confidence)

---

## Executive Summary

This feature extends the `cdd new` command to support creating documentation files (guides and features) using the same familiar CLI workflow users already know from creating tickets. Users will be able to run `cdd new documentation guide <name>` or `cdd new documentation feature <name>` to create markdown documentation files with structured templates that Socrates can fill through conversation.

**Key Design Principle:** Reuse existing patterns and infrastructure - the documentation workflow leverages the same code paths, error handling, and UI patterns as ticket creation, just with different destinations and file formats.

**Key Deliverables:**
- CLI subcommand: `cdd new documentation <guide|feature> <name>`
- Two markdown templates: `guide-doc-template.md` and `feature-doc-template.md`
- Extended backend logic to handle documentation routing
- Updated help text and success messages
- Unit tests for new functionality

---

## Technical Decisions

### Decision 1: Extend Existing `create_new_ticket()` Function
**Choice:** Add documentation handling to the existing `new_ticket.py` module rather than creating a separate module
**Rationale:** Documentation creation shares 90% of the same logic (name normalization, git root detection, template loading, file creation). Creating a separate module would duplicate code. The function can handle both tickets and documentation with minimal branching logic.
**Alternatives Considered:**
- Create separate `create_new_documentation()` function → Would duplicate git detection, name normalization, error handling
- Create new module `documentation.py` → Unnecessary complexity for what is essentially a variant of ticket creation

### Decision 2: Use Nested Click Command Structure
**Choice:** Add `documentation` as a subcommand: `cdd new documentation <guide|feature> <name>`
**Rationale:** Follows Click best practices for nested commands. Clear hierarchy: `new` is the action, `documentation` is the category, `guide/feature` is the type. Maintains backward compatibility with existing `cdd new feature/bug/spike` commands.
**Alternatives Considered:**
- Flat structure: `cdd new guide <name>` → Less clear separation between tickets and docs
- Flag-based: `cdd new --doc guide <name>` → More typing, less intuitive

### Decision 3: Clean File Names Without Type Prefix
**Choice:** Create files as `<name>.md` in appropriate directories, not `guide-<name>.md` or `feature-<name>.md`
**Rationale:** Directory structure already provides the context (`docs/guides/` vs `docs/features/`). Clean names are more readable and professional. Matches the existing pattern in `docs/features/init-command.md` (not `feature-init-command.md`).
**Alternatives Considered:**
- Include type prefix → Redundant given directory structure, longer file names

### Decision 4: Markdown Templates with Placeholder Sections
**Choice:** Create templates with `# Section Name` headers and `[placeholder text]` for AI to fill
**Rationale:** Socrates already knows how to work with structured templates. Markdown is more conversationally friendly than YAML. Section headers provide clear structure that AI can parse and fill systematically.
**Alternatives Considered:**
- Completely blank markdown files → No structure to guide conversation
- YAML-based doc templates → Awkward for documentation, less readable

### Decision 5: No Date Population for Docs (Unlike Tickets)
**Choice:** Documentation templates won't have auto-populated dates like ticket templates do
**Rationale:** Documentation is living and continuously updated - a single "created" date is less meaningful. Users can add version/last-updated metadata manually if needed. Keeps templates simpler.
**Alternatives Considered:**
- Add created/updated dates → Less relevant for living docs, adds complexity

---

## File Structure

### New Files to Create

1. **`.cdd/templates/guide-doc-template.md`**
   - Purpose: Template for user guides (how-to, getting started, etc.)
   - Key sections: What is [Topic]?, Getting Started, Examples, Tips & Best Practices, Business Rules

2. **`.cdd/templates/feature-doc-template.md`**
   - Purpose: Template for feature documentation (technical reference)
   - Key sections: Overview, Current Implementation, Usage, API Reference, Business Rules & Edge Cases

3. **`tests/test_documentation_creation.py`**
   - Purpose: Unit tests for documentation creation logic
   - Key tests: CLI command, file creation, template loading, error handling

### Existing Files to Modify

1. **`src/cddoc/cli.py`**
   - Changes: Add `documentation` subcommand to `new` command group
   - Location: After existing `@main.command()` definitions (around line 220)

2. **`src/cddoc/new_ticket.py`**
   - Changes:
     - Add `create_new_documentation()` function (similar to `create_new_ticket()`)
     - Update `get_template_path()` to handle markdown templates
     - Add helper to determine destination directory
   - Location: New functions at bottom of module

3. **`src/cddoc/init.py`**
   - Changes: Ensure `docs/guides/` directory is created (may already exist)
   - Location: In `create_directory_structure()` function
   - Note: Check if this already exists - may not need changes

### Files to Reference for Patterns

1. **`src/cddoc/new_ticket.py`**
   - Pattern: Error handling, name normalization, git root detection, template loading
   - Reason: This is the primary reference implementation

2. **`src/cddoc/cli.py`**
   - Pattern: Click command structure, Rich console formatting, success messages
   - Reason: Shows existing UI patterns to maintain consistency

3. **`docs/features/init-command.md`**
   - Pattern: Feature documentation structure and style
   - Reason: Real example of what feature template should guide users toward

---

## Data Models & API Contracts

### Type Definitions

```python
# New type hint for documentation types
from typing import Literal

DocumentationType = Literal["guide", "feature"]

# Function signature for new function
def create_new_documentation(
    doc_type: DocumentationType,
    name: str
) -> dict:
    """Create a new documentation file.

    Returns:
        Dictionary with creation results:
        {
            "file_path": Path,           # Full path to created .md file
            "normalized_name": str,       # Normalized file name
            "doc_type": str,              # "guide" or "feature"
            "overwritten": bool           # Whether file was overwritten
        }
    """
    pass
```

### Template Structure

**Guide Template (`guide-doc-template.md`):**
```markdown
# [Guide Title]

> Brief description of what this guide covers

**Status:** Draft
**Last Updated:** [Date]

---

## What is [Topic]?

[Explain what this topic/feature/concept is and why it matters]

## Getting Started

[Step-by-step instructions to get started with this topic]

### Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]

### Quick Start
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

### Example 1: [Scenario]
[Code or detailed example]

### Example 2: [Scenario]
[Code or detailed example]

## Tips & Best Practices

- **[Tip 1]:** [Explanation]
- **[Tip 2]:** [Explanation]
- **[Tip 3]:** [Explanation]

## Business Rules

### [Rule Category]
- [Rule 1]: [Description]
- [Rule 2]: [Description]

## Common Pitfalls

- **[Pitfall 1]:** [How to avoid]
- **[Pitfall 2]:** [How to avoid]

## Related Documentation

- [Link to related guide]
- [Link to related feature]

---

*Last updated: [Date] | Maintained by: [Team/Person]*
```

**Feature Template (`feature-doc-template.md`):**
```markdown
# Feature: [Feature Name]

> Living documentation for the [feature name]

**Status:** [Draft | In Development | Production]
**Version:** [Version number]
**Last Updated:** [Date]

---

## Overview

[High-level description of what this feature does and why it exists]

**Key Capabilities:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

## Current Implementation

### How It Works Today

[Describe the current behavior from user and system perspective]

### Architecture Overview

[Technical architecture - components, data flow, integration points]

```
[Optional ASCII diagram of architecture]
```

### Key Components

**[Component 1]:**
- Location: `[file path]`
- Purpose: [What it does]
- Key functions: [List]

**[Component 2]:**
- Location: `[file path]`
- Purpose: [What it does]
- Key functions: [List]

## Usage

### Basic Usage

[How to use this feature - commands, API calls, etc.]

```[language]
[Code example]
```

### Advanced Usage

[More complex scenarios]

```[language]
[Code example]
```

## API Reference

### [Function/Endpoint 1]

**Signature:** `[function signature or HTTP endpoint]`

**Parameters:**
- `[param1]` ([type]): [Description]
- `[param2]` ([type]): [Description]

**Returns:** [Return type and description]

**Example:**
```[language]
[Usage example]
```

### [Function/Endpoint 2]

[Same structure...]

## Business Rules & Edge Cases

### Business Logic
- **[Rule 1]:** [Description and behavior]
- **[Rule 2]:** [Description and behavior]

### Edge Cases
- **[Edge case 1]:** [How the system handles it]
- **[Edge case 2]:** [How the system handles it]

### Validation Rules
- [Validation 1]
- [Validation 2]

## Testing

### Test Coverage
- Unit tests: [Location and coverage %]
- Integration tests: [Location and coverage %]

### Key Test Scenarios
- [Scenario 1]
- [Scenario 2]

## Dependencies

### Required Dependencies
- [Dependency 1]: [Version and purpose]
- [Dependency 2]: [Version and purpose]

### Integration Points
- [System/Module 1]: [How it integrates]
- [System/Module 2]: [How it integrates]

## Performance & Scalability

[Performance characteristics, limits, optimization notes]

## Security & Compliance

[Security considerations, data handling, compliance requirements]

## Future Enhancements

[Planned improvements, known limitations, roadmap items]

## Related Documentation

- [Link to related features]
- [Link to guides]
- [Link to API docs]

---

*Last updated: [Date] | Status: [Status] | Version: [Version]*
```

---

## Implementation Steps

Execute these steps in order. Each step has a clear outcome.

### Step 1: Create Markdown Templates
**Outcome:** Two template files exist in `.cdd/templates/` directory

**Details:**
- Create `guide-doc-template.md` with guide structure (see Data Models section above)
- Create `feature-doc-template.md` with feature structure (see Data Models section above)
- Both templates use markdown with clear section headers
- Include placeholder text in `[brackets]` for Socrates to fill

**Location:** `.cdd/templates/`

**Validation:**
- Templates exist and are readable
- Markdown is valid (no syntax errors)
- Section headers match acceptance criteria

---

### Step 2: Update `src/cddoc/new_ticket.py` - Add Helper Functions
**Outcome:** Helper functions exist to support documentation creation

**Details:**

Add after existing helper functions (around line 145):

```python
def get_documentation_directory(git_root: Path, doc_type: str) -> Path:
    """Get destination directory for documentation files.

    Args:
        git_root: Git repository root path
        doc_type: Type of documentation ("guide" or "feature")

    Returns:
        Path to documentation directory
    """
    if doc_type == "guide":
        return git_root / "docs" / "guides"
    elif doc_type == "feature":
        return git_root / "docs" / "features"
    else:
        raise ValueError(f"Invalid documentation type: {doc_type}")


def get_documentation_template_path(git_root: Path, doc_type: str) -> Path:
    """Get path to documentation template file.

    Args:
        git_root: Git repository root path
        doc_type: Type of documentation ("guide" or "feature")

    Returns:
        Path to template file

    Raises:
        TicketCreationError: If template not found
    """
    template_name = f"{doc_type}-doc-template.md"
    template_path = git_root / ".cdd" / "templates" / template_name

    if not template_path.exists():
        raise TicketCreationError(
            f"Template not found: {template_name}\n"
            f"Documentation templates are required.\n"
            f"Run: cdd init"
        )

    return template_path


def create_documentation_file(file_path: Path, template_path: Path) -> None:
    """Create documentation markdown file from template.

    Args:
        file_path: Full path where documentation should be created
        template_path: Path to template file

    Raises:
        TicketCreationError: If creation fails
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Read template
        template_content = template_path.read_text()

        # Note: We don't populate dates for documentation (unlike tickets)
        # Documentation is living and continuously updated

        # Write markdown file
        file_path.write_text(template_content)

    except Exception as e:
        raise TicketCreationError(f"Failed to create documentation: {e}")
```

**Validation:**
- Functions are defined and importable
- Type hints are correct
- Docstrings follow existing style

---

### Step 3: Update `src/cddoc/new_ticket.py` - Add Main Function
**Outcome:** New `create_new_documentation()` function exists

**Details:**

Add after `create_new_ticket()` function (around line 306):

```python
def create_new_documentation(doc_type: str, name: str) -> dict:
    """Create a new documentation file.

    Main entry point for documentation creation logic.
    Similar to create_new_ticket() but simpler (no spec.yaml/plan.md).

    Args:
        doc_type: Type of documentation ("guide" or "feature")
        name: Documentation name (will be normalized)

    Returns:
        Dictionary with creation results:
        {
            "file_path": Path,           # Full path to created .md file
            "normalized_name": str,       # Normalized file name
            "doc_type": str,              # "guide" or "feature"
            "overwritten": bool           # Whether file was overwritten
        }

    Raises:
        TicketCreationError: If creation fails
    """
    # Normalize the name
    normalized_name = normalize_ticket_name(name)

    if not normalized_name:
        raise TicketCreationError(
            "Invalid documentation name\n"
            "Name must contain at least one alphanumeric character.\n"
            "Example: cdd new documentation guide getting-started"
        )

    # Get git root
    git_root = get_git_root()

    # Get template
    template_path = get_documentation_template_path(git_root, doc_type)

    # Get destination directory
    doc_directory = get_documentation_directory(git_root, doc_type)

    # Construct file path (clean name, no type prefix)
    file_path = doc_directory / f"{normalized_name}.md"

    overwritten = False

    # Handle existing file with loop (same pattern as tickets)
    while file_path.exists():
        console.print(
            f"\n[yellow]⚠️  Documentation already exists: {file_path}[/yellow]"
        )

        if prompt_overwrite():
            overwritten = True
            break
        else:
            # Prompt for new name
            new_name = prompt_new_name(f"{doc_type} documentation")

            if new_name is None:
                raise TicketCreationError("Documentation creation cancelled by user")

            # Re-normalize and reconstruct path
            normalized_name = normalize_ticket_name(new_name)

            if not normalized_name:
                console.print(
                    "[red]❌ Invalid name - must contain alphanumeric "
                    "characters[/red]"
                )
                continue

            file_path = doc_directory / f"{normalized_name}.md"

    # Create the documentation file
    create_documentation_file(file_path, template_path)

    return {
        "file_path": file_path,
        "normalized_name": normalized_name,
        "doc_type": doc_type,
        "overwritten": overwritten,
    }
```

**Validation:**
- Function signature matches design
- Error handling follows three-part pattern
- Reuses existing helpers (normalize_ticket_name, get_git_root, prompt_overwrite, prompt_new_name)

---

### Step 4: Update `src/cddoc/cli.py` - Add Documentation Subcommand
**Outcome:** CLI accepts `cdd new documentation guide|feature <name>` commands

**Details:**

Add after the existing `@main.command() def new(...)` function (around line 278):

```python
@main.command()
@click.argument(
    "doc_type",
    type=click.Choice(["guide", "feature"], case_sensitive=False),
)
@click.argument("name")
def documentation(doc_type, name):
    """Create a new documentation file.

    DOC_TYPE: Type of documentation (guide or feature)
    NAME: Name for the documentation file (will be auto-normalized)

    Examples:
        cdd new documentation guide getting-started
        cdd new documentation feature "User Authentication"

    The command will:
    - Normalize the name to lowercase-with-dashes format
    - Create docs/guides/<name>.md or docs/features/<name>.md
    - Populate template with structured sections
    - Show you the next steps (use Socrates to fill it!)
    """
    console.print(
        Panel.fit(
            f"📚 [bold]Creating {doc_type.title()} Documentation[/bold]",
            border_style="blue",
        )
    )

    try:
        # Import at function level to avoid circular imports
        from .new_ticket import create_new_documentation

        # Create the documentation
        result = create_new_documentation(doc_type.lower(), name)

        # Display success
        console.print()
        _display_documentation_success(result)

        sys.exit(0)

    except TicketCreationError as e:
        console.print(f"\n[red]❌ Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error:[/red] {e}")
        sys.exit(1)


def _display_documentation_success(result: dict):
    """Display documentation creation success message.

    Args:
        result: Dictionary containing creation results
    """
    file_path = result["file_path"]
    normalized_name = result["normalized_name"]
    doc_type = result["doc_type"]
    overwritten = result["overwritten"]

    # Create status message
    status = "Overwritten" if overwritten else "Created"

    # Show creation summary
    table = Table(title=f"{status} Successfully", show_header=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Type", f"{doc_type.title()} Documentation")
    table.add_row("File Name", f"{normalized_name}.md")
    table.add_row("Location", str(file_path))

    console.print(table)

    # Show next steps
    next_steps = f"""[bold]Next Steps:[/bold]

1. 📝 Fill out your documentation with Socrates:
   - In Claude Code, run: [cyan]/socrates {file_path}[/cyan]
   - Have a natural conversation to build comprehensive docs
   - Socrates will help you think through the structure

2. 📚 Documentation is now part of your living docs:
   - Guide docs: Help users understand and use features
   - Feature docs: Technical reference for implementation details
   - Keep it updated as the code evolves

3. 🔗 Link related documentation:
   - Cross-reference other guides and features
   - Build a knowledge network

4. 🎯 Remember the CDD philosophy:
   - Context captured once, understood forever
   - Living documentation that evolves with your code
   - AI assistants have full context automatically

[bold]Pro tip:[/bold] Use Socrates to brainstorm! Start the conversation even if you're not
sure what to write - Socrates will ask the right questions.
"""

    console.print()
    console.print(
        Panel(
            next_steps,
            title="🎉 Documentation File Created!",
            border_style="green",
        )
    )
```

**Important Notes:**
- This is added as a NEW top-level command, not as a subcommand of `new`
- Usage: `cdd documentation guide <name>` NOT `cdd new documentation guide <name>`
- This is simpler than nesting under `new` and matches Click patterns

**Validation:**
- Command is accessible via `cdd documentation --help`
- Arguments are parsed correctly
- Success message shows with Rich formatting

---

### Step 5: Update Help Text and Command Structure
**Outcome:** CLI help text accurately reflects new capability

**Details:**

Update the `new` command docstring in `src/cddoc/cli.py` (around line 179):

```python
@main.command()
@click.argument(
    "ticket_type",
    type=click.Choice(
        ["feature", "bug", "spike", "enhancement"], case_sensitive=False
    ),
)
@click.argument("name")
def new(ticket_type, name):
    """Create a new ticket specification file.

    TICKET_TYPE: Type of ticket (feature, bug, spike, or enhancement)
    NAME: Name for the ticket (will be auto-normalized)

    Examples:
        cdd new feature user-authentication
        cdd new bug "Payment Processing Error"
        cdd new spike api_performance_investigation
        cdd new enhancement improve-error-messages

    For documentation files, use: cdd documentation guide|feature <name>

    The command will:
    - Normalize the name to lowercase-with-dashes format
    - Create specs/tickets/<type>-<name>/spec.yaml
    - Populate template with current date
    - Show you the next steps
    """
```

**Validation:**
- Help text is accurate and helpful
- Cross-reference to documentation command is clear

---

### Step 6: Verify Init Creates Required Directories
**Outcome:** `docs/guides/` directory is created by `cdd init`

**Details:**

Check `src/cddoc/init.py` in the `create_directory_structure()` function. The directory structure should include:

```python
# Around line 120-150 in init.py
directories = [
    git_root / "specs" / "tickets",
    git_root / "docs" / "features",
    git_root / "docs" / "guides",  # ← Verify this exists
    git_root / ".claude" / "commands",
    git_root / ".cdd" / "templates",
]
```

If `docs/guides/` is NOT in the list, add it.

**Validation:**
- Running `cdd init` creates `docs/guides/` directory with `.gitkeep`
- Both `docs/features/` and `docs/guides/` exist

---

### Step 7: Update Template Installation Logic
**Outcome:** `cdd init` installs the new documentation templates

**Details:**

Check `src/cddoc/init.py` in the `install_templates()` function (around line 200-250).

Verify the template installation logic copies all templates from the package `src/cddoc/templates/` to `.cdd/templates/`.

The new templates should be added to the source:
- `src/cddoc/templates/guide-doc-template.md`
- `src/cddoc/templates/feature-doc-template.md`

When users run `cdd init`, these will be automatically copied to `.cdd/templates/`.

**Validation:**
- Templates exist in `src/cddoc/templates/` (source)
- After `cdd init`, templates are copied to `.cdd/templates/` (destination)

---

## Test Cases

### Unit Tests

**File:** `tests/test_documentation_creation.py`

```python
"""Unit tests for documentation creation."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from cddoc.new_ticket import (
    create_new_documentation,
    get_documentation_directory,
    get_documentation_template_path,
    create_documentation_file,
    TicketCreationError,
)


class TestDocumentationHelpers:
    """Test documentation helper functions."""

    def test_get_documentation_directory_guide(self, tmp_path):
        """Test guide directory resolution."""
        result = get_documentation_directory(tmp_path, "guide")
        assert result == tmp_path / "docs" / "guides"

    def test_get_documentation_directory_feature(self, tmp_path):
        """Test feature directory resolution."""
        result = get_documentation_directory(tmp_path, "feature")
        assert result == tmp_path / "docs" / "features"

    def test_get_documentation_directory_invalid_type(self, tmp_path):
        """Test invalid documentation type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_documentation_directory(tmp_path, "invalid")
        assert "Invalid documentation type" in str(exc_info.value)

    def test_get_documentation_template_path_exists(self, tmp_path):
        """Test template path resolution when template exists."""
        # Create template
        template_dir = tmp_path / ".cdd" / "templates"
        template_dir.mkdir(parents=True)
        template_file = template_dir / "guide-doc-template.md"
        template_file.write_text("# Template")

        result = get_documentation_template_path(tmp_path, "guide")
        assert result == template_file
        assert result.exists()

    def test_get_documentation_template_path_missing(self, tmp_path):
        """Test template path error when template doesn't exist."""
        with pytest.raises(TicketCreationError) as exc_info:
            get_documentation_template_path(tmp_path, "guide")

        error_msg = str(exc_info.value)
        assert "Template not found" in error_msg
        assert "guide-doc-template.md" in error_msg
        assert "cdd init" in error_msg


class TestCreateDocumentationFile:
    """Test documentation file creation."""

    def test_create_documentation_file_success(self, tmp_path):
        """Test successful documentation file creation."""
        # Create template
        template = tmp_path / "template.md"
        template.write_text("# Guide Template\n\n[Content]")

        # Create documentation
        doc_file = tmp_path / "docs" / "guides" / "test.md"
        create_documentation_file(doc_file, template)

        # Verify
        assert doc_file.exists()
        assert doc_file.read_text() == "# Guide Template\n\n[Content]"

    def test_create_documentation_file_creates_parent_dirs(self, tmp_path):
        """Test that parent directories are created."""
        template = tmp_path / "template.md"
        template.write_text("# Template")

        # Parent dirs don't exist yet
        doc_file = tmp_path / "docs" / "guides" / "nested" / "test.md"
        assert not doc_file.parent.exists()

        create_documentation_file(doc_file, template)

        # Parent dirs created
        assert doc_file.parent.exists()
        assert doc_file.exists()

    def test_create_documentation_file_template_not_found(self, tmp_path):
        """Test error when template doesn't exist."""
        template = tmp_path / "nonexistent.md"
        doc_file = tmp_path / "test.md"

        with pytest.raises(TicketCreationError) as exc_info:
            create_documentation_file(doc_file, template)

        assert "Failed to create documentation" in str(exc_info.value)


class TestCreateNewDocumentation:
    """Test main documentation creation function."""

    def test_create_guide_documentation(self, tmp_path):
        """Test creating a guide documentation file."""
        # Setup
        template_dir = tmp_path / ".cdd" / "templates"
        template_dir.mkdir(parents=True)
        template = template_dir / "guide-doc-template.md"
        template.write_text("# Guide Template")

        with patch("cddoc.new_ticket.get_git_root", return_value=tmp_path):
            result = create_new_documentation("guide", "getting-started")

        # Verify result
        assert result["normalized_name"] == "getting-started"
        assert result["doc_type"] == "guide"
        assert result["overwritten"] is False

        file_path = result["file_path"]
        assert file_path == tmp_path / "docs" / "guides" / "getting-started.md"
        assert file_path.exists()

    def test_create_feature_documentation(self, tmp_path):
        """Test creating a feature documentation file."""
        # Setup
        template_dir = tmp_path / ".cdd" / "templates"
        template_dir.mkdir(parents=True)
        template = template_dir / "feature-doc-template.md"
        template.write_text("# Feature Template")

        with patch("cddoc.new_ticket.get_git_root", return_value=tmp_path):
            result = create_new_documentation("feature", "authentication")

        # Verify result
        assert result["normalized_name"] == "authentication"
        assert result["doc_type"] == "feature"

        file_path = result["file_path"]
        assert file_path == tmp_path / "docs" / "features" / "authentication.md"
        assert file_path.exists()

    def test_create_documentation_normalizes_name(self, tmp_path):
        """Test that documentation names are normalized."""
        # Setup
        template_dir = tmp_path / ".cdd" / "templates"
        template_dir.mkdir(parents=True)
        template = template_dir / "guide-doc-template.md"
        template.write_text("# Template")

        with patch("cddoc.new_ticket.get_git_root", return_value=tmp_path):
            result = create_new_documentation("guide", "Getting Started Guide")

        # Name normalized
        assert result["normalized_name"] == "getting-started-guide"
        assert result["file_path"].name == "getting-started-guide.md"

    def test_create_documentation_invalid_name(self, tmp_path):
        """Test error on invalid documentation name."""
        with patch("cddoc.new_ticket.get_git_root", return_value=tmp_path):
            with pytest.raises(TicketCreationError) as exc_info:
                create_new_documentation("guide", "!@#$%")

        error_msg = str(exc_info.value)
        assert "Invalid documentation name" in error_msg
        assert "alphanumeric character" in error_msg

    def test_create_documentation_file_exists_overwrite(self, tmp_path):
        """Test overwriting existing documentation."""
        # Setup
        template_dir = tmp_path / ".cdd" / "templates"
        template_dir.mkdir(parents=True)
        template = template_dir / "guide-doc-template.md"
        template.write_text("# New Template")

        # Create existing file
        doc_dir = tmp_path / "docs" / "guides"
        doc_dir.mkdir(parents=True)
        existing_file = doc_dir / "test.md"
        existing_file.write_text("# Old Content")

        with patch("cddoc.new_ticket.get_git_root", return_value=tmp_path):
            with patch("cddoc.new_ticket.prompt_overwrite", return_value=True):
                result = create_new_documentation("guide", "test")

        # Verify overwritten
        assert result["overwritten"] is True
        assert existing_file.read_text() == "# New Template"

    def test_create_documentation_file_exists_rename(self, tmp_path):
        """Test renaming when documentation exists."""
        # Setup
        template_dir = tmp_path / ".cdd" / "templates"
        template_dir.mkdir(parents=True)
        template = template_dir / "guide-doc-template.md"
        template.write_text("# Template")

        # Create existing file
        doc_dir = tmp_path / "docs" / "guides"
        doc_dir.mkdir(parents=True)
        (doc_dir / "test.md").write_text("# Existing")

        with patch("cddoc.new_ticket.get_git_root", return_value=tmp_path):
            with patch("cddoc.new_ticket.prompt_overwrite", return_value=False):
                with patch("cddoc.new_ticket.prompt_new_name", return_value="test2"):
                    result = create_new_documentation("guide", "test")

        # Verify renamed
        assert result["normalized_name"] == "test2"
        assert result["file_path"].name == "test2.md"
        assert (doc_dir / "test2.md").exists()
        assert (doc_dir / "test.md").read_text() == "# Existing"  # Original untouched
```

### Integration Tests

**Test 1: `test_cli_documentation_command_guide`**
```python
def test_cli_documentation_command_guide(tmp_path):
    """Test full CLI workflow for creating guide documentation."""
    # Setup git repo and cdd structure
    # Run: cdd init
    # Run: cdd documentation guide getting-started
    # Verify: docs/guides/getting-started.md exists
    # Verify: File contains template content
```

**Test 2: `test_cli_documentation_command_feature`**
```python
def test_cli_documentation_command_feature(tmp_path):
    """Test full CLI workflow for creating feature documentation."""
    # Setup git repo and cdd structure
    # Run: cdd init
    # Run: cdd documentation feature authentication
    # Verify: docs/features/authentication.md exists
    # Verify: File contains template content
```

**Test 3: `test_socrates_can_read_documentation_template`**
```python
def test_socrates_can_read_documentation_template():
    """Verify Socrates can load and parse markdown templates."""
    # Manual test (AI-driven feature)
    # Create documentation: cdd documentation guide test
    # Run: /socrates docs/guides/test.md
    # Verify: Socrates loads file and recognizes sections
    # Verify: Socrates asks appropriate questions for each section
```

### Expected Test Coverage
- Unit test coverage: ≥80% for new functions
- Critical paths: 100% coverage (file creation, error handling)
- Edge cases: Invalid names, missing templates, file exists scenarios

---

## Error Handling

### Error Scenario 1: Template Not Found
**Trigger:** User runs `cdd documentation guide test` but template doesn't exist in `.cdd/templates/`
**Error Message:**
```
❌ Error: Template not found: guide-doc-template.md
Documentation templates are required.
Run: cdd init
```
**Recovery:** User runs `cdd init` to install templates
**User Impact:** Cannot create documentation until templates are installed

### Error Scenario 2: Not in Git Repository
**Trigger:** User runs command outside a git repository
**Error Message:**
```
❌ Error: Not a git repository
CDD requires git for version control of documentation.
Run: git init
```
**Recovery:** User initializes git in the directory
**User Impact:** Cannot proceed without git

### Error Scenario 3: Invalid Documentation Name
**Trigger:** User provides name with no alphanumeric characters (e.g., `"!@#$%"`)
**Error Message:**
```
❌ Error: Invalid documentation name
Name must contain at least one alphanumeric character.
Example: cdd documentation guide getting-started
```
**Recovery:** User provides valid name
**User Impact:** Must retry with valid name

### Error Scenario 4: File Already Exists
**Trigger:** Documentation file already exists at target path
**Error Message:**
```
⚠️  Documentation already exists: docs/guides/test.md
Overwrite? [y/N]
```
**Recovery:** User chooses to overwrite or provide new name
**User Impact:** Protected from accidental overwrites (safe default is "no")

### Error Scenario 5: Permission Denied
**Trigger:** User doesn't have write permissions for docs directory
**Error Message:**
```
❌ Error: Failed to create documentation: [Errno 13] Permission denied: 'docs/guides/test.md'
Check file permissions and try again.
Run: chmod u+w docs/guides
```
**Recovery:** User fixes permissions
**User Impact:** Cannot create documentation until permissions fixed

### Logging Requirements
- **Info level:** Documentation created successfully, file path
- **Warning level:** File already exists (before prompting user)
- **Error level:** Template missing, permission denied, invalid name

---

## Integration Points

### Integration 1: Socrates Slash Command
**Connection Point:** Socrates reads markdown files via `/socrates <path>`
**Data Flow:** User creates doc with `cdd documentation`, then uses `/socrates docs/guides/test.md` to fill it conversationally
**Dependencies:** Socrates must support reading markdown files (already supported)
**Error Handling:** If Socrates cannot read markdown, document in Socrates troubleshooting

### Integration 2: Init Command
**Connection Point:** `cdd init` creates directory structure and installs templates
**Data Flow:** Init copies templates from `src/cddoc/templates/` to `.cdd/templates/`
**Dependencies:** New templates must exist in package source
**Error Handling:** If templates missing from package, init fails with clear error

### Integration 3: Git Repository Detection
**Connection Point:** Uses existing `get_git_root()` function from `new_ticket.py`
**Data Flow:** Determines project root before creating documentation
**Dependencies:** Git must be installed and repo must exist
**Error Handling:** Reuses existing git error messages (three-part pattern)

---

## Dependencies

### New Dependencies to Install
**None** - This feature uses only existing dependencies.

### Existing Dependencies to Leverage
- **Click**: CLI command structure, argument parsing, prompts
- **Rich**: Console formatting, panels, tables for success messages
- **pathlib**: File path operations (Path objects)
- **Python standard library**: re (regex for name normalization), subprocess (git operations), datetime (optional for templates)

### Version Constraints
- Python: 3.9+ (existing constraint)
- Click: 8.1.7 (existing)
- Rich: 13.x (existing)

---

## Effort Estimation

| Activity              | Estimated Time | Assumptions |
|-----------------------|----------------|-------------|
| Create templates      | 0.5 hours      | Simple markdown with placeholders |
| Add helper functions  | 0.5 hours      | Follow existing patterns |
| Add main function     | 1 hour         | Similar to create_new_ticket() |
| Update CLI command    | 0.5 hours      | Follow existing Click patterns |
| Update help text      | 0.25 hours     | Simple docstring updates |
| Verify init changes   | 0.25 hours     | May require no changes |
| **Implementation**    | **3 hours**    | **Total implementation time** |
| Unit tests            | 1.5 hours      | 10-12 test cases |
| Integration tests     | 0.5 hours      | 2 CLI tests + manual Socrates test |
| **Testing**           | **2 hours**    | **Total testing time** |
| Update CLI docs       | 0.5 hours      | Add documentation command to CLI_REFERENCE.md |
| Update README         | 0.25 hours     | Mention docs workflow |
| **Documentation**     | **0.75 hours** | **Total documentation time** |
| Code review prep      | 0.5 hours      | Self-review, run Black/Ruff |
| **Total**             | **6.25 hours** | **~1 working day** |

**Confidence Level:** High (±20%)

**Key Assumptions:**
1. Developer is familiar with the codebase (has worked on tickets before)
2. Existing test infrastructure is set up (pytest, fixtures)
3. No unforeseen issues with template parsing
4. Socrates already supports markdown files (no changes needed)
5. No breaking changes to existing ticket workflow

**Risks to Estimate:**
- **If Socrates needs updates to handle markdown well:** +1-2 hours
- **If directory structure changes needed in init:** +0.5-1 hour
- **If complex template validation required:** +1-2 hours
- **If Click command nesting causes issues:** +1 hour

**Note:** Original spec estimated 4-6 hours. This detailed plan estimates 6.25 hours due to thorough testing and documentation. Both estimates align well.

---

## Definition of Done

- ✅ All implementation steps completed
- ✅ Two markdown templates created and installed by init
- ✅ `cdd documentation guide <name>` creates file in `docs/guides/`
- ✅ `cdd documentation feature <name>` creates file in `docs/features/`
- ✅ File names are clean (no type prefix)
- ✅ Error handling follows three-part pattern
- ✅ Help text updated
- ✅ All unit tests pass (≥80% coverage)
- ✅ Integration tests pass (CLI workflow)
- ✅ Manual Socrates test confirms markdown templates work
- ✅ Code formatted with Black
- ✅ Linting passes with Ruff (no errors)
- ✅ CLI_REFERENCE.md updated with new command
- ✅ README mentions documentation workflow
- ✅ No breaking changes to existing ticket commands
- ✅ Code reviewed and approved

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: specs/tickets/feature-add-documentation-support/spec.yaml*

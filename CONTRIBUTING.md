# Contributing to CDD

Thank you for your interest in contributing to Context-Driven Documentation (CDD)! We're building the future of AI-assisted development, and we welcome contributions from the community.

This guide will help you get started with contributing to CDD.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)
- [Communication](#communication)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on what's best for the project and community
- Accept constructive criticism gracefully
- Show empathy toward other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information without consent
- Other conduct that would be inappropriate in a professional setting

**If you experience or witness unacceptable behavior, please report it by opening a GitHub issue or emailing guilherme.gouw@gmail.com**

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. **Check existing issues** - Your bug may already be reported
2. **Try the latest version** - The bug may already be fixed
3. **Gather details** - Collect reproduction steps and environment information

**Creating a good bug report:**

```markdown
**Description:**
Clear description of what's wrong

**Steps to Reproduce:**
1. Run `cdd init`
2. Execute `cdd new feature test`
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- CDD version: 0.1.0
- Python version: 3.11.5
- OS: Ubuntu 22.04
- Git version: 2.40.0

**Additional Context:**
Any relevant logs, screenshots, or details
```

### Suggesting Features

We love feature suggestions! Before submitting:

1. **Check the roadmap** - See if it's already planned
2. **Search existing issues** - Someone may have suggested it already
3. **Consider the scope** - Does it align with CDD's vision?

**Creating a good feature request:**

```markdown
**Problem Statement:**
What problem does this solve?

**Proposed Solution:**
How would this feature work?

**Alternatives Considered:**
What other approaches did you think about?

**Use Cases:**
Who would use this? When? Why?

**Additional Context:**
Mockups, examples, related features
```

### Contributing Code

We welcome code contributions! Here are areas where you can help:

**Good First Issues:**
- Documentation improvements
- Test coverage improvements
- Bug fixes
- Small feature enhancements

**Medium Complexity:**
- New ticket types
- Template improvements
- CLI enhancements
- New slash commands

**Advanced:**
- Architecture improvements
- Performance optimizations
- New core features

**Look for issues labeled:**
- `good first issue` - Great for newcomers
- `help wanted` - We'd love contributions here
- `documentation` - Docs improvements needed

---

## Development Setup

### Prerequisites

Ensure you have:
- **Python 3.9 or higher**
- **Git**
- **Poetry** (for dependency management)

### Installing Poetry

If you don't have Poetry installed:

```bash
# Linux, macOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -

# Or via pip
pip install poetry
```

### Clone the Repository

```bash
git clone https://github.com/guilhermegouw/context-driven-documentation.git
cd context-driven-documentation
```

### Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
poetry install

# Activate the virtual environment
poetry shell
```

### Verify Installation

```bash
# Run tests
poetry run pytest

# Check code formatting
poetry run black --check .

# Run linter
poetry run ruff check .

# Test CLI
poetry run cdd --version
```

If all commands succeed, you're ready to develop!

---

## Development Workflow

### 1. Create a Feature Branch

Always work on a feature branch, never directly on `main`:

```bash
# Create and checkout new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test improvements
- `refactor/` - Code refactoring

### 2. Make Your Changes

Follow the code standards (see below) and write tests for your changes.

### 3. Run Quality Checks

Before committing, ensure your code passes all quality gates:

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=cddoc --cov-report=term-missing
```

**All checks must pass before submitting a PR.**

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for enhancement ticket type"
```

**Commit message format:**

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/updates
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting)
- `chore:` - Build process, dependencies

**Examples:**

```bash
# Good
git commit -m "feat: add /sync-docs command for documentation synchronization"
git commit -m "fix: handle missing templates gracefully in cdd new"
git commit -m "docs: add troubleshooting section to GETTING_STARTED.md"

# Less clear
git commit -m "updates"
git commit -m "fix bug"
```

### 5. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a pull request on GitHub
```

---

## Code Standards

### Code Style

We use **Black** for automatic code formatting and **Ruff** for linting.

**Configuration:**
- Line length: 79 characters
- Python version: 3.9+

**Format your code:**
```bash
poetry run black .
```

**Check linting:**
```bash
poetry run ruff check .
```

### Type Hints

Use type hints throughout your code:

```python
# Good
def create_ticket(ticket_type: str, name: str) -> Path:
    """Create a new ticket directory."""
    ...

# Avoid
def create_ticket(ticket_type, name):
    ...
```

### Docstrings

Use clear docstrings for public APIs:

```python
def normalize_name(name: str) -> str:
    """
    Normalize ticket/documentation name to lowercase-with-dashes format.

    Args:
        name: Raw name input (may contain spaces, underscores, mixed case)

    Returns:
        Normalized name (lowercase, dashes only)

    Examples:
        >>> normalize_name("User Authentication")
        'user-authentication'
        >>> normalize_name("API_Performance")
        'api-performance'
    """
    ...
```

### Error Handling

Follow the **minimal with context** philosophy:

```python
# Good - three-part error pattern
if not git_root:
    console.print("[red]Error:[/red] Not a git repository")
    console.print("CDD requires git for version control.")
    console.print("Run: [cyan]git init[/cyan]")
    sys.exit(1)

# Avoid - too terse
raise Exception("Not git repo")

# Avoid - too verbose
raise Exception(
    "This directory does not appear to be a git repository. "
    "CDD requires git because it uses version control to track "
    "documentation changes over time. Git provides many benefits..."
)
```

### File Organization

- Keep files focused and single-purpose
- Use handlers for different file types
- Separate concerns (CLI, handlers, utilities)

---

## Testing Guidelines

### Test Coverage

We aim for **high test coverage** of critical functionality.

**What needs tests:**
- ✅ CLI commands (cdd init, cdd new)
- ✅ File operations (creation, validation)
- ✅ Handlers (constitution, tickets, docs)
- ✅ Utilities (path resolution, name normalization)
- ✅ Error handling
- ⏭️ AI-driven features (slash commands) - Manual testing with checklist

### Writing Tests

**Use pytest:**

```python
import pytest
from pathlib import Path
from cddoc.utils import normalize_name


def test_normalize_name_basic():
    """Test basic name normalization."""
    assert normalize_name("User Auth") == "user-auth"


def test_normalize_name_special_chars():
    """Test normalization with special characters."""
    assert normalize_name("API_Performance!!") == "api-performance"


def test_normalize_name_empty_raises_error():
    """Test that empty names raise ValueError."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        normalize_name("")
```

**Testing file operations:**

```python
import pytest
from pathlib import Path


@pytest.fixture
def temp_git_repo(tmp_path):
    """Create temporary git repository for testing."""
    (tmp_path / ".git").mkdir()
    return tmp_path


def test_cdd_init_creates_structure(temp_git_repo):
    """Test that cdd init creates expected directory structure."""
    from cddoc.cli import init_project

    init_project(temp_git_repo)

    assert (temp_git_repo / "CLAUDE.md").exists()
    assert (temp_git_repo / "specs/tickets").exists()
    assert (temp_git_repo / "docs/features").exists()
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=cddoc --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_cli.py

# Run specific test
poetry run pytest tests/test_cli.py::test_normalize_name
```

### Manual Testing for AI Features

AI-driven features (slash commands) should be manually tested with checklists:

**Manual Testing Checklist for /socrates:**
- ✅ Produces valid YAML output
- ✅ Handles incomplete files (fills gaps)
- ✅ Handles complete files (focuses on refinement)
- ✅ Asks intelligent, context-aware questions
- ✅ Conversation flow feels natural
- ✅ Shows summary before saving
- ✅ Saves correctly after approval

---

## Submitting Changes

### Pull Request Process

1. **Ensure all quality checks pass:**
   - Black formatting ✅
   - Ruff linting ✅
   - Tests passing ✅
   - Coverage maintained or improved ✅

2. **Update documentation:**
   - Add/update docstrings
   - Update relevant .md files
   - Add examples if applicable

3. **Create pull request:**
   - Use descriptive title
   - Reference related issues
   - Explain what changed and why
   - Include testing details

**Good PR description:**

```markdown
## Summary
Add support for enhancement ticket type

## Motivation
Users need a way to track improvements to existing features separately from new features and bugs.

## Changes
- Added enhancement ticket template (src/cddoc/templates/enhancement-ticket-template.yaml)
- Updated CLI to support `cdd new enhancement <name>` command
- Added tests for enhancement ticket creation
- Updated CLI_REFERENCE.md documentation

## Testing
- ✅ Unit tests added (tests/test_enhancement_tickets.py)
- ✅ Manual testing: created enhancement ticket, verified structure
- ✅ All existing tests still pass

## Related Issues
Closes #42
```

### Review Process

1. **Automated checks** run on every PR (GitHub Actions)
2. **Code review** by maintainers
3. **Feedback and iteration** - Address review comments
4. **Approval** - At least one maintainer approval required
5. **Merge** - Maintainer merges your PR

**Review criteria:**
- Code quality and style
- Test coverage
- Documentation updates
- Adherence to project philosophy
- No breaking changes (or proper migration path)

---

## Project Structure

Understanding the codebase structure:

```
context-driven-documentation/
├── src/cddoc/                 # Main package
│   ├── cli.py                 # CLI commands (cdd init, cdd new)
│   ├── handlers/              # File type handlers
│   │   ├── constitution.py    # CLAUDE.md handler
│   │   ├── ticket.py          # Ticket spec.yaml handler
│   │   └── documentation.py   # Documentation handler
│   ├── utils.py               # Utility functions
│   ├── commands/              # Slash command definitions
│   │   ├── socrates.md        # /socrates command
│   │   ├── plan.md            # /plan command
│   │   ├── exec.md            # /exec command
│   │   ├── exec-auto.md       # /exec-auto command
│   │   └── sync-docs.md       # /sync-docs command
│   └── templates/             # Internal templates
│       ├── constitution-template.md
│       ├── feature-ticket-template.yaml
│       ├── bug-ticket-template.yaml
│       ├── spike-ticket-template.yaml
│       ├── enhancement-ticket-template.yaml
│       └── feature-doc-template.md
├── tests/                     # Test suite
│   ├── test_cli.py            # CLI tests
│   ├── test_handlers.py       # Handler tests
│   └── test_utils.py          # Utility tests
├── docs/                      # Documentation
│   ├── features/              # Feature documentation
│   ├── guides/                # User guides
│   └── examples/              # Example specs
├── .claude/commands/          # Framework slash commands (installed by cdd init)
├── pyproject.toml             # Project configuration
├── README.md                  # Project overview
├── CONTRIBUTING.md            # This file
└── LICENSE                    # MIT License
```

**Key components:**

- **CLI (cli.py):** Entry point for `cdd` commands
- **Handlers:** Process different file types (constitution, tickets, docs)
- **Commands:** Slash command definitions (AI-driven)
- **Templates:** Internal templates for tickets and documentation
- **Tests:** Comprehensive test suite

---

## Communication

### Getting Help

- **GitHub Issues:** Ask questions, report bugs, suggest features
- **Discussions:** For broader conversations about design and architecture
- **Pull Requests:** Code reviews and technical discussions

### Asking Questions

Before asking, check:
1. **Documentation** - README, guides, feature docs
2. **Existing issues** - Your question may be answered already
3. **Code** - Sometimes reading the code clarifies things

**When asking:**
- Be specific
- Provide context
- Include code/error messages if relevant
- Mention what you've already tried

### Staying Updated

- **Watch the repository** - Get notified of issues and PRs
- **Star the project** - Show support and stay in the loop
- **Check roadmap** - Understand where the project is headed

---

## Development Philosophy

### AI-First Design

CDD is built for AI-assisted development. When contributing:

- **Use conventional patterns** AI understands
- **Favor clarity over cleverness**
- **Write descriptive names** for functions, variables, classes
- **Document with future AI readers in mind**

### Minimal with Context

Error messages and outputs should be:
- **Clear** - What went wrong?
- **Contextual** - Why does it matter?
- **Actionable** - How to fix it?

### Living Documentation

Documentation should:
- **Evolve with code** - Keep it current
- **Focus on user needs** - What do developers need to know?
- **Show examples** - Don't just describe, demonstrate

---

## Recognition

All contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- Project documentation (for major features)

We value all contributions, whether code, documentation, bug reports, or feature ideas!

---

## Questions?

If you have questions about contributing, please:

1. Check this guide first
2. Search existing issues
3. Open a new issue with the `question` label
4. Email guilherme.gouw@gmail.com for private inquiries

---

## Thank You!

Thank you for contributing to CDD! Your efforts help make AI-assisted development more natural, powerful, and productive for everyone.

**Happy coding! 🚀**

---

*Last Updated: 2025-11-03*

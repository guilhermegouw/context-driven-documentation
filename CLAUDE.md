# Project Constitution

> This file serves as the foundational context for all AI-assisted development in this project.
> Complete this constitution to enable powerful, context-aware AI collaboration.

## Project Overview

**Project:** Context-Driven Documentation (CDD Framework)

**Purpose:** A complete engineering intelligence system that makes human-AI collaboration feel natural, powerful, and productive.

**Target Users:** Software engineers and development teams working with AI assistants

**Business Domain:** Software engineering tools and AI-assisted development

**Core Value Proposition:** Eliminates the need to repeatedly provide context to AI assistants. Capture your project's context once in structured documentation, and AI assistants immediately understand your project, architecture, and current work - making every conversation start from shared understanding instead of zero.

**AI-First Development Philosophy:**
- **MVP Focus**: Claude Code as primary interface - AI-assisted engineering is the core workflow
- **Future Vision**: Support for additional AI clients while maintaining AI-first approach
- **Philosophy**: Building for a new paradigm of software development where AI collaboration is fundamental, not supplementary

## Architecture & Design Patterns

**Architecture Philosophy:** AI-First Design - use well-known, conventional patterns that AI assistants can recognize and understand immediately. Favor clarity and familiarity over cleverness.

**Core Architectural Patterns:**
- **Handler Pattern**: Separate handlers for different file types (ConstitutionHandler, TicketSpecHandler, etc.) - each knows how to work with its specific file format
- **Command Pattern**: CLI commands via Click (`cdd init`, etc.) for tooling operations
- **Slash Commands**: AI-driven commands (`/socrates`, `/plan`) that turn Claude into specialized personas for intelligent conversations
  - `/socrates` - Interactive requirements gathering through natural conversation
  - `/plan` - Autonomous implementation planning with minimal questions
- **Template-Driven**: Use templates to define structure, AI reads templates to understand what needs to be captured

**Key Architectural Decisions:**
1. **Conventional over Clever**: Use familiar design patterns AI already understands rather than inventing new abstractions
2. **Modular Structure**: Each component is self-contained and single-purpose for easy AI comprehension
3. **Two-Tier Interface**:
   - CLI commands (`cdd init`, `cdd new`) for mechanical operations
   - Slash commands (`/socrates`, `/plan`) for AI-driven intelligent interactions
4. **File-Based**: All state lives in files (no database) - simple, inspectable, version-controllable

**Code Organization:**
- `src/cddoc/cli.py` - CLI command definitions
- `src/cddoc/handlers/` - File type handlers (one per file type)
- `.claude/commands/` - Slash command definitions for AI personas
- `.cddoc/templates/` - File templates that define structure

**Integration Points:**
- Claude Code (AI assistant) - primary interface
- Git (version control) - documentation lives in repos
- Local file system - all operations are file-based

## Technology Stack & Constraints

**Primary Language:** Python 3.9+

**Framework:** Minimal - using standard library plus selective dependencies

**Key Dependencies:**
- **Rich** - Terminal UI formatting (panels, tables, colors, progress bars)
- **Click** - CLI argument parsing and command structure
- **PyYAML** - YAML file parsing for specifications
- **Poetry** - Dependency management and packaging

**Database:** None (file-based documentation system)

**Deployment:** Installed locally via pip/poetry as a CLI tool

**Version Constraints:**
- Python 3.9+ required (for modern type hints and syntax)
- Cross-platform compatibility (Linux, macOS, Windows)

**Performance Requirements:**
- Fast startup time (< 1 second)
- Minimal memory footprint
- Works offline (no API calls for core functionality)

**Security Requirements:**
- No sensitive data collection
- All data stays local
- File system access only within project directories

## Error Handling Philosophy

**Error Handling Philosophy:**
- **Minimal with Context** - Find the sweet spot between terse and verbose
- **Three-Part Error Pattern**:
  1. Clear error message (what went wrong)
  2. Brief context (why it matters)
  3. Actionable next step (how to fix it)

**Example:**
```
Error: Not a git repository
CDD requires git for version control of documentation.
Run: git init
```

**Goals:**
- Users immediately understand what's broken
- Users know how to fix it without googling
- No unnecessary verbosity or over-explanation

## Development Standards

**Code Style:**
- **Black** - Automatic code formatting (79 character line length)
- **Ruff** - Fast Python linter for code quality checks
- **Type Hints** - Use throughout for better IDE support and AI understanding
- Consistent formatting is critical - makes code familiar and AI-readable

**Testing Standards:**
- **pytest** - Testing framework
- **Test coverage is important** - aim for high coverage of critical functionality
- Test critical paths and core features thoroughly
- Use `pytest-cov` for coverage reporting
- **Deterministic vs AI-Driven Testing**:
  - **Deterministic features** (CLI commands, file operations, handlers) → Unit tests required
  - **AI-driven features** (slash commands, conversational interfaces) → Manual testing with checklist:
    - ✅ Produces correct output format
    - ✅ Handles edge cases gracefully (empty files, malformed input)
    - ✅ Conversation flow feels natural

**Code Quality Gates:**
- All code must pass Black formatting
- All code must pass Ruff linting (no errors)
- Tests must pass before considering work complete
- Type hints required for public APIs

**Definition of Done:**
- ✅ Feature implemented and working
- ✅ Tests written and passing (unit tests for deterministic features, manual testing checklist for AI features)
- ✅ Code formatted with Black
- ✅ Code passes Ruff checks
- ✅ Documentation updated if needed
- ✅ No breaking changes to existing functionality

**Quality Philosophy:**
Structure and familiarity over novelty - well-formatted, consistently styled code helps both humans and AI understand the system quickly.

## Team Conventions

**Branching Strategy:**
- **Feature branches** - All development happens on feature branches
- Branch naming: descriptive names (e.g., `feature/socrates-command`, `fix/yaml-parsing`)
- Feature branches enable safe experimentation and easy rollbacks
- Main branch (`main`) stays stable

**Commit Message Format:**
- Use basic conventional commit prefixes for clarity:
  - `feat:` - New features
  - `fix:` - Bug fixes
  - `docs:` - Documentation changes
  - `test:` - Test additions or updates
  - `refactor:` - Code refactoring
- Not strict about format, but prefixes provide useful structure
- Keep commits focused and atomic when possible

**Workflow:**
1. Create feature branch from `main`
2. Develop feature with tests
3. Ensure all quality gates pass (Black, Ruff, tests)
4. Commit changes with descriptive messages
5. Merge back to `main` when complete

**Development Environment:**
- Poetry for dependency management
- Virtual environments for isolation
- WSL2/Linux development environment

**Communication:**
- AI-assisted development is primary workflow
- Use Claude Code for implementation and problem-solving
- Documentation (this file!) serves as shared context for all AI interactions

---
*Generated by CDD Framework v0.1.0 - Learn more: https://github.com/guilhermegouw/context-driven-documentation*

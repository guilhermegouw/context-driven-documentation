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
- **Command Pattern**: CLI commands via Click for tooling operations
  - `cdd init` - Framework initialization (options: --force, --minimal)
  - `cdd new` - Ticket and documentation creation with 6 variants:
    - Tickets: feature, bug, spike, enhancement
    - Documentation: guide, feature
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
- `.cdd/templates/` - Internal templates for tickets and documentation
  - Ticket templates: feature, bug, spike, enhancement (YAML with spec.yaml structure)
  - Documentation templates: guide, feature (Markdown)
  - Constitution template: constitution-template.md

**Integration Points:**
- Claude Code (AI assistant) - primary interface
- Git (version control) - documentation lives in repos
- Local file system - all operations are file-based

## Mechanical Layer Commands

The mechanical layer consists of CLI commands that generate files with predictable structure. These commands are deterministic, fast, and require no AI interaction.

### Framework Initialization

**`cdd init [PATH]`** - Initialize CDD structure in a project

**Purpose:** Sets up complete CDD framework with directories, templates, and slash commands

**Options:**
- `--force` - Overwrite existing files (use with caution)
- `--minimal` - Create only essential structure, skip templates
- `PATH` - Target directory (defaults to current directory)

**What it creates:**
- `CLAUDE.md` - Project constitution template
- `specs/tickets/` - Directory for temporary sprint work tickets
- `docs/features/` - Living feature documentation
- `docs/guides/` - User guides and how-to documentation
- `.claude/commands/` - AI agent slash commands (socrates, plan, exec)
- `.cdd/templates/` - Internal templates for tickets and documentation

**Behavior:**
- Detects git root automatically (must be run inside git repository)
- Safe by default - won't overwrite existing CLAUDE.md unless --force is used
- Installs all framework components in a single operation

### Ticket Creation

**`cdd new <type> <name>`** - Create work tickets with spec.yaml

**Ticket Types:**
- `feature` - New functionality or capabilities
- `bug` - Bug fixes and defect resolution
- `spike` - Research, investigation, or proof-of-concept work
- `enhancement` - Improvements to existing features

**Creates:** `specs/tickets/<type>-<name>/spec.yaml`

**Behavior:**
- Auto-populates creation/update dates in spec.yaml
- Normalizes names to lowercase-with-dashes format
  - "User Auth System" → "user-auth-system"
  - "payment_processing" → "payment-processing"
- Prompts for overwrite/rename if ticket already exists
- Validates git repository and template availability

**Examples:**
```bash
cdd new feature user-authentication
cdd new bug "Payment Processing Error"
cdd new spike oauth-provider-comparison
cdd new enhancement improve-error-messages
```

### Documentation Creation

**`cdd new documentation <type> <name>`** - Create living documentation files

**Documentation Types:**
- `guide` - User-facing guides, tutorials, how-to documentation
  - Creates: `docs/guides/<name>.md`
- `feature` - Technical feature documentation, implementation details
  - Creates: `docs/features/<name>.md`

**Behavior:**
- Same name normalization as tickets (lowercase-with-dashes)
- No date population (documentation is living and continuously updated)
- Prompts for overwrite/rename if file already exists

**Examples:**
```bash
cdd new documentation guide getting-started
cdd new documentation feature authentication
```

### Naming Convention Enforcement

All `cdd new` commands automatically normalize names:

**Algorithm:**
1. Convert to lowercase
2. Replace spaces, underscores, special chars with dashes
3. Remove duplicate consecutive dashes
4. Strip leading/trailing dashes

**Validation:**
- Names must contain at least one alphanumeric character after normalization
- Empty or all-special-character names are rejected with clear error message

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

**Post-Completion Bug Workflow:**

When bugs are found after a feature is completed and archived:

1. **Create new bug ticket (don't restore archived feature):**
   ```bash
   cdd new bug <descriptive-bug-name>
   /socrates bug-<name>
   /plan bug-<name>
   /exec bug-<name>
   ```

2. **Socrates loads context automatically:**
   - During `/socrates` conversation, answer when asked: "Is this bug related to an existing feature?"
   - Provide the related feature name (e.g., "feature-user-auth")
   - Socrates will:
     - Search archives first, then active tickets
     - Load spec.yaml and plan.md from related ticket
     - Show brief summary for confirmation
     - Add `related_to` field to bug spec.yaml

3. **Benefits of this approach:**
   - **No re-explaining implementations** - Socrates understands the feature already
   - **Proper template structure** - Bug ticket has correct bug template format
   - **Preserved history** - Feature implementation history stays intact in archive
   - **Clear relationships** - Bug automatically linked to related features via metadata
   - **Faster specifications** - Focus only on what's broken, not how system works

**Why separate tickets:**
- Bug template gives AI proper context for bug requirements (reproduction, impact)
- Feature template structure preserved for feature requirements (user stories, acceptance criteria)
- Clean version control - separate history for feature implementation vs bug fix
- Industry standard practice - bugs are distinct from features

**Example flow:**
```bash
# Bug found after feature-user-auth was archived
cdd new bug user-auth-login-500
/socrates bug-user-auth-login-500
# Socrates asks: "Is this related to an existing feature?"
# You answer: "Yes, feature-user-auth"
# Socrates loads feature context automatically
# You only explain the bug - no need to re-explain authentication system
/plan bug-user-auth-login-500
/exec bug-user-auth-login-500
```

**Living Documentation Sync Workflow:**

After features are implemented and archived, sync living documentation to keep it accurate:

1. **Trigger documentation sync:**
   ```bash
   /sync-docs feature-user-auth
   ```

2. **Review AI-proposed updates:**
   - Sync-Docs analyzes archived ticket (spec + plan + progress)
   - Smart verification reads key interface files (APIs, configs, public interfaces)
   - Proposes specific section updates with reasoning
   - Shows what was implemented vs what's documented

3. **Choose how to proceed:**
   - **[Y] Apply all** - Accept all proposed updates, docs generated automatically
   - **[E] Edit proposals** - Refine through Socratic conversation
   - **[S] Show preview** - See detailed content before applying
   - **[N] Skip** - Defer documentation update for later

4. **Documentation updated automatically:**
   - Feature docs reflect actual implementation
   - APIs, configurations, usage documented accurately
   - Living docs stay in sync with code

**Benefits of sync workflow:**
- **AI analyzes changes** - No manual comparison needed
- **Smart verification** - Reads code to ensure accuracy
- **Targeted proposals** - Specific updates, not overwhelming rewrites
- **Human approval** - Review before applying changes
- **Conversational refinement** - Can discuss and refine proposals
- **Preserved context** - Uses archived ticket as source of truth

**Smart verification approach:**
- ✅ Reads: API routes, configuration files, public interfaces
- ⏭️  Skips: Internal implementation, test files, utilities
- 🎯 Documents: What users need (APIs, configs, usage, examples)
- 🚫 Ignores: Internal details better left in code comments

**Example flow:**
```bash
# Monday: Implement feature
/exec feature-user-auth
# ✅ Implementation complete, ticket archived

# Tuesday: Sync documentation
/sync-docs feature-user-auth
# Sync-Docs analyzes implementation, proposes updates:
#   1. Create API Reference section (3 endpoints discovered)
#   2. Create Configuration section (5 options discovered)
#   3. Create Usage Examples (from acceptance criteria)
# [Y] Apply all
# ✅ docs/features/authentication.md created with accurate details
```

**When to sync:**
- After `/exec` completes and archives ticket
- When you're ready to document (no rush - ticket context preserved)
- Before marking work as fully complete
- Periodically for features that evolved over multiple tickets

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

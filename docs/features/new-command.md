# Feature: `cdd new` Command System

> Living documentation for the ticket and documentation creation engine

**Status:** Production
**Version:** 0.1.0
**Last Updated:** 2025-11-02

---

## Overview

The `cdd new` command system is the **mechanical layer** of the CDD framework. It generates structured files from templates, ensuring consistency between what's created and how intelligent commands (Socrates, plan, exec) will use them.

**Why it exists:**
The CDD framework operates on two layers:
1. **Mechanical layer** (`cdd new`, `cdd init`) - Generates files with predictable structure
2. **Intelligence layer** (`/socrates`, `/plan`, `/exec`) - Fills and processes those files

The `cdd new` command guarantees that every ticket and documentation file follows the exact template structure that intelligent commands expect. This structural contract enables Socrates to know exactly what sections to fill, and plan/exec to know exactly where to find requirements.

**Key Capabilities:**
- Creates 4 ticket types with spec.yaml (feature, bug, spike, enhancement)
- Creates 2 documentation types with markdown templates (guides, features)
- Enforces naming conventions (lowercase-with-dashes)
- Validates git repository and template availability
- Handles overwrites safely with user prompts
- Ensures every file matches its template structure exactly

---

## Current Implementation

### How It Works Today

**User Perspective:**
1. User runs command → System validates environment and normalizes name
2. System checks for conflicts → Prompts for overwrite/rename if needed
3. System creates file(s) from template → Displays success with next steps

**Input → Output:**
```
Input:  cdd new feature "User Auth"
Output: specs/tickets/feature-user-auth/spec.yaml (from template)

Input:  cdd new documentation guide "Getting Started"
Output: docs/guides/getting-started.md (from template)
```

### Architecture Overview

**Command Hierarchy:**
```
cdd new (Click group)
├── feature → create_new_ticket("feature", name)
├── bug → create_new_ticket("bug", name)
├── spike → create_new_ticket("spike", name)
├── enhancement → create_new_ticket("enhancement", name)
└── documentation (nested group)
    ├── guide → create_new_documentation("guide", name)
    └── feature → create_new_documentation("feature", name)
```

**Data Flow:**
```
User Command
    ↓
CLI Layer (cli.py) - Parse arguments, display UI
    ↓
Logic Layer (new_ticket.py) - Validate, create files
    ↓
Templates (.cdd/templates/) - Structure definitions
    ↓
File System (specs/, docs/) - Generated files
```

### Key Components

**CLI Layer: `src/cddoc/cli.py`**
- Purpose: Command definitions and user interface
- Key functions:
  - `feature(name)`, `bug(name)`, `spike(name)`, `enhancement(name)` - Ticket command handlers
  - `doc_guide(name)`, `doc_feature(name)` - Documentation command handlers
  - `_display_ticket_success(result)` - Shows creation summary and next steps for tickets
  - `_display_documentation_success(result)` - Shows creation summary and next steps for docs

**Logic Layer: `src/cddoc/new_ticket.py`**
- Purpose: Core creation logic, validation, file operations
- Key functions:
  - `create_new_ticket(ticket_type, name) -> dict` - Orchestrates ticket creation
    - Input: ticket type (feature/bug/spike/enhancement), raw name
    - Output: `{ticket_path, normalized_name, ticket_type, overwritten}`
  - `create_new_documentation(doc_type, name) -> dict` - Orchestrates doc creation
    - Input: doc type (guide/feature), raw name
    - Output: `{file_path, normalized_name, doc_type, overwritten}`
  - `normalize_ticket_name(name) -> str` - Converts to lowercase-with-dashes format
    - Input: any string ("User Auth", "payment_processing")
    - Output: normalized string ("user-auth", "payment-processing")
  - `get_git_root() -> Path` - Finds git repository root directory
  - `get_template_path(git_root, ticket_type) -> Path` - Locates ticket template file
  - `get_documentation_template_path(git_root, doc_type) -> Path` - Locates doc template file
  - `prompt_overwrite() -> bool` - Asks user to confirm overwrite
  - `prompt_new_name(ticket_type) -> str | None` - Asks for alternative name
  - `create_ticket_file(ticket_path, template_path)` - Writes spec.yaml from template
  - `create_documentation_file(file_path, template_path)` - Writes markdown from template

**Template System: `.cdd/templates/`**
- Purpose: Defines structure for all generated files
- Ticket templates (YAML): `feature-ticket-template.yaml`, `bug-ticket-template.yaml`, `spike-ticket-template.yaml`, `enhancement-ticket-template.yaml`
- Documentation templates (Markdown): `guide-doc-template.md`, `feature-doc-template.md`

---

## Usage

### Basic Usage

**Creating Tickets:**
```bash
# Feature ticket
cdd new feature user-authentication
→ Creates: specs/tickets/feature-user-authentication/spec.yaml

# Bug ticket
cdd new bug login-error-500
→ Creates: specs/tickets/bug-login-error-500/spec.yaml

# Spike (research) ticket
cdd new spike oauth-provider-comparison
→ Creates: specs/tickets/spike-oauth-provider-comparison/spec.yaml

# Enhancement ticket
cdd new enhancement improve-error-messages
→ Creates: specs/tickets/enhancement-improve-error-messages/spec.yaml
```

**Creating Documentation:**
```bash
# Guide documentation
cdd new documentation guide getting-started
→ Creates: docs/guides/getting-started.md

# Feature documentation
cdd new documentation feature authentication
→ Creates: docs/features/authentication.md
```

### Advanced Usage

**Name Normalization:**
```bash
# The system automatically normalizes names
cdd new feature "User Authentication System"
→ Normalized to: user-authentication-system
→ Creates: specs/tickets/feature-user-authentication-system/spec.yaml

cdd new documentation guide "API Reference"
→ Normalized to: api-reference
→ Creates: docs/guides/api-reference.md
```

**Handling Existing Files:**
```bash
# If file/directory exists, system prompts:
$ cdd new feature user-auth

⚠️  Ticket already exists: specs/tickets/feature-user-auth

Overwrite existing ticket? [y/N]: n
Enter new ticket name (or 'cancel'): user-auth-v2

✅ Created: specs/tickets/feature-user-auth-v2/spec.yaml
```

**Complete Workflow (Mechanical → Intelligence):**
```bash
# 1. Create ticket (mechanical layer)
cdd new feature user-authentication

# 2. Fill with Socrates (intelligence layer)
/socrates feature-user-authentication

# 3. Generate plan
/plan feature-user-authentication

# 4. Implement
/exec feature-user-authentication
```

---

## API Reference

### `create_new_ticket(ticket_type: str, name: str) -> dict`

**Purpose:** Main orchestration function for creating ticket directories and spec.yaml files.

**Parameters:**
- `ticket_type` (str): Type of ticket - "feature", "bug", "spike", or "enhancement"
- `name` (str): Raw ticket name from user input (will be normalized)

**Returns:** `dict` with keys:
- `ticket_path` (Path): Absolute path to created ticket directory
- `normalized_name` (str): Normalized name used for directory
- `ticket_type` (str): Type of ticket created
- `overwritten` (bool): True if existing ticket was overwritten

**Example:**
```python
result = create_new_ticket("feature", "User Auth")
# Returns: {
#   "ticket_path": Path("/project/specs/tickets/feature-user-auth"),
#   "normalized_name": "user-auth",
#   "ticket_type": "feature",
#   "overwritten": False
# }
```

**Location:** `src/cddoc/new_ticket.py:296-376`

---

### `create_new_documentation(doc_type: str, name: str) -> dict`

**Purpose:** Main orchestration function for creating documentation markdown files.

**Parameters:**
- `doc_type` (str): Type of documentation - "guide" or "feature"
- `name` (str): Raw documentation name from user input (will be normalized)

**Returns:** `dict` with keys:
- `file_path` (Path): Absolute path to created markdown file
- `normalized_name` (str): Normalized name used for filename
- `doc_type` (str): Type of documentation created
- `overwritten` (bool): True if existing file was overwritten

**Example:**
```python
result = create_new_documentation("guide", "Getting Started")
# Returns: {
#   "file_path": Path("/project/docs/guides/getting-started.md"),
#   "normalized_name": "getting-started",
#   "doc_type": "guide",
#   "overwritten": False
# }
```

**Location:** `src/cddoc/new_ticket.py:379-463`

---

### `normalize_ticket_name(name: str) -> str`

**Purpose:** Converts any string to lowercase-with-dashes format for consistent naming.

**Parameters:**
- `name` (str): Raw name from user input

**Returns:** `str` - Normalized name following conventions

**Algorithm:**
1. Convert to lowercase
2. Replace spaces, underscores, special chars with dashes
3. Remove duplicate consecutive dashes
4. Strip leading/trailing dashes

**Examples:**
```python
normalize_ticket_name("User Auth System")    # → "user-auth-system"
normalize_ticket_name("payment_processing")  # → "payment-processing"
normalize_ticket_name("Feature__Name")       # → "feature-name"
normalize_ticket_name("  dash-test  ")       # → "dash-test"
```

**Location:** `src/cddoc/new_ticket.py:20-54`

---

### `get_git_root() -> Path`

**Purpose:** Finds the git repository root directory.

**Parameters:** None

**Returns:** `Path` - Absolute path to git root

**Raises:** `TicketCreationError` if:
- Not in a git repository
- Git is not installed

**Example:**
```python
git_root = get_git_root()
# Returns: Path("/home/user/my-project")
```

**Location:** `src/cddoc/new_ticket.py:57-85`

---

### `get_template_path(git_root: Path, ticket_type: str) -> Path`

**Purpose:** Locates the template file for a given ticket type.

**Parameters:**
- `git_root` (Path): Git repository root directory
- `ticket_type` (str): Type of ticket ("feature", "bug", "spike", "enhancement")

**Returns:** `Path` - Absolute path to template file

**Raises:** `TicketCreationError` if template doesn't exist

**Example:**
```python
template = get_template_path(git_root, "feature")
# Returns: Path("/project/.cdd/templates/feature-ticket-template.yaml")
```

**Location:** `src/cddoc/new_ticket.py:88-111`

---

### `get_documentation_template_path(git_root: Path, doc_type: str) -> Path`

**Purpose:** Locates the template file for a given documentation type.

**Parameters:**
- `git_root` (Path): Git repository root directory
- `doc_type` (str): Type of documentation ("guide", "feature")

**Returns:** `Path` - Absolute path to template file

**Raises:** `TicketCreationError` if template doesn't exist

**Example:**
```python
template = get_documentation_template_path(git_root, "guide")
# Returns: Path("/project/.cdd/templates/guide-doc-template.md")
```

**Location:** `src/cddoc/new_ticket.py:243-266`

---

### `prompt_overwrite() -> bool`

**Purpose:** Prompts user to confirm overwriting existing file/directory.

**Parameters:** None

**Returns:** `bool` - True if user confirms overwrite, False otherwise

**Behavior:**
- Displays: "Overwrite existing ticket? [y/N]:"
- Default is 'N' (safe default - don't overwrite)
- Accepts 'y', 'yes', 'Y', 'YES' as confirmation

**Location:** `src/cddoc/new_ticket.py:146-161`

---

### `prompt_new_name(ticket_type: str) -> str | None`

**Purpose:** Prompts user for an alternative name when file/directory exists.

**Parameters:**
- `ticket_type` (str): Type of ticket/doc being created (for display)

**Returns:**
- `str` - New name provided by user
- `None` - If user cancels operation

**Behavior:**
- Displays: "Enter new ticket name (or 'cancel'):"
- Returns None if user types 'cancel' or presses Ctrl+C
- Returns new name string for retry

**Location:** `src/cddoc/new_ticket.py:164-194`

---

## Business Rules & Edge Cases

### Business Logic

**Name Normalization Rules:**
- **All lowercase:** "UserAuth" → "userauth"
- **Spaces to dashes:** "User Auth" → "user-auth"
- **Underscores to dashes:** "user_auth" → "user-auth"
- **Special chars removed:** "user@auth!" → "user-auth"
- **Duplicate dashes removed:** "user--auth" → "user-auth"
- **Stripped edges:** " user-auth " → "user-auth"

**Git Repository Requirement:**
- All commands MUST be run inside a git repository
- System finds git root using `git rev-parse --show-toplevel`
- If not in git repo → Clear error message directing user to run `git init`

**Template Validation:**
- Templates MUST exist before creating files
- Missing templates → Error message directing user to run `cdd init`
- Templates define the structural contract for intelligent commands

**Overwrite Safety:**
- Default behavior: Do NOT overwrite existing files
- User must explicitly confirm with 'y' to overwrite
- Alternative: Prompt for new name to avoid data loss

### Edge Cases

**Empty or Invalid Names:**
```bash
cdd new feature ""
→ Error: Invalid ticket name
   Name must contain at least one alphanumeric character.
   Example: cdd new feature user-authentication
```

**All Special Characters:**
```bash
cdd new feature "@#$%"
→ After normalization: "" (empty)
→ Error: Invalid ticket name
```

**Very Long Names:**
```bash
cdd new feature "this-is-a-very-long-feature-name-that-keeps-going-and-going"
→ Accepted (no length limit currently)
→ Creates: specs/tickets/feature-this-is-a-very-long-feature-name-that-keeps-going-and-going/
```

**Non-ASCII Characters:**
```bash
cdd new feature "usuário-autenticação"
→ Normalized: "usurio-autenticao" (non-ASCII chars removed)
```

**Git Subdirectories:**
```bash
# Running from subdirectory: /project/src/components/
cdd new feature user-auth
→ Finds git root: /project
→ Creates: /project/specs/tickets/feature-user-auth/spec.yaml
```

**Missing Templates:**
```bash
# If templates weren't installed
cdd new feature user-auth
→ Error: Template not found: feature-ticket-template.yaml
   Templates are required for ticket creation.
   Run: cdd init
```

**Concurrent File System:**
```bash
# Edge case: File created between existence check and creation
→ System overwrites (race condition possible but rare)
```

### Validation Rules

- **Name validation:** Must contain at least one alphanumeric character after normalization
- **Git validation:** Repository must exist before any file creation
- **Template validation:** Template file must exist and be readable
- **Path validation:** Must have write permissions to target directory

---

## Testing

### Test Coverage

- **Unit tests:** `tests/test_new_ticket.py`
- **Coverage:** Focused on deterministic functions (name normalization, path resolution)
- **Manual testing:** Required for UI/UX flows (prompts, Rich formatting)

### Key Test Scenarios

**Automated (Unit Tests):**
- Name normalization with various inputs
- Git root discovery in different directory contexts
- Template path resolution
- File creation with valid templates
- Error handling for missing git repo
- Error handling for missing templates

**Manual Testing Checklist:**
- ✅ All 6 command variants create correct files
- ✅ Rich UI displays correctly (panels, tables, colors)
- ✅ Overwrite prompts work as expected
- ✅ Alternative name prompts handle cancellation
- ✅ Success messages show correct next steps
- ✅ Error messages are clear and actionable

**Edge Case Testing:**
- Empty names rejected with clear error
- Special characters normalized correctly
- Very long names handled properly
- Non-ASCII characters processed safely
- Git subdirectory detection works
- Race conditions (rare but possible)

---

## Dependencies

### Required Dependencies

- **Click (^8.0):** Command-line interface framework
  - Purpose: Command groups, argument parsing, nested commands
  - Used for: Entire CLI structure (`@main.group()`, `@new.command()`)

- **Rich (^13.0):** Terminal UI formatting
  - Purpose: Beautiful terminal output with panels, tables, colors
  - Used for: Success messages, error display, progress indicators

- **Git (system requirement):** Version control system
  - Purpose: Repository validation and root discovery
  - Used for: Finding project root, validating git repo exists

- **PyYAML (^6.0):** YAML file parsing
  - Purpose: Reading YAML template files
  - Used for: Template validation and content reading (though templates are copied as-is)

- **Python 3.9+:** Language runtime
  - Purpose: Modern type hints, pathlib support
  - Used for: Entire codebase

### Integration Points

**File System Integration:**
- Reads templates from `.cdd/templates/`
- Writes tickets to `specs/tickets/{type}-{name}/`
- Writes documentation to `docs/guides/` or `docs/features/`
- All operations use absolute paths from git root

**Git Integration:**
- Calls `git rev-parse --show-toplevel` via subprocess
- Validates repository exists before any operations
- Ensures all files created within git control

**Socrates Integration:**
- Success messages always reference Socrates as next step
- File paths shown in format Socrates expects
- Creates files with structure Socrates knows how to fill

**CLI Framework (Click):**
- Nested command groups enable `cdd new documentation guide`
- Decorators define command hierarchy
- Automatic help text generation

**Terminal UI (Rich):**
- Console output for all user messages
- Panels for framing important information
- Tables for displaying creation results
- Color coding for status (green=success, yellow=warning, red=error)

---

## Performance & Scalability

**Performance Characteristics:**
- **Startup time:** < 100ms (fast CLI initialization)
- **Command execution:** < 500ms for typical operations
- **Memory footprint:** Minimal (< 50MB)
- **Disk I/O:** Single template read + single file write per operation

**Scalability Limits:**
- No practical limit on number of tickets/docs
- Performance independent of project size
- Each command is isolated operation (no cumulative state)

**Optimization Notes:**
- Template files read once per command (not cached across invocations)
- Git root discovery cached within single command execution
- No database or network calls (all local file operations)
- Rich UI rendering is fast even for complex layouts

---

## Security & Compliance

**Security Considerations:**
- **File system access:** Limited to within git repository root
- **No sensitive data:** Commands don't collect or transmit user data
- **Local only:** All operations are local file system
- **Path traversal protection:** Uses git root as boundary

**Data Handling:**
- User input (names) is sanitized through normalization
- Template content copied as-is (no code execution)
- No external API calls or network activity

**Compliance:**
- GDPR: No personal data collection
- Open source: MIT license
- Local execution: User data never leaves machine

---

## Future Enhancements

**Template Extensibility:**
- Auto-discovery of custom templates in `.cdd/templates/`
- User-defined ticket types beyond the 4 built-in
- Template inheritance for customization

**Batch Operations:**
- Create multiple tickets from CSV/JSON
- Bulk documentation generation
- Project scaffolding (create related tickets together)

**Integration Improvements:**
- GitHub/GitLab/Jira integration for ticket sync
- Import existing issues as CDD tickets
- Export tickets to external systems

**Enhanced Validation:**
- Check for duplicate ticket names across types
- Validate ticket name against project conventions
- Suggest similar existing tickets

**Improved User Experience:**
- Interactive ticket creation wizard
- Template preview before creation
- Undo command for accidental creation

---

## Related Documentation

- [CLI Reference Guide](../guides/CLI_REFERENCE.md) - Complete command reference
- [Init Command](init-command.md) - Framework initialization
- [Socrates Guide](../guides/SOCRATES_GUIDE.md) - Requirements gathering workflow
- [Template System](../guides/TEMPLATE_SYSTEM.md) - How templates work *(Coming Soon)*

---

*Last updated: 2025-11-02 | Status: Production | Version: 0.1.0*

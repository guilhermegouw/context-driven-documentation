# Feature: Init Command

> Living documentation for the `cdd init` command

**Status:** Production
**Version:** 0.1.0
**Last Updated:** 2025-11-01

---

## Current Implementation Status

The `cdd init` command initializes the CDD framework structure in any project directory. It creates a clean, git-friendly directory layout and installs framework components (AI agents and templates) from the package.

**Production Status:** Stable and tested (22 unit tests, 94% coverage)

**Last Major Updates:**
- v0.1.0 (2025-11-01): Complete refactor to new structure (specs/, docs/, .claude/, .cdd/)
- Introduced living documentation concept with docs/features/
- Framework commands shipped with package instead of inline templates
- Added .gitkeep files for empty directories

---

## How It Works Today

### User Perspective

When a developer runs `cdd init` in their project:

1. **Validates Environment**
   - Checks for git repository (required)
   - Validates write permissions
   - Refuses to initialize in dangerous system directories

2. **Creates Directory Structure**
   - `specs/tickets/` - For current sprint work (tickets with specs and plans)
   - `docs/features/` - For living documentation
   - `.claude/commands/` - Framework AI agents (socrates, plan, exec, exec-auto)
   - `.cdd/templates/` - Internal templates for ticket creation

3. **Generates Project Files**
   - `CLAUDE.md` - Project constitution template
   - `.gitkeep` files in empty directories (specs/tickets/, docs/features/)

4. **Shows Next Steps**
   - Rich terminal UI with component summary
   - Quick start workflow guidance
   - Links to documentation

### System Behavior

**Idempotent Operation:**
- Running `cdd init` multiple times is safe
- Only creates missing directories and files
- Preserves existing content by default
- `--force` flag overwrites existing files (use with caution)

**Git Integration:**
- Auto-detects git root and initializes there (not in subdirectory)
- All created files are git-friendly (text-based, no binary)
- Respects .gitignore (if .cdd/config.yaml should be ignored)

**Error Handling:**
- Clear error messages with actionable fixes
- Validates before creating anything
- Fails fast with helpful context

---

## Technical Implementation

### Architecture Overview

**Components:**

```
cdd init
    ↓
validate_path()  ← Checks safety and permissions
    ↓
check_existing_structure()  ← Detects what already exists
    ↓
create_directory_structure()  ← Creates folders + .gitkeep
    ↓
install_framework_commands()  ← Copies from src/cddoc/commands/
    ↓
install_templates()  ← Copies from src/cddoc/templates/
    ↓
generate_claude_md()  ← Creates CLAUDE.md from template
    ↓
Display success summary (Rich UI)
```

### Key Files and Components

**Core Logic:**
- `src/cddoc/init.py:initialize_project()` - Main entry point
- `src/cddoc/cli.py:init()` - CLI command wrapper with Rich UI

**Helper Functions:**
- `validate_path()` - Security checks (dangerous paths, permissions)
- `is_dangerous_path()` - Prevents initialization in /, /usr, /etc, etc.
- `get_git_root()` - Finds git repository root
- `check_existing_structure()` - Detects existing CDD installation
- `create_directory_structure()` - Creates folder hierarchy
- `install_framework_commands()` - Copies AI agent files from package
- `install_templates()` - Copies template files from package
- `generate_claude_md()` - Creates constitution from template

**Package Resources:**
- `src/cddoc/commands/*.md` - Framework AI agents (4 files)
- `src/cddoc/templates/*.md|*.yaml` - Ticket and plan templates (8+ files)

### Data Flow

```python
# User runs: cdd init /path/to/project

1. CLI parses arguments (path, --force, --minimal)
   ↓
2. initialize_project(path, force, minimal) called
   ↓
3. Path validation and resolution
   - Resolve to absolute path
   - Check if dangerous (/, /usr, /home, etc.)
   - Check write permissions
   ↓
4. Git root detection (if in git repo)
   - Use git root instead of subdirectory
   - Show info message to user
   ↓
5. Check existing structure
   - Scan for specs/, docs/, .claude/, .cdd/
   - Return list of existing items
   ↓
6. Create directory structure
   - Only create missing directories
   - Add .gitkeep to empty user directories
   ↓
7. Install framework files
   - Copy commands from package (shutil.copy2)
   - Copy templates from package (glob + copy)
   ↓
8. Generate CLAUDE.md
   - Skip if exists (unless --force)
   - Copy from constitution-template.md
   ↓
9. Return result dict
   {
     "path": Path,
     "created_dirs": List[str],
     "installed_commands": List[str],
     "installed_templates": List[str],
     "claude_md_created": bool,
     "existing_structure": bool
   }
   ↓
10. CLI displays Rich UI summary
```

### Database Schema (File-Based)

**No traditional database** - all state lives in files:

**Directory Structure:**
```
project/
├── CLAUDE.md                      # Project constitution
├── specs/tickets/                 # Ticket folders
│   └── .gitkeep
├── docs/features/                 # Living docs
│   └── .gitkeep
├── .claude/commands/              # Framework agents
│   ├── socrates.md
│   ├── plan.md
│   ├── exec.md
│   └── exec-auto.md
└── .cdd/templates/                # Internal templates
    ├── constitution-template.md
    ├── feature-ticket-template.yaml
    ├── bug-ticket-template.yaml
    ├── spike-ticket-template.yaml
    ├── feature-plan-template.md
    ├── bug-plan-template.md
    ├── spike-plan-template.md
    └── feature-doc-template.md
```

---

## Business Rules & Edge Cases

### Business Logic

**Initialization Rules:**
1. Must be in a git repository (enforced)
2. Cannot initialize in system directories (/, /usr, /etc, home)
3. Must have write permissions
4. Prefers git root over subdirectories
5. Only creates missing items (partial initialization supported)

**File Handling:**
1. CLAUDE.md only created if it doesn't exist (unless --force)
2. Framework commands always copied (overwrites if exist)
3. Templates always copied (overwrites if exist)
4. Directories created if missing (mkdir -p behavior)

### Edge Cases

**Git Repository Detection:**
- If run in git subdirectory → uses git root
- If run outside git → shows error, refuses to initialize
- If git command fails → treats as non-git directory

**Existing Structure:**
- Partial installation → creates only missing items
- Full installation exists → shows warning, skips existing
- --force flag → overwrites CLAUDE.md (commands/templates always overwrite)

**Permissions:**
- No write access → fails with clear error
- Parent directory doesn't exist → creates it (mkdir -p)
- System directory → refuses immediately (security)

**Concurrent Execution:**
- Multiple `cdd init` in same directory → safe (file operations are atomic)
- Git operations not locked → relies on git's locking

### Validation Rules

**Path Validation:**
```python
DANGEROUS_PATHS = ["/", "/usr", "/etc", "/bin", "/sbin", "/var", "/sys", "/proc", "/boot"]
- Rejects if path in DANGEROUS_PATHS
- Rejects if path == Path.home()
- Requires write permission (os.access check)
```

**Git Validation:**
```python
- Must have .git directory in tree
- git rev-parse --show-toplevel succeeds
```

**File Creation:**
```python
- CLAUDE.md: skip if exists (unless force=True)
- Commands: always copy (overwrite)
- Templates: always copy (overwrite)
- Directories: create if missing (exist_ok=True)
```

---

## Testing

### Test Coverage

**Location:** `tests/test_init.py` (22 tests, 94% coverage)

**Test Categories:**

1. **Integration Tests:**
   - `test_initialize_project_creates_structure()` - Full workflow
   - `test_initialize_existing_structure()` - Idempotent behavior
   - `test_initialize_with_force_flag()` - Force overwrite

2. **Component Tests:**
   - `test_create_directory_structure()` - Directory creation
   - `test_install_framework_commands()` - Command installation
   - `test_install_templates()` - Template installation
   - `test_generate_claude_md()` - CLAUDE.md generation

3. **Validation Tests:**
   - `test_is_dangerous_path()` - Security checks
   - `test_validate_path_dangerous()` - Path validation
   - `test_validate_path_no_permission()` - Permission checks

4. **Edge Case Tests:**
   - `test_initialize_nonexistent_directory()` - Creates parent dirs
   - `test_gitkeep_files_created()` - .gitkeep in empty dirs
   - `test_check_existing_structure_*()` - Existing file detection

### Known Issues

**None currently.** All 22 tests passing.

**Potential Future Issues:**
- Windows symlink compatibility (if we add symlinks)
- Non-UTF8 file systems (template files assume UTF-8)
- Permissions on shared filesystems (NFS, SMB)

---

## Dependencies

### External Dependencies

**Python Standard Library:**
- `os` - File permissions checking
- `shutil` - File copying operations
- `subprocess` - Git command execution
- `pathlib` - Path manipulation

**Framework Dependencies:**
- `rich` - Terminal UI (panels, tables, colors)
- `click` - CLI argument parsing (via cli.py)

### Internal Dependencies

**Commands that depend on init:**
- `cdd new` - Requires `.cdd/templates/` for ticket creation
- `/socrates` - References templates for understanding structure
- `/plan` - References templates for plan generation

**Files created by init that other components need:**
- `CLAUDE.md` - Loaded by all AI agents
- `.cdd/templates/` - Used by `cdd new`
- `.claude/commands/` - Slash commands for Claude Code

---

## Performance & Scalability

### Current Performance

**Initialization Time:** < 1 second for typical project

**Operations:**
- Directory creation: O(n) where n = 4 directories
- File copying: O(m) where m = 12 files (4 commands + 8 templates)
- Git root detection: 1 subprocess call
- Path validation: O(1) checks

**Bottlenecks:**
- Git subprocess call (typically 10-50ms)
- File I/O for copying (negligible for small files)

### Scalability Considerations

**Not a Concern:**
- Init runs once per project
- Files are small (< 50KB total)
- No network calls
- No database operations

**Future Optimizations (if needed):**
- Parallel file copying (unlikely to be necessary)
- Cache git root detection (not worth complexity)
- Use symlinks instead of copying commands (breaks on Windows)

---

## Security & Compliance

### Security Measures

**Path Validation:**
- Refuses to initialize in system directories
- Refuses to initialize in user home directory
- Checks write permissions before creating files

**File Operations:**
- Uses shutil.copy2 (preserves metadata safely)
- No shell command execution (except git subprocess)
- No eval() or exec() - all paths are validated

**Template Security:**
- Templates are read-only data files
- No executable code in templates
- YAML templates validated on read (by new_ticket.py)

### Compliance

**Git-Friendly:**
- All files are text-based (UTF-8)
- No binary files created
- .gitkeep for empty directories (git compatibility)

**Cross-Platform:**
- Uses pathlib (cross-platform path handling)
- No platform-specific commands (except git, which is universal)
- Works on Linux, macOS, Windows

---

## Future Enhancements

### Planned Improvements

**Smart Defaults:**
- Auto-detect project type (Python, JavaScript, etc.)
- Pre-populate CLAUDE.md with detected info (from package.json, requirements.txt)
- Suggest tech stack based on files in repository

**Template Customization:**
- Allow user-level template customization (~/.cdd/templates/)
- Support project-specific template overrides
- Template marketplace (share templates)

**Enhanced Git Integration:**
- Auto-commit initialization (optional)
- Create .gitignore entries automatically
- Detect and warn about uncommitted changes

**Validation Enhancements:**
- Check for conflicting tools (.cdd/ collision)
- Validate project name conventions
- Warn about large repositories (performance)

### Potential Expansions

**Team Features:**
- Sync framework commands across team (version pinning)
- Shared templates repository
- Organization-level defaults

**Developer Experience:**
- Interactive mode (prompts for customization)
- Dry-run mode (--dry-run to preview)
- Verbose mode (--verbose for debugging)

**Maintenance:**
- `cdd upgrade` - Update framework commands to latest
- `cdd doctor` - Validate installation integrity
- `cdd clean` - Remove unused files

---

## Related Documentation

- **CLI Reference:** [docs/guides/CLI_REFERENCE.md](../guides/CLI_REFERENCE.md) - User-facing command documentation
- **Templates:** `src/cddoc/templates/` - All template files
- **Commands:** `src/cddoc/commands/` - Framework AI agent files
- **Tests:** `tests/test_init.py` - Comprehensive test suite

---

*This is a living document - update it as the init command evolves*
*Last reviewed: 2025-11-01 by Claude*

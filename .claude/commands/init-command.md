# /init-command

**Context:** Implementation details for the `cdd init` command

## Overview
The init command sets up the CDD folder structure in a new or existing project. It creates the necessary directories, generates template files, and establishes the foundation for context-driven documentation.

This is the entry point for any project wanting to use CDD - it should be simple, safe, and provide immediate value.

## Core Capabilities
- Initialize CDD structure in new projects
- Safely initialize in existing projects without overwriting files
- Create starter templates for project and feature specs
- Generate initial Claude Code command structure
- Provide clear feedback about what was created

## Key Workflows

### init_new_project
**Trigger:** User runs `cdd init project-name`

**Steps:**
1. Create project directory if it doesn't exist
2. Create directory structure: `specs/`, `specs/features/`, `.claude/commands/`, `.cddoc/templates/`
3. Copy template files into `.cddoc/templates/`
4. Generate default `project.yaml` with placeholder content
5. Generate `sync-docs.md` command
6. Create `.cddoc/config.yaml` with defaults
7. Display success message with next steps

### init_existing_project
**Trigger:** User runs `cdd init .` in existing project

**Steps:**
1. Check if CDD structure already exists
2. If exists, ask for confirmation before proceeding
3. Create missing directories only
4. Skip files that already exist (no overwrite)
5. Report what was created vs. what was skipped
6. Validate existing structure if present

## Business Rules
- **Never overwrite existing files without explicit confirmation**
- All generated files should have comments indicating they're auto-generated
- Project name must be valid directory name (lowercase, hyphens allowed)
- If `.git` exists, prefer git root as project root
- Templates should be self-documenting with inline comments
- Config file should have sensible defaults requiring zero configuration

## Edge Cases to Consider
- What if directory already exists with CDD structure?
- What if user runs init in their home directory by accident?
- What if `specs/` exists but isn't a CDD structure?
- What if permissions prevent directory creation?
- What if `.claude/` directory exists from previous manual setup?
- What if user runs init multiple times?
- What if project name contains invalid characters?

## CLI Interface

### Command
```bash
cdd init [path]
```

### Arguments
- `path` (optional) — Target directory, defaults to current directory. Creates if doesn't exist.

### Options
- `--force` — Overwrite existing files (use with caution)
- `--minimal` — Create only essential structure, skip templates

### Exit Codes
- `0` — Success, structure created
- `1` — Error (invalid path or permissions)
- `2` — Aborted (user declined overwrite)

## Directory Structure Created

```
project/
├── specs/
│   ├── project.yaml          # Generated from template
│   └── features/             # Empty, ready for feature specs
│
├── .claude/
│   └── commands/
│       └── sync-docs.md      # Built-in sync command
│
└── .cddoc/
    ├── config.yaml           # Tool configuration
    └── templates/
        ├── feature.yaml      # Template for new features
        ├── project.yaml      # Template for project spec
        └── config.yaml       # Template for config
```

## Dependencies
**Required:**
- `pathlib` — Cross-platform path manipulation
- `PyYAML` — YAML file generation

**Optional:**
- `click` or `argparse` — CLI argument parsing
- `rich` — Pretty terminal output with colors

## Implementation Notes

### 1. Path Resolution
- Use `pathlib.Path` for cross-platform compatibility
- Resolve relative paths to absolute paths early
- Detect git repository root if available using `git rev-parse --show-toplevel`

### 2. Safety Checks
```python
# Check if path is suspiciously broad
dangerous_paths = ['/', os.path.expanduser('~'), '/usr', '/etc']
if path.resolve() in [Path(p) for p in dangerous_paths]:
    print("⚠️  Refusing to initialize in system directory")
    sys.exit(1)

# Verify write permissions before starting
if not os.access(path, os.W_OK):
    print("❌ No write permission for this directory")
    sys.exit(1)
```

### 3. Directory Creation
```python
# Create all directories with exist_ok=True
directories = [
    'specs',
    'specs/features',
    '.claude/commands',
    '.cddoc',
    '.cddoc/templates'
]

for dir_path in directories:
    (base_path / dir_path).mkdir(parents=True, exist_ok=True)
```

### 4. File Generation
- Templates should be complete, working examples
- Include helpful comments and documentation
- Use realistic placeholder values
- Add "auto-generated" comment at top of each file

### 5. User Feedback
```python
# Show clear progress
print("✅ Created specs/ structure")
print("✅ Created .claude/commands/")
print("⚠️  Skipped specs/project.yaml (already exists)")

# Provide next steps
print("\nNext steps:")
print("1. Edit specs/project.yaml to describe your project")
print("2. Run 'cdd new your-first-feature'")
```

### 6. Idempotency
Running init twice should be safe:
- Skip existing files, create missing ones
- Report what was skipped vs. created
- Never fail if structure already exists

## Security Considerations
- Validate path input to prevent directory traversal attacks
- Check write permissions before attempting to create files
- Never execute user input as shell commands
- Limit path depth to prevent accidental system-wide initialization

## Example Usage

### New Project
```bash
$ cdd init my-app

✅ Created my-app/ directory
✅ Created specs/ structure
✅ Created .claude/commands/
✅ Generated templates

Next steps:
1. cd my-app
2. Edit specs/project.yaml to describe your project
3. Run 'cdd new your-first-feature' to create a feature spec

$ cd my-app && tree -a -L 2
my-app/
├── .cddoc/
│   ├── config.yaml
│   └── templates/
├── .claude/
│   └── commands/
├── specs/
│   ├── features/
│   └── project.yaml
```

### Existing Project
```bash
$ cd existing-project
$ cdd init .

✅ Created specs/features/
⚠️  Skipped specs/project.yaml (already exists)
✅ Created .claude/commands/

CDD structure ready! Your existing files were preserved.
```

## Test Cases

### Test 1: Init in empty directory
```python
def test_init_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(['cdd', 'init', tmpdir])
        assert result.returncode == 0
        assert (Path(tmpdir) / 'specs' / 'features').exists()
        assert (Path(tmpdir) / '.claude' / 'commands').exists()
        assert (Path(tmpdir) / 'specs' / 'project.yaml').exists()
```

### Test 2: Init preserves existing files
```python
def test_init_preserves_existing():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create existing project.yaml with custom content
        specs_dir = Path(tmpdir) / 'specs'
        specs_dir.mkdir()
        custom_content = "project:\n  name: 'custom'"
        (specs_dir / 'project.yaml').write_text(custom_content)
        
        # Run init
        subprocess.run(['cdd', 'init', tmpdir])
        
        # Verify custom content preserved
        assert (specs_dir / 'project.yaml').read_text() == custom_content
```

### Test 3: Init rejects dangerous paths
```python
def test_init_rejects_root():
    result = subprocess.run(['cdd', 'init', '/'], capture_output=True)
    assert result.returncode == 1
    assert b"system directory" in result.stderr
```

## Suggested Prompts

When using this context, you can ask Claude to:
- "Help me implement the directory creation logic with proper error handling"
- "How should I detect if we're in a git repository?"
- "What's the best way to handle the overwrite protection?"
- "Show me how to generate the template files with good defaults"
- "How can I make the CLI output colorful and user-friendly?"
- "Help me write tests for the init command"

## Open Questions
- Should we auto-detect project name from git remote or directory name?
- Should we offer different templates (Python vs. JS vs. generic)?
- Should we create a `.gitignore` entry for `.cddoc/cache` (future feature)?
- Should init create a sample feature spec to show the format?
- Should we integrate with git to auto-commit the initial structure?

## Performance Target
- Should complete in **<1 second** for typical projects
- No external API calls or network requests
- Minimal file system operations

---
*Manually created for bootstrap process*  
*Source: specs/features/init-command.yaml*  
*Created: 2025-10-26*

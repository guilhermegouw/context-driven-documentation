"""Initialize CDD structure in projects."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

from rich.console import Console

console = Console()

# Dangerous system paths that should never be initialized
DANGEROUS_PATHS = [
    "/",
    "/usr",
    "/etc",
    "/bin",
    "/sbin",
    "/var",
    "/sys",
    "/proc",
    "/boot",
]


class InitializationError(Exception):
    """Raised when initialization cannot proceed."""

    pass


def is_dangerous_path(path: Path) -> bool:
    """Check if path is a dangerous system directory.

    Args:
        path: Path to check

    Returns:
        True if path is dangerous, False otherwise
    """
    resolved = path.resolve()

    # Check if it's a dangerous system path
    if str(resolved) in DANGEROUS_PATHS:
        return True

    # Check if it's home directory
    home = Path.home()
    if resolved == home:
        return True

    return False


def get_git_root(path: Path) -> Path | None:
    """Try to find git repository root.

    Args:
        path: Starting path to search from

    Returns:
        Git root path if found, None otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def validate_path(path: Path) -> Path:
    """Validate and resolve target path.

    Args:
        path: Target path for initialization

    Returns:
        Resolved absolute path

    Raises:
        InitializationError: If path is invalid or dangerous
    """
    # Resolve to absolute path
    resolved = path.resolve()

    # Check if dangerous
    if is_dangerous_path(resolved):
        raise InitializationError(
            f"Refusing to initialize in system directory: {resolved}"
        )

    # Check write permissions if directory exists
    if resolved.exists() and not os.access(resolved, os.W_OK):
        raise InitializationError(
            f"No write permission for directory: {resolved}"
        )

    return resolved


def check_existing_structure(base_path: Path) -> Tuple[bool, List[str]]:
    """Check if CDD structure already exists.

    Args:
        base_path: Base directory to check

    Returns:
        Tuple of (has_structure, existing_items)
        where has_structure is True if any CDD items exist,
        and existing_items is list of existing paths
    """
    existing = []

    # Check for CDD directories (new structure)
    cdd_items = [
        "specs",
        "specs/tickets",
        "docs",
        "docs/features",
        ".claude",
        ".claude/commands",
        ".cdd",
        ".cdd/templates",
    ]

    for item in cdd_items:
        if (base_path / item).exists():
            existing.append(item)

    # Check for key files
    key_files = [
        "CLAUDE.md",
    ]

    for file in key_files:
        if (base_path / file).exists():
            existing.append(file)

    return len(existing) > 0, existing


def create_directory_structure(base_path: Path) -> List[str]:
    """Create CDD directory structure.

    Args:
        base_path: Base directory for structure

    Returns:
        List of created directories
    """
    directories = [
        "specs/tickets",
        "docs/features",
        ".claude/commands",
        ".cdd/templates",
    ]

    created = []
    for dir_path in directories:
        full_path = base_path / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_path)

            # Create .gitkeep for empty directories
            if dir_path in ["specs/tickets", "docs/features"]:
                gitkeep = full_path / ".gitkeep"
                gitkeep.touch()

    return created


def install_framework_commands(base_path: Path) -> List[str]:
    """Copy framework command files to .claude/commands/.

    Args:
        base_path: Base directory for project

    Returns:
        List of installed command files
    """
    commands_source = Path(__file__).parent / "commands"
    commands_dest = base_path / ".claude" / "commands"

    command_files = [
        "socrates.md",
        "plan.md",
        "exec.md",
        "exec-auto.md",
    ]

    installed = []
    for cmd_file in command_files:
        source = commands_source / cmd_file
        dest = commands_dest / cmd_file

        if source.exists():
            shutil.copy2(source, dest)
            installed.append(f".claude/commands/{cmd_file}")

    return installed


def install_templates(base_path: Path) -> List[str]:
    """Copy templates to .cdd/templates/.

    Args:
        base_path: Base directory for project

    Returns:
        List of installed template files
    """
    templates_source = Path(__file__).parent / "templates"
    templates_dest = base_path / ".cdd" / "templates"

    installed = []

    # Copy all template files
    for template_file in templates_source.glob("*.md"):
        dest = templates_dest / template_file.name
        shutil.copy2(template_file, dest)
        installed.append(f".cdd/templates/{template_file.name}")

    for template_file in templates_source.glob("*.yaml"):
        dest = templates_dest / template_file.name
        shutil.copy2(template_file, dest)
        installed.append(f".cdd/templates/{template_file.name}")

    return installed


def generate_claude_md(base_path: Path, force: bool = False) -> bool:
    """Generate CLAUDE.md from constitution template.

    Args:
        base_path: Base directory for project
        force: Whether to overwrite existing file

    Returns:
        True if file was created, False if skipped
    """
    claude_md_path = base_path / "CLAUDE.md"

    # Skip if exists and not forcing
    if claude_md_path.exists() and not force:
        return False

    # Copy from template
    template_path = (
        base_path / ".cdd" / "templates" / "constitution-template.md"
    )

    if template_path.exists():
        shutil.copy2(template_path, claude_md_path)
        return True

    return False


def initialize_project(
    path: str, force: bool = False, minimal: bool = False
) -> dict:
    """Initialize CDD structure in a project.

    Creates:
    - CLAUDE.md (project constitution)
    - specs/tickets/ (temporary work)
    - docs/features/ (living documentation)
    - .claude/commands/ (framework AI agents)
    - .cdd/templates/ (internal templates)

    Args:
        path: Target directory path
        force: Whether to overwrite existing files
        minimal: Whether to create minimal structure only (reserved for future)

    Returns:
        Dictionary with initialization results

    Raises:
        InitializationError: If initialization fails
    """
    target_path = Path(path)

    # Validate path
    try:
        target_path = validate_path(target_path)
    except InitializationError as e:
        raise e

    # Create directory if it doesn't exist
    if not target_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)

    # Try to use git root if we're in a git repo
    git_root = get_git_root(target_path)
    if git_root and git_root != target_path:
        console.print(
            f"[blue]ℹ️  Detected git repository. "
            f"Using git root: {git_root}[/blue]"
        )
        target_path = git_root

    # Check for existing structure
    has_existing, existing_items = check_existing_structure(target_path)

    if has_existing and not force:
        console.print(
            "[yellow]⚠️  CDD structure partially exists. "
            "Creating missing items only.[/yellow]"
        )

    # Create directory structure
    created_dirs = create_directory_structure(target_path)

    # Install framework commands
    installed_commands = install_framework_commands(target_path)

    # Install templates
    installed_templates = install_templates(target_path)

    # Generate CLAUDE.md
    claude_md_created = generate_claude_md(target_path, force)

    return {
        "path": target_path,
        "created_dirs": created_dirs,
        "installed_commands": installed_commands,
        "installed_templates": installed_templates,
        "claude_md_created": claude_md_created,
        "existing_structure": has_existing,
    }

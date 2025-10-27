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

    # Check for CDD directories
    cdd_items = [
        "specs",
        "specs/features",
        ".claude/commands",
        ".cddoc",
        ".cddoc/templates",
    ]

    for item in cdd_items:
        if (base_path / item).exists():
            existing.append(item)

    # Check for key files
    key_files = [
        "specs/project.yaml",
        ".cddoc/config.yaml",
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
        "specs",
        "specs/features",
        ".claude/commands",
        ".cddoc",
        ".cddoc/templates",
    ]

    created = []
    for dir_path in directories:
        full_path = base_path / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_path)

    return created


def copy_template_files(base_path: Path) -> Tuple[List[str], List[str]]:
    """Copy template files from package to project.

    Args:
        base_path: Base directory for project

    Returns:
        Tuple of (created_files, skipped_files)
    """
    # Get template directory from package
    template_dir = Path(__file__).parent / "templates"

    if not template_dir.exists():
        raise InitializationError(
            "Template directory not found in package"
        )

    created = []
    skipped = []

    # Map templates to destination paths (template_file, destination_path)
    template_mapping = [
        ("project.yaml", "specs/project.yaml"),
        ("config.yaml", ".cddoc/config.yaml"),
        ("feature.yaml", ".cddoc/templates/feature.yaml"),
        ("project.yaml", ".cddoc/templates/project.yaml"),
        ("sync-docs.md", ".claude/commands/sync-docs.md"),
    ]

    for template_name, dest_path in template_mapping:
        source = template_dir / template_name
        destination = base_path / dest_path

        if destination.exists():
            skipped.append(dest_path)
        else:
            # Ensure parent directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            created.append(dest_path)

    return created, skipped


def initialize_project(
    path: str, force: bool = False, minimal: bool = False
) -> dict:
    """Initialize CDD structure in a project.

    Args:
        path: Target directory path
        force: Whether to overwrite existing files
        minimal: Whether to create minimal structure only

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

    # Check for existing structure
    has_existing, existing_items = check_existing_structure(target_path)

    if has_existing and not force:
        # Partial initialization - create missing items only
        console.print(
            "[yellow]⚠️  CDD structure partially exists. "
            "Creating missing items only.[/yellow]"
        )

    # Try to use git root if we're in a git repo
    git_root = get_git_root(target_path)
    if git_root and git_root != target_path:
        console.print(
            f"[blue]ℹ️  Detected git repository. "
            f"Using git root: {git_root}[/blue]"
        )
        target_path = git_root

    # Create directory structure
    created_dirs = create_directory_structure(target_path)

    # Copy template files (unless minimal mode)
    created_files = []
    skipped_files = []

    if not minimal:
        created_files, skipped_files = copy_template_files(target_path)

    return {
        "path": target_path,
        "created_dirs": created_dirs,
        "created_files": created_files,
        "skipped_files": skipped_files,
        "existing_structure": has_existing,
    }

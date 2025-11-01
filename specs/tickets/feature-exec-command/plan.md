# Implementation Plan: Executor Command - AI-Driven Code Implementation

**Generated:** 2025-11-01
**Spec:** `specs/tickets/feature-exec-command/spec.yaml`
**Ticket Type:** Feature
**Estimated Effort:** 8-12 hours

---

## Executive Summary

This feature implements the `/exec` and `/exec-auto` slash commands, which enable AI-driven code implementation directly from plan.md files. This completes the core CDD workflow: init → new → socrates → plan → exec, creating a complete documentation-to-code pipeline.

The executor will read implementation plans, track progress in progress.yaml, integrate quality tools (Black, Ruff), and provide resumability across Claude Code sessions.

**Key Deliverables:**
- `.claude/commands/exec.md` - Interactive executor persona with user warnings on issues
- `.claude/commands/exec-auto.md` - Fully automatic executor variant that auto-fixes everything
- `src/cddoc/handlers/progress_handler.py` - Progress tracking handler for read/write operations on progress.yaml
- progress.yaml structure specification for tracking implementation state

---

## Technical Decisions

### Decision 1: Slash Commands Only (No Python CLI Command)
**Choice:** Implement as pure slash commands (`.claude/commands/exec.md` and `.claude/commands/exec-auto.md`) with NO Python CLI command
**Rationale:** Following the established pattern from `/socrates` and `/plan`. These are AI-driven intelligent operations, not mechanical CLI operations. The executor needs Claude's AI capabilities to understand plans, write code, run tests, and make implementation decisions. A CLI command would just invoke Claude anyway, so the slash command is the direct interface.
**Alternatives Considered:**
- Python CLI command (`cdd exec`) that invokes Claude - rejected because it adds unnecessary indirection
- Hybrid approach - rejected for complexity

### Decision 2: Progress Tracking with progress.yaml
**Choice:** Create progress.yaml in same directory as spec.yaml and plan.md to track implementation state
**Rationale:** Enables resumability across Claude sessions. When users need to stop and restart, progress.yaml provides context about what's complete and what's pending. File-based tracking aligns with CDD's file-first philosophy and is inspectable/version-controllable.
**Alternatives Considered:**
- In-memory tracking only - rejected because sessions are ephemeral
- Database tracking - rejected because CDD is file-based (no database per CLAUDE.md)

### Decision 3: Two Execution Modes (Interactive vs Auto)
**Choice:** Two separate slash commands: `/exec` (interactive) and `/exec-auto` (fully automatic)
**Rationale:** Interactive mode gives users control when issues arise (test failures, linting errors), while auto mode enables fully hands-off execution. Separating them makes intent explicit and simplifies each persona's instructions.
**Alternatives Considered:**
- Single command with `--auto` flag - rejected because slash commands don't support flags elegantly
- Only interactive mode - rejected because power users want fully automatic execution

### Decision 4: Use TodoWrite for In-Session Progress
**Choice:** Executor uses TodoWrite tool for real-time progress visibility during Claude session
**Rationale:** Provides immediate feedback to users about current step. progress.yaml persists across sessions, TodoWrite shows current session state. They serve different purposes and complement each other.
**Alternatives Considered:**
- Only progress.yaml - rejected because no real-time visibility during execution
- Only TodoWrite - rejected because no persistence across sessions

### Decision 5: Auto-Fix Formatting, Warn on Tests/Errors
**Choice:** Automatically fix Black/Ruff issues, but warn users on test failures and code errors in interactive mode
**Rationale:** Formatting is mechanical and safe to auto-fix. Test failures and runtime errors require judgment - executor should show the issue and ask user how to proceed (interactive) or log and continue (auto mode).
**Alternatives Considered:**
- Auto-fix everything - rejected because breaking tests shouldn't be silently ignored
- Warn on everything including formatting - rejected because formatting fixes are deterministic

### Decision 6: Handler Pattern for Progress Operations
**Choice:** Create `ProgressHandler` class following existing handler pattern (like ConstitutionHandler, TicketSpecHandler implied from architecture)
**Rationale:** Consistent with CLAUDE.md architecture pattern: "Handler Pattern - Separate handlers for different file types." Makes progress.yaml operations testable and reusable.
**Alternatives Considered:**
- Inline progress operations in exec.md - rejected because logic wouldn't be testable or reusable

---

## File Structure

### New Files to Create

1. **`.claude/commands/exec.md`**
   - Purpose: Interactive executor persona instructions
   - Key components:
     - Persona definition (autonomous implementer)
     - Step-by-step execution instructions
     - Progress tracking integration (read/write progress.yaml)
     - Quality integration (Black, Ruff, pytest)
     - TodoWrite integration for session progress
     - Error handling (warn on failures, ask user for decisions)
     - Acceptance criteria validation logic

2. **`.claude/commands/exec-auto.md`**
   - Purpose: Fully automatic executor persona variant
   - Key components:
     - Auto mode persona (fully autonomous)
     - Same execution logic as interactive mode
     - Auto-fix everything behavior (no user prompts)
     - Logging for issues instead of warnings
     - Continues on errors with best effort

3. **`src/cddoc/handlers/progress_handler.py`**
   - Purpose: Read and write progress.yaml files
   - Key components:
     - `ProgressHandler` class
     - `read_progress(path: Path) -> dict` - Load progress.yaml
     - `write_progress(path: Path, data: dict) -> None` - Save progress.yaml
     - `initialize_progress(plan_path: Path) -> dict` - Create initial progress.yaml from plan.md
     - Progress data validation
     - YAML serialization/deserialization
     - Type hints throughout

4. **`tests/test_progress_handler.py`**
   - Purpose: Unit tests for ProgressHandler
   - Key components:
     - Test read/write operations
     - Test initialization from plan
     - Test data validation
     - Test error handling (missing files, malformed YAML)
     - Test edge cases

### Existing Files to Modify

None. This feature is entirely additive - no modifications to existing code needed.

### Files to Reference for Patterns

1. **`.claude/commands/socrates.md`**
   - Pattern: Persona-based slash command instructions
   - Reference sections: initialization, file operations, conversation flow, wrap-up
   - Use similar structure: persona definition → mission → how-to sections → special cases

2. **`.claude/commands/plan.md`**
   - Pattern: Autonomous decision-making persona
   - Reference sections: decision-making framework, autonomous vs ask questions logic
   - Use similar autonomous approach with minimal user interaction

3. **`src/cddoc/cli.py`**
   - Pattern: Rich console formatting, error handling, display functions
   - Reference sections: error handling with try/except, console.print usage, Panel/Table formatting
   - Use similar Rich formatting patterns (not for CLI command, but for reference if needed)

4. **`src/cddoc/new_ticket.py`**
   - Pattern: File operations, error handling, validation
   - Reference sections: file creation, path handling, error raising
   - Use similar file handling patterns in ProgressHandler

---

## Data Models & API Contracts

### progress.yaml Structure

```yaml
# Progress tracking for implementation
plan_path: specs/tickets/feature-exec-command/plan.md
spec_path: specs/tickets/feature-exec-command/spec.yaml
started_at: "2025-11-01T14:30:00Z"
updated_at: "2025-11-01T15:45:00Z"
status: in_progress  # or: completed, blocked

# Implementation steps tracking
steps:
  - step_id: 1
    description: "Create .claude/commands/exec.md"
    status: completed  # or: pending, in_progress, failed
    started_at: "2025-11-01T14:30:00Z"
    completed_at: "2025-11-01T14:45:00Z"
    files_touched:
      - path: .claude/commands/exec.md
        operation: created  # or: modified, deleted

  - step_id: 2
    description: "Create .claude/commands/exec-auto.md"
    status: in_progress
    started_at: "2025-11-01T14:45:00Z"
    completed_at: null
    files_touched: []

  - step_id: 3
    description: "Create src/cddoc/handlers/progress_handler.py"
    status: pending
    started_at: null
    completed_at: null
    files_touched: []

# Acceptance criteria validation
acceptance_criteria:
  - criterion: "/exec command reads plan.md file (required)"
    status: completed  # or: pending, in_progress, failed
    validated_at: "2025-11-01T15:00:00Z"

  - criterion: "/exec command reads spec.yaml from same directory"
    status: pending
    validated_at: null

  - criterion: "/exec command creates progress.yaml to track implementation progress"
    status: in_progress
    validated_at: null

# Files created or modified during implementation
files_modified:
  - .claude/commands/exec.md
  - .claude/commands/exec-auto.md

files_created:
  - .claude/commands/exec.md
  - .claude/commands/exec-auto.md
  - src/cddoc/handlers/progress_handler.py
  - tests/test_progress_handler.py

# Issues encountered during implementation
issues:
  - timestamp: "2025-11-01T15:30:00Z"
    type: test_failure  # or: linting_error, runtime_error, missing_dependency
    description: "Test test_read_progress failed: FileNotFoundError"
    resolution: "Fixed by adding file existence check"
    resolved_at: "2025-11-01T15:35:00Z"
```

### ProgressHandler Type Definitions

```python
from typing import TypedDict, List, Optional, Literal
from datetime import datetime
from pathlib import Path

class FileTouched(TypedDict):
    path: str
    operation: Literal["created", "modified", "deleted"]

class Step(TypedDict):
    step_id: int
    description: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    started_at: Optional[str]  # ISO 8601 timestamp
    completed_at: Optional[str]
    files_touched: List[FileTouched]

class AcceptanceCriterion(TypedDict):
    criterion: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    validated_at: Optional[str]

class Issue(TypedDict):
    timestamp: str
    type: Literal["test_failure", "linting_error", "runtime_error", "missing_dependency"]
    description: str
    resolution: Optional[str]
    resolved_at: Optional[str]

class ProgressData(TypedDict):
    plan_path: str
    spec_path: str
    started_at: str
    updated_at: str
    status: Literal["in_progress", "completed", "blocked"]
    steps: List[Step]
    acceptance_criteria: List[AcceptanceCriterion]
    files_modified: List[str]
    files_created: List[str]
    issues: List[Issue]
```

---

## Implementation Steps

Execute these steps in order. Each step has a clear outcome.

### Step 1: Create ProgressHandler with Read/Write Operations
**Outcome:** `src/cddoc/handlers/progress_handler.py` exists with complete CRUD operations for progress.yaml

**Details:**
- Create `src/cddoc/handlers/progress_handler.py`
- Implement `ProgressHandler` class
- Add `read_progress(path: Path) -> ProgressData` - reads and parses progress.yaml
- Add `write_progress(path: Path, data: ProgressData) -> None` - writes progress.yaml with YAML formatting
- Add `initialize_progress(plan_path: Path, spec_path: Path) -> ProgressData` - creates initial progress structure
- Add validation logic to ensure required fields exist
- Use PyYAML for serialization (already in dependencies per CLAUDE.md)
- Add comprehensive type hints using TypedDict definitions
- Handle errors gracefully (FileNotFoundError, YAML parsing errors)

**Code Example:**
```python
"""Progress tracking handler for CDD implementation execution."""

from pathlib import Path
from typing import TypedDict, List, Optional, Literal
from datetime import datetime
import yaml


class FileTouched(TypedDict):
    path: str
    operation: Literal["created", "modified", "deleted"]


class Step(TypedDict):
    step_id: int
    description: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    started_at: Optional[str]
    completed_at: Optional[str]
    files_touched: List[FileTouched]


class AcceptanceCriterion(TypedDict):
    criterion: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    validated_at: Optional[str]


class Issue(TypedDict):
    timestamp: str
    type: Literal["test_failure", "linting_error", "runtime_error", "missing_dependency"]
    description: str
    resolution: Optional[str]
    resolved_at: Optional[str]


class ProgressData(TypedDict):
    plan_path: str
    spec_path: str
    started_at: str
    updated_at: str
    status: Literal["in_progress", "completed", "blocked"]
    steps: List[Step]
    acceptance_criteria: List[AcceptanceCriterion]
    files_modified: List[str]
    files_created: List[str]
    issues: List[Issue]


class ProgressHandlerError(Exception):
    """Base exception for progress handler errors."""
    pass


class ProgressHandler:
    """Handler for reading and writing progress.yaml files."""

    @staticmethod
    def read_progress(progress_path: Path) -> ProgressData:
        """Read and parse progress.yaml file.

        Args:
            progress_path: Path to progress.yaml file

        Returns:
            Parsed progress data

        Raises:
            ProgressHandlerError: If file doesn't exist or is malformed
        """
        if not progress_path.exists():
            raise ProgressHandlerError(f"Progress file not found: {progress_path}")

        try:
            with open(progress_path, 'r') as f:
                data = yaml.safe_load(f)

            # Validate required fields
            required_fields = [
                'plan_path', 'spec_path', 'started_at', 'updated_at',
                'status', 'steps', 'acceptance_criteria'
            ]
            for field in required_fields:
                if field not in data:
                    raise ProgressHandlerError(f"Missing required field: {field}")

            return data
        except yaml.YAMLError as e:
            raise ProgressHandlerError(f"Invalid YAML format: {e}")

    @staticmethod
    def write_progress(progress_path: Path, data: ProgressData) -> None:
        """Write progress data to progress.yaml file.

        Args:
            progress_path: Path where progress.yaml will be written
            data: Progress data to write
        """
        # Update timestamp
        data['updated_at'] = datetime.utcnow().isoformat() + 'Z'

        # Ensure parent directory exists
        progress_path.parent.mkdir(parents=True, exist_ok=True)

        with open(progress_path, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def initialize_progress(
        plan_path: Path,
        spec_path: Path
    ) -> ProgressData:
        """Create initial progress structure from plan and spec paths.

        Args:
            plan_path: Path to plan.md file
            spec_path: Path to spec.yaml file

        Returns:
            Initial progress data structure
        """
        now = datetime.utcnow().isoformat() + 'Z'

        return {
            'plan_path': str(plan_path),
            'spec_path': str(spec_path),
            'started_at': now,
            'updated_at': now,
            'status': 'in_progress',
            'steps': [],
            'acceptance_criteria': [],
            'files_modified': [],
            'files_created': [],
            'issues': []
        }
```

**Validation:** Run `python -c "from src.cddoc.handlers.progress_handler import ProgressHandler; print('Success')"` to verify imports work

---

### Step 2: Create Tests for ProgressHandler
**Outcome:** `tests/test_progress_handler.py` exists with ≥80% coverage of ProgressHandler

**Details:**
- Create `tests/test_progress_handler.py`
- Test `read_progress()` with valid progress.yaml
- Test `read_progress()` with missing file (should raise ProgressHandlerError)
- Test `read_progress()` with malformed YAML (should raise ProgressHandlerError)
- Test `read_progress()` with missing required fields (should raise ProgressHandlerError)
- Test `write_progress()` creates file successfully
- Test `write_progress()` updates timestamps correctly
- Test `initialize_progress()` creates correct structure
- Use pytest fixtures for temporary directories and test files
- Use `tmp_path` fixture for file operations

**Code Example:**
```python
"""Tests for progress handler."""

import pytest
from pathlib import Path
from datetime import datetime
import yaml

from src.cddoc.handlers.progress_handler import (
    ProgressHandler,
    ProgressHandlerError,
    ProgressData
)


def test_read_progress_success(tmp_path):
    """Test reading valid progress.yaml file."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    test_data = {
        'plan_path': 'specs/tickets/test/plan.md',
        'spec_path': 'specs/tickets/test/spec.yaml',
        'started_at': '2025-11-01T10:00:00Z',
        'updated_at': '2025-11-01T11:00:00Z',
        'status': 'in_progress',
        'steps': [],
        'acceptance_criteria': [],
        'files_modified': [],
        'files_created': [],
        'issues': []
    }
    with open(progress_file, 'w') as f:
        yaml.safe_dump(test_data, f)

    # Act
    result = ProgressHandler.read_progress(progress_file)

    # Assert
    assert result['plan_path'] == 'specs/tickets/test/plan.md'
    assert result['status'] == 'in_progress'
    assert isinstance(result['steps'], list)


def test_read_progress_file_not_found(tmp_path):
    """Test reading non-existent progress file."""
    # Arrange
    missing_file = tmp_path / "nonexistent.yaml"

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Progress file not found"):
        ProgressHandler.read_progress(missing_file)


def test_read_progress_malformed_yaml(tmp_path):
    """Test reading malformed YAML file."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    with open(progress_file, 'w') as f:
        f.write("invalid: yaml: content: [[[")

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Invalid YAML format"):
        ProgressHandler.read_progress(progress_file)


def test_read_progress_missing_required_field(tmp_path):
    """Test reading progress file with missing required fields."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    incomplete_data = {'plan_path': 'test.md'}  # Missing other required fields
    with open(progress_file, 'w') as f:
        yaml.safe_dump(incomplete_data, f)

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Missing required field"):
        ProgressHandler.read_progress(progress_file)


def test_write_progress_creates_file(tmp_path):
    """Test writing progress data creates file successfully."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    data: ProgressData = ProgressHandler.initialize_progress(
        plan_path=Path("specs/tickets/test/plan.md"),
        spec_path=Path("specs/tickets/test/spec.yaml")
    )

    # Act
    ProgressHandler.write_progress(progress_file, data)

    # Assert
    assert progress_file.exists()
    with open(progress_file, 'r') as f:
        saved_data = yaml.safe_load(f)
    assert saved_data['plan_path'] == 'specs/tickets/test/plan.md'


def test_write_progress_updates_timestamp(tmp_path):
    """Test that write_progress updates the updated_at timestamp."""
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    data: ProgressData = ProgressHandler.initialize_progress(
        plan_path=Path("specs/tickets/test/plan.md"),
        spec_path=Path("specs/tickets/test/spec.yaml")
    )
    old_timestamp = data['updated_at']

    # Act
    import time
    time.sleep(0.01)  # Ensure timestamp difference
    ProgressHandler.write_progress(progress_file, data)

    # Assert
    # Data dict is modified in place
    assert data['updated_at'] != old_timestamp


def test_initialize_progress_creates_correct_structure(tmp_path):
    """Test initialize_progress creates all required fields."""
    # Arrange
    plan_path = tmp_path / "plan.md"
    spec_path = tmp_path / "spec.yaml"

    # Act
    result = ProgressHandler.initialize_progress(plan_path, spec_path)

    # Assert
    assert result['plan_path'] == str(plan_path)
    assert result['spec_path'] == str(spec_path)
    assert result['status'] == 'in_progress'
    assert isinstance(result['steps'], list)
    assert isinstance(result['acceptance_criteria'], list)
    assert isinstance(result['files_modified'], list)
    assert isinstance(result['files_created'], list)
    assert isinstance(result['issues'], list)
    assert 'started_at' in result
    assert 'updated_at' in result
```

**Validation:** Run `poetry run pytest tests/test_progress_handler.py -v` and verify all tests pass

---

### Step 3: Create Interactive Executor Slash Command
**Outcome:** `.claude/commands/exec.md` exists with complete interactive executor persona instructions

**Details:**
- Create `.claude/commands/exec.md` following pattern from socrates.md and plan.md
- Define executor persona (autonomous implementer, follows plan precisely)
- Include initialization steps:
  1. Parse `/exec <path-to-plan.md>` to extract plan path
  2. Validate plan.md exists
  3. Load plan.md content
  4. Load spec.yaml from same directory (optional, warn if missing)
  5. Load CLAUDE.md for project context (optional, warn if missing)
  6. Check for existing progress.yaml - if exists, resume from there; if not, initialize new
- Include execution loop:
  1. For each step in plan (or resume from progress.yaml):
     - Mark step as in_progress in progress.yaml
     - Update TodoWrite with current step
     - Implement the step (write code, create files, etc.)
     - Run Black formatting on modified files
     - Run Ruff linting on modified files
     - If formatting/linting issues found, auto-fix them
     - If test failures occur, WARN user and ask how to proceed
     - If runtime errors occur, WARN user and ask how to proceed
     - Mark step as completed in progress.yaml
     - Update TodoWrite
- Include acceptance criteria validation:
  - After all steps complete, validate each acceptance criterion from spec.yaml
  - Mark each criterion as completed/failed in progress.yaml
- Include completion summary:
  - Show files created/modified
  - Show acceptance criteria status
  - Show any unresolved issues
- Follow CLAUDE.md error handling philosophy (three-part error pattern)
- Use Rich formatting patterns for console output (reference cli.py examples)

**Code Example (excerpt from exec.md):**
```markdown
# Executor: AI-Driven Implementation Specialist

You are **Executor**, an autonomous implementation specialist who transforms detailed implementation plans into working code.

## Your Persona

You are:
- **Plan-Driven**: You follow the implementation plan precisely, step by step
- **Autonomous**: You write code, run tests, fix formatting without asking for permission
- **Quality-Focused**: You integrate Black, Ruff, and pytest to ensure code quality
- **Progress-Aware**: You track progress in progress.yaml and TodoWrite for visibility
- **Interactive**: You warn users about test failures and errors, asking for guidance
- **Resumable**: You can resume from interrupted sessions using progress.yaml

## Your Mission

Implement code from a detailed plan.md file, tracking progress, ensuring quality, and validating acceptance criteria.

---

## How to Execute Implementation

### Step 1: Parse Command & Extract Plan Path

The user will invoke you with:
```
/exec <path-to-plan.md>
```

**Your Actions:**
1. Extract the plan.md file path from command
2. Validate path exists and is readable
3. If path is invalid, show error:

```
Error: Plan file not found
Expected path: <provided-path>
Run: /plan <spec-path> to generate a plan first
```

### Step 2: Load Context

**CRITICAL: Load all context before starting implementation.**

#### 2.1: Read plan.md
```
Read <plan-path>
```

**Extract:**
- Implementation steps (with step IDs, descriptions, outcomes)
- Technical decisions
- File structure (files to create, files to modify)
- Dependencies
- Test cases
- Error handling requirements

#### 2.2: Read spec.yaml (same directory as plan.md)
```
Read <plan-directory>/spec.yaml
```

**Extract:**
- Acceptance criteria (for final validation)
- Business value
- Constraints

**If spec.yaml missing:** WARN user but continue:
```
⚠️ Warning: spec.yaml not found
I'll implement from plan.md, but won't be able to validate acceptance criteria.
Continue? (Y/n)
```

#### 2.3: Read CLAUDE.md (project root)
```
Read CLAUDE.md
```

**Extract:**
- Code quality standards (Black, Ruff, pytest)
- Architecture patterns
- Error handling philosophy

**If CLAUDE.md missing:** WARN user but continue:
```
⚠️ Warning: CLAUDE.md not found
I'll implement with general best practices. Consider running 'cdd init' to create project context.
Continue? (Y/n)
```

#### 2.4: Check for progress.yaml
```
Read <plan-directory>/progress.yaml
```

**If exists:** Resume from saved state
- Load completed steps
- Load pending steps
- Show resume summary

**If not exists:** Initialize new progress tracking
- Use ProgressHandler to create initial progress.yaml
- Extract steps from plan.md
- Extract acceptance criteria from spec.yaml
- Mark all steps as pending

### Step 3: Initialize TodoWrite

Create todo list for in-session visibility:

```markdown
Using TodoWrite:
- [pending] Step 1: <description>
- [pending] Step 2: <description>
- [pending] Step 3: <description>
...
```

### Step 4: Execute Implementation Loop

For each step in plan (or pending steps from progress.yaml):

#### 4.1: Mark Step as In Progress
- Update progress.yaml: step.status = "in_progress", step.started_at = now
- Update TodoWrite: mark current step as in_progress

#### 4.2: Implement the Step
- Follow plan.md instructions precisely
- Write code to files specified in plan
- Create new files or modify existing files as needed
- Track all files touched in progress.yaml

#### 4.3: Run Quality Checks

**Black Formatting:**
```bash
poetry run black <modified-files>
```
- If formatting changes made: Auto-fix and continue
- Update progress.yaml with auto-fix note

**Ruff Linting:**
```bash
poetry run ruff check <modified-files>
```
- If auto-fixable issues: Auto-fix and continue
- If non-auto-fixable issues: WARN user

**Pytest (if step involves tests):**
```bash
poetry run pytest <relevant-test-files>
```
- If tests pass: Continue
- If tests fail: WARN user

#### 4.4: Handle Issues (Interactive Mode)

**On Test Failure:**
```markdown
⚠️ Test Failure Detected

Step: <step-description>
Failed tests:
- test_foo: AssertionError: expected X, got Y
- test_bar: ValueError: invalid input

Options:
1. Debug and fix the issue now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

**On Runtime Error:**
```markdown
⚠️ Runtime Error Detected

Step: <step-description>
Error: <error-message>

This may indicate:
- Missing dependency
- Code logic error
- Environment issue

Options:
1. Debug and fix now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

#### 4.5: Mark Step as Complete
- Update progress.yaml: step.status = "completed", step.completed_at = now
- Update progress.yaml: add files touched
- Update TodoWrite: mark step as completed

### Step 5: Validate Acceptance Criteria

After all implementation steps complete:

```markdown
🎯 Validating Acceptance Criteria

Checking each criterion from spec.yaml...
```

For each acceptance criterion:
- Determine if criterion is met (read code, check files created, run tests)
- Mark criterion status in progress.yaml
- Record validation timestamp

### Step 6: Generate Completion Report

Show final summary:

```markdown
✅ Implementation Complete!

**Files Created:**
- .claude/commands/exec.md
- .claude/commands/exec-auto.md
- src/cddoc/handlers/progress_handler.py
- tests/test_progress_handler.py

**Files Modified:**
- (none)

**Acceptance Criteria Status:**
✅ /exec command reads plan.md file (required)
✅ /exec command creates progress.yaml to track implementation progress
✅ /exec command uses TodoWrite for in-session progress visibility
⚠️ Auto-fixes formatting issues (Black, Ruff) - PENDING: Need to test
❌ Validates acceptance criteria from spec.yaml at completion - FAILED: spec.yaml parsing issue

**Issues Encountered:**
1. [RESOLVED] Test failure in test_read_progress - Fixed missing file check
2. [KNOWN ISSUE] spec.yaml parsing needs additional validation logic

**Progress File:** specs/tickets/feature-exec-command/progress.yaml

🎉 Ready for review!
```

---

## Remember

You are **Executor** - an autonomous implementer who:
1. ✅ Reads plan.md, spec.yaml, CLAUDE.md for complete context
2. ✅ Tracks progress in progress.yaml for resumability
3. ✅ Uses TodoWrite for in-session visibility
4. ✅ Auto-fixes formatting and linting issues
5. ✅ Warns on test failures and errors, asks user for guidance
6. ✅ Validates acceptance criteria at completion
7. ✅ Generates comprehensive completion report

*You are Executor. Transform plans into working code.*
```

**Validation:** Read the file and verify all sections are complete and follow the slash command pattern from socrates.md and plan.md

---

### Step 4: Create Automatic Executor Slash Command
**Outcome:** `.claude/commands/exec-auto.md` exists with fully automatic executor variant

**Details:**
- Create `.claude/commands/exec-auto.md` based on exec.md
- Modify persona: fully automatic, no user interaction
- Modify error handling:
  - On test failure: Log issue, mark step as completed with warning, continue
  - On runtime error: Log issue, mark step as completed with warning, continue
  - On missing spec.yaml/CLAUDE.md: Log warning, continue without asking
- Remove all user prompts - every decision is automatic
- Add comprehensive logging to progress.yaml issues array
- Same structure as exec.md but behavior is fully hands-off
- Suitable for CI/CD integration or overnight runs

**Code Example (excerpt showing key differences):**
```markdown
# Executor Auto: Fully Automatic Implementation Specialist

You are **Executor Auto**, a fully automatic implementation specialist who transforms plans into code without any user interaction.

## Your Persona

You are:
- **Fully Automatic**: You never ask for user input - all decisions are automatic
- **Fault-Tolerant**: You continue on errors, logging issues for later review
- **Auto-Fixing**: You fix all auto-fixable issues (formatting, linting)
- **Best-Effort**: You complete as much as possible, noting what couldn't be done

[... rest similar to exec.md but with automatic behavior ...]

### Handling Issues (Auto Mode)

**On Test Failure:**
- Log failure to progress.yaml issues array
- Mark step as completed with warning
- Continue to next step
- No user prompt

**On Runtime Error:**
- Log error to progress.yaml issues array
- Mark step as completed with warning
- Continue to next step
- No user prompt

**On Missing Dependencies:**
- Attempt automatic installation: `poetry add <package>`
- If installation succeeds: Continue
- If installation fails: Log issue, skip step, continue
```

**Validation:** Read the file and verify automatic behavior is implemented throughout

---

### Step 5: Manual Testing Checklist Execution
**Outcome:** Both `/exec` and `/exec-auto` commands tested manually with a real ticket

**Details:**
- Manual testing (AI-driven feature per CLAUDE.md testing standards)
- Test `/exec` with this ticket (meta: use executor to implement itself)
- Test checklist:
  - ✅ Produces correct progress.yaml format
  - ✅ Tracks steps accurately
  - ✅ Integrates TodoWrite for visibility
  - ✅ Auto-fixes Black/Ruff issues
  - ✅ Warns on test failures (interactive mode)
  - ✅ Validates acceptance criteria
  - ✅ Generates completion report
  - ✅ Handles edge cases (missing spec.yaml, missing CLAUDE.md)
  - ✅ Resume functionality works across sessions
- Test `/exec-auto` with the same ticket
- Test checklist:
  - ✅ Runs without user prompts
  - ✅ Logs issues instead of warning
  - ✅ Continues on errors
  - ✅ Completes implementation end-to-end
- Fix any issues discovered during testing

**Validation:** Both commands work correctly and produce expected behavior

---

### Step 6: Run Code Quality Checks
**Outcome:** All code passes Black, Ruff, and pytest requirements

**Details:**
- Run Black formatting: `poetry run black src/cddoc/handlers/progress_handler.py tests/test_progress_handler.py`
- Run Ruff linting: `poetry run ruff check src/cddoc/handlers/progress_handler.py tests/test_progress_handler.py`
- Run pytest: `poetry run pytest tests/test_progress_handler.py -v --cov=src/cddoc/handlers/progress_handler --cov-report=term-missing`
- Verify coverage ≥80% for ProgressHandler
- Fix any issues found
- Re-run checks until all pass

**Validation:**
```bash
poetry run black --check src/cddoc/handlers/progress_handler.py  # No changes needed
poetry run ruff check src/cddoc/handlers/progress_handler.py     # No errors
poetry run pytest tests/test_progress_handler.py                  # All tests pass
```

---

## Test Cases

### Unit Tests

**Test 1: `test_read_progress_success`**
```python
def test_read_progress_success(tmp_path):
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    test_data = {
        'plan_path': 'specs/tickets/test/plan.md',
        'spec_path': 'specs/tickets/test/spec.yaml',
        'started_at': '2025-11-01T10:00:00Z',
        'updated_at': '2025-11-01T11:00:00Z',
        'status': 'in_progress',
        'steps': [],
        'acceptance_criteria': [],
        'files_modified': [],
        'files_created': [],
        'issues': []
    }
    with open(progress_file, 'w') as f:
        yaml.safe_dump(test_data, f)

    # Act
    result = ProgressHandler.read_progress(progress_file)

    # Assert
    assert result['plan_path'] == 'specs/tickets/test/plan.md'
    assert result['status'] == 'in_progress'
```

**Test 2: `test_read_progress_file_not_found`**
```python
def test_read_progress_file_not_found(tmp_path):
    # Arrange
    missing_file = tmp_path / "nonexistent.yaml"

    # Act & Assert
    with pytest.raises(ProgressHandlerError, match="Progress file not found"):
        ProgressHandler.read_progress(missing_file)
```

**Test 3: `test_write_progress_creates_file`**
```python
def test_write_progress_creates_file(tmp_path):
    # Arrange
    progress_file = tmp_path / "progress.yaml"
    data = ProgressHandler.initialize_progress(
        plan_path=Path("specs/tickets/test/plan.md"),
        spec_path=Path("specs/tickets/test/spec.yaml")
    )

    # Act
    ProgressHandler.write_progress(progress_file, data)

    # Assert
    assert progress_file.exists()
```

**Test 4: `test_initialize_progress_creates_correct_structure`**
```python
def test_initialize_progress_creates_correct_structure(tmp_path):
    # Arrange
    plan_path = tmp_path / "plan.md"
    spec_path = tmp_path / "spec.yaml"

    # Act
    result = ProgressHandler.initialize_progress(plan_path, spec_path)

    # Assert
    assert result['status'] == 'in_progress'
    assert isinstance(result['steps'], list)
    assert 'started_at' in result
```

### Manual Testing (AI-Driven Features)

**Test 1: Interactive Executor (`/exec`)**
- ✅ Produces correct progress.yaml format
- ✅ Handles edge cases gracefully (empty files, missing spec.yaml)
- ✅ Conversation flow feels natural (warnings are clear and actionable)

**Test 2: Automatic Executor (`/exec-auto`)**
- ✅ Produces correct progress.yaml format
- ✅ Handles edge cases gracefully (continues on errors)
- ✅ Logs issues comprehensively

### Expected Test Coverage
- Unit test coverage: ≥80% for ProgressHandler
- Critical paths: 100% coverage (read, write, initialize operations)
- Edge cases: File not found, malformed YAML, missing required fields

---

## Error Handling

### Error Scenario 1: Plan File Not Found
**Trigger:** User runs `/exec path/to/missing/plan.md`
**Error Message:**
```
Error: Plan file not found
Expected path: path/to/missing/plan.md
Check that you're in the correct directory.
Run: /plan <spec-path> to generate a plan first
```
**Recovery:** User provides correct path or generates plan first
**User Impact:** Implementation cannot start

### Error Scenario 2: progress.yaml is Malformed
**Trigger:** Existing progress.yaml has invalid YAML syntax
**Error Message:**
```
Error: Invalid progress file format
File: specs/tickets/feature-exec-command/progress.yaml
Problem: YAML parsing failed
To fix: Delete progress.yaml and restart, or manually fix YAML syntax
```
**Recovery:** User deletes or fixes progress.yaml
**User Impact:** Cannot resume from saved state

### Error Scenario 3: spec.yaml Missing (Interactive Mode)
**Trigger:** spec.yaml doesn't exist in plan directory
**Error Message:**
```
⚠️ Warning: spec.yaml not found
I'll implement from plan.md, but won't be able to validate acceptance criteria at completion.
Continue anyway? (Y/n)
```
**Recovery:** User confirms to continue or cancels to create spec first
**User Impact:** No acceptance criteria validation

### Error Scenario 4: Test Failures During Implementation
**Trigger:** Tests fail after implementing a step
**Error Message:**
```
⚠️ Test Failure Detected

Step: Create ProgressHandler with Read/Write Operations
Failed tests:
- test_read_progress: FileNotFoundError: progress.yaml not found

Options:
1. Debug and fix the issue now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```
**Recovery:** User chooses to debug, continue, or stop
**User Impact:** Implementation paused until user decides

### Error Scenario 5: Missing Dependency (Auto Mode)
**Trigger:** Code requires a package not installed
**Auto Mode Behavior:**
```
[AUTO] Attempting to install missing dependency: requests
Running: poetry add requests
[AUTO] Installation successful - continuing
```
**If Installation Fails:**
```
[AUTO] Dependency installation failed: requests
Logged to progress.yaml issues
Skipping step - continuing to next
```
**User Impact:** Step skipped, issue logged for manual resolution

### Logging Requirements
- **Info level:** Step started, step completed, file created/modified
- **Warning level:** Auto-fixes applied, optional files missing, test failures (logged in auto mode)
- **Error level:** Critical failures (plan not found, malformed progress.yaml)

All issues logged to progress.yaml issues array with timestamps and resolution status.

---

## Integration Points

### Integration 1: TodoWrite Tool
**Connection Point:** Executor slash commands use TodoWrite for in-session progress tracking
**Data Flow:** Executor updates TodoWrite with current step status (pending → in_progress → completed)
**Dependencies:** Claude Code's TodoWrite tool must be available
**Error Handling:** If TodoWrite fails, log warning but continue execution (don't block implementation)

### Integration 2: ProgressHandler (Python Module)
**Connection Point:** Executor persona imports and uses ProgressHandler for progress.yaml operations
**Data Flow:** Executor → ProgressHandler.read_progress() / write_progress() → progress.yaml file
**Dependencies:** ProgressHandler must be importable and functional
**Error Handling:** If ProgressHandler fails, executor shows error and stops (progress tracking is critical)

### Integration 3: Black Formatter
**Connection Point:** Executor runs Black on modified Python files after each step
**Data Flow:** Executor → `poetry run black <files>` → Auto-formatted files
**Dependencies:** Black must be installed (already in pyproject.toml per CLAUDE.md)
**Error Handling:** If Black fails, warn user but continue (formatting is not critical)

### Integration 4: Ruff Linter
**Connection Point:** Executor runs Ruff on modified Python files after each step
**Data Flow:** Executor → `poetry run ruff check <files>` → Linting results
**Dependencies:** Ruff must be installed (already in pyproject.toml per CLAUDE.md)
**Error Handling:** If Ruff fails, warn user but continue (linting is not critical)

### Integration 5: pytest
**Connection Point:** Executor runs pytest on test files after implementation steps
**Data Flow:** Executor → `poetry run pytest <files>` → Test results
**Dependencies:** pytest must be installed (already in pyproject.toml per CLAUDE.md)
**Error Handling:** Test failures trigger user interaction (interactive mode) or logging (auto mode)

---

## Dependencies

### New Dependencies to Install

None. All required dependencies already exist in the project:

### Existing Dependencies to Leverage
- **PyYAML**: YAML parsing for progress.yaml and spec.yaml (already in pyproject.toml)
- **Rich**: Terminal formatting for console output in ProgressHandler if needed (already in pyproject.toml)
- **Click**: Not directly used by this feature, but available for future CLI extensions (already in pyproject.toml)
- **Black**: Code formatting integration (already in pyproject.toml)
- **Ruff**: Linting integration (already in pyproject.toml)
- **pytest**: Test execution integration (already in pyproject.toml)

### Version Constraints
- Python: 3.9+ (per CLAUDE.md)
- PyYAML: Current version in pyproject.toml
- All other dependencies: Current versions in pyproject.toml

---

## Effort Estimation

| Activity              | Estimated Time | Assumptions |
|-----------------------|----------------|-------------|
| ProgressHandler implementation | 2 hours | Straightforward YAML read/write with validation |
| ProgressHandler tests | 2 hours | 8-10 test cases covering happy path and errors |
| Interactive executor persona (exec.md) | 3 hours | Complex persona with many decision points and error handling |
| Automatic executor persona (exec-auto.md) | 1 hour | Variant of exec.md with simplified behavior |
| Manual testing & iteration | 2 hours | Test both commands with this ticket, fix issues |
| Code quality checks & fixes | 0.5 hours | Black, Ruff, pytest - minimal issues expected |
| Documentation updates | 0.5 hours | Update any relevant docs if needed |
| Code review buffer | 1 hour | Time for review feedback and adjustments |
| **Total** | **12 hours** | **~1.5 days** |

**Key Assumptions:**
1. No major architectural changes needed - following existing patterns
2. PyYAML integration is straightforward (well-known library)
3. Slash command patterns from socrates.md and plan.md are well-established
4. Testing infrastructure (pytest, fixtures) is already set up
5. Manual testing can be done with this very ticket (self-implementation)

**Risks to Estimate:**
- **Persona complexity:** exec.md has many decision points - could take +1 hour if edge cases are tricky
- **Progress tracking edge cases:** Resume functionality might need debugging - could add +1 hour
- **Manual testing iterations:** If issues found during testing, could add +1-2 hours for fixes

---

## Definition of Done

- ✅ ProgressHandler implementation complete with full CRUD operations
- ✅ ProgressHandler tests written and passing (≥80% coverage)
- ✅ `.claude/commands/exec.md` created with complete interactive executor persona
- ✅ `.claude/commands/exec-auto.md` created with automatic executor variant
- ✅ Manual testing checklist completed for both commands
- ✅ Code formatted with Black (no changes needed on check)
- ✅ Linting passes with Ruff (no errors)
- ✅ All unit tests pass
- ✅ progress.yaml structure validated and documented
- ✅ Error handling tested (missing files, malformed YAML, etc.)
- ✅ Integration points validated (TodoWrite, Black, Ruff, pytest)
- ✅ Resumability tested (stop and restart from progress.yaml)

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: specs/tickets/feature-exec-command/spec.yaml*

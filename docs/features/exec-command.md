# Feature: Executor - Interactive AI Implementation

> Living documentation for the Executor AI implementation specialist

**Status:** Production
**Version:** 0.1.0
**Last Updated:** 2025-11-03

---

## Overview

Executor is an **interactive AI implementation specialist** that transforms detailed implementation plans into working code. After Planner creates a comprehensive plan.md, Executor reads it step-by-step, writes code, runs quality checks, and validates acceptance criteria - all while keeping you informed and asking for guidance when needed.

**Why it exists:**

After Planner generates a detailed plan, developers face implementation execution. Executor bridges the gap between *plan* and *working code* by:
- Following implementation plans step-by-step with precision
- Writing code that matches project patterns and standards
- Running quality gates automatically (Black, Ruff, pytest)
- Tracking progress for resumability (progress.yaml + TodoWrite)
- Validating acceptance criteria from spec.yaml
- Asking for guidance on test failures or errors (interactive mode)

**Key Capabilities:**
- Plan-driven execution (follows plan.md precisely)
- Progress tracking (resume from interruptions)
- Quality automation (auto-fix formatting and linting)
- Interactive error handling (asks user when blocked)
- Acceptance criteria validation
- Comprehensive completion reporting
- Shorthand ticket paths (`/exec feature-auth`)

**Philosophy:**

Executor embodies the framework's implementation tier: **"Clear Plan + Full Context = Confident Implementation."** By loading complete context (plan.md, spec.yaml, CLAUDE.md) and following structured steps, Executor transforms detailed plans into working code while maintaining visibility and quality.

---

## Current Implementation

### How It Works Today

**User Perspective:**
1. Developer runs `/exec feature-user-auth` (or `/exec specs/tickets/feature-user-auth/plan.md`)
2. Executor loads context silently (plan.md, spec.yaml, CLAUDE.md, progress.yaml if resuming)
3. Updates spec.yaml status to "in_progress" (if starting fresh)
4. Creates progress.yaml for tracking
5. Initializes TodoWrite for in-session visibility
6. Executes implementation steps one by one
7. Runs quality checks (Black, Ruff, pytest) after each step
8. Asks for guidance on test failures or errors (interactive)
9. Validates acceptance criteria at completion
10. Shows comprehensive completion report
11. Updates spec.yaml status to "completed"
12. Archives ticket to specs/archive/ directory
13. Updates archived spec.yaml status to "archived"

**Core Behavior:**
- **Plan-driven**: Follows plan.md implementation steps precisely
- **Progress-tracked**: Maintains progress.yaml for resumability
- **Quality-focused**: Auto-fixes formatting/linting, runs tests
- **Interactive**: Warns on errors, asks user for guidance when blocked
- **Resumable**: Can continue from interruption using progress.yaml
- **Validating**: Checks acceptance criteria from spec.yaml at completion

### Architecture Overview

**Intelligence Layer Integration:**
```
CDD Framework Architecture
├── Mechanical Layer (CLI)
│   ├── cdd init - Framework initialization
│   └── cdd new - Ticket/doc creation
└── Intelligence Layer (Slash Commands)
    ├── /socrates - Requirements gathering
    ├── /plan - Implementation planning
    └── /exec - AI-assisted implementation ← YOU ARE HERE
```

**Command Structure:**
- **Location**: `.claude/commands/exec.md`
- **Type**: Slash command (AI persona - Implementation Specialist)
- **Invocation**: `/exec <ticket-name>` or `/exec <path-to-plan.md>`
- **Outputs**:
  - Code files (new and modified)
  - `progress.yaml` (execution tracking)
  - Completion report

**Data Flow:**
```
User invokes /exec
    ↓
Resolve path (shorthand → full path)
    ↓
Load plan.md (implementation steps)
    ↓
Load spec.yaml (acceptance criteria)
    ↓
Load CLAUDE.md (project context)
    ↓
Load/create progress.yaml (tracking)
    ↓
Initialize TodoWrite (in-session visibility)
    ↓
Execute implementation loop:
  - Implement step
  - Run quality checks (Black, Ruff, pytest)
  - Handle errors (ask user if needed)
  - Mark step complete
  - Repeat
    ↓
Validate acceptance criteria
    ↓
Generate completion report
    ↓
Update spec.yaml status to "completed"
    ↓
Archive ticket to specs/archive/
    ↓
Update archived spec status to "archived"
```

### Key Components

**Path Resolution:**
- **Shorthand**: `/exec feature-user-auth` → `specs/tickets/feature-user-auth/plan.md`
- **Full path**: `/exec specs/tickets/feature-user-auth/plan.md` → use as-is
- **Fuzzy matching**: Typos show helpful suggestions (70% similarity threshold)

**Context Loading:**
1. **plan.md** - Implementation steps, file structure, dependencies, test cases
2. **spec.yaml** - Acceptance criteria, business value, constraints
3. **CLAUDE.md** - Quality standards, architecture patterns, error handling philosophy
4. **progress.yaml** - Completed/pending steps (if resuming)

**Progress Tracking System:**

**progress.yaml Structure:**
```yaml
ticket:
  name: feature-user-authentication
  type: feature
  started_at: "2025-11-03T10:30:00Z"
  updated_at: "2025-11-03T11:45:00Z"
  status: in_progress

implementation_steps:
  - step_id: 1
    description: "Create authentication module structure"
    status: completed
    started_at: "2025-11-03T10:30:00Z"
    completed_at: "2025-11-03T10:45:00Z"
    files_touched:
      - src/auth/__init__.py
      - src/auth/handlers.py

  - step_id: 2
    description: "Implement password hashing"
    status: in_progress
    started_at: "2025-11-03T10:46:00Z"
    completed_at: null
    files_touched: []

acceptance_criteria:
  - criterion: "Users can register with email and password"
    status: pending
    validated_at: null

  - criterion: "Passwords are hashed using bcrypt"
    status: met
    validated_at: "2025-11-03T10:50:00Z"

issues:
  - timestamp: "2025-11-03T10:35:00Z"
    type: test_failure
    description: "test_password_validation failed: AssertionError"
    resolution: "Fixed validation logic in auth/validators.py"
    resolved_at: "2025-11-03T10:40:00Z"

files_created:
  - src/auth/__init__.py
  - src/auth/handlers.py
  - src/auth/validators.py
  - tests/test_auth.py

files_modified:
  - src/main.py

quality_checks:
  black: passed
  ruff: passed_with_fixes
  pytest: 15_passed_2_failed
```

**TodoWrite Integration:**

Shows in-session progress in Claude Code:
```
✅ Step 1: Create authentication module structure
✅ Step 2: Implement password hashing
🔄 Step 3: Add JWT token generation
⏳ Step 4: Create login endpoint
⏳ Step 5: Add session management
```

**Quality Gates:**

1. **Black Formatting:**
   - Runs after each file modification
   - Auto-fixes formatting issues
   - Logs to progress.yaml

2. **Ruff Linting:**
   - Runs after each file modification
   - Auto-fixes fixable issues
   - Warns on non-fixable issues (asks user)

3. **Pytest:**
   - Runs relevant tests after each step
   - Reports failures (asks user for guidance)
   - Tracks pass/fail counts in progress.yaml

**Interactive Error Handling:**

**On Test Failure:**
```markdown
⚠️ Test Failure Detected

Step: Implement password hashing
Failed tests:
- test_password_strength: AssertionError: expected True, got False
- test_hash_uniqueness: ValueError: hash collision detected

Options:
1. Debug and fix the issue now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

**On Runtime Error:**
```markdown
⚠️ Runtime Error Detected

Step: Add JWT token generation
Error: ModuleNotFoundError: No module named 'jose'

This may indicate:
- Missing dependency (jose)
- Import path issue
- Environment configuration

Options:
1. Debug and fix now (e.g., add dependency)
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

**Resumability:**

If interrupted (Ctrl+C, crash, etc.), progress.yaml preserves state:

```bash
# Session interrupted at step 3
/exec feature-user-auth

Executor: 📋 Resuming from previous session...

Progress found:
✅ Completed: Steps 1-2 (2/5)
⏳ Remaining: Steps 3-5 (3/5)

Resuming from Step 3: Add JWT token generation
```

---

## Usage

### Basic Usage

**Starting an Execution Session:**
```bash
# Shorthand (recommended)
/exec feature-user-auth
/exec enhancement-shortcuts
/exec bug-validation-error

# Full path (also supported)
/exec specs/tickets/feature-user-auth/plan.md
/exec specs/tickets/enhancement-shortcuts/plan.md
```

**What Happens:**
1. Executor resolves path and validates plan.md exists
2. Loads context (plan, spec, CLAUDE.md, progress)
3. Creates/updates progress.yaml
4. Initializes TodoWrite
5. Executes implementation steps
6. Runs quality checks after each step
7. Asks for guidance on errors (interactive)
8. Validates acceptance criteria
9. Shows completion report

---

### Complete Workflow Example

**The Recommended Flow:**

```bash
# 1. MECHANICAL: Create ticket structure
cdd new feature user-authentication
# → Creates specs/tickets/feature-user-authentication/spec.yaml (empty)

# 2. INTELLIGENCE: Brainstorm and fill spec
/socrates feature-user-authentication
# → Guided conversation to build complete specification
# → Updates spec.yaml with requirements

# 3. INTELLIGENCE: Generate implementation plan
/plan feature-user-authentication
# → Creates detailed plan.md based on complete spec
# → Shows confirmation before generating

# 4. INTELLIGENCE: Execute the plan
/exec feature-user-authentication  ← YOU ARE HERE
# → Implements code step-by-step from plan
# → Runs quality checks automatically
# → Asks for guidance when blocked
```

**Why this order matters:**
- Socrates → Requirements clarity (conversations build understanding)
- Planner → Implementation clarity (detailed roadmap)
- **Executor → Code reality** (plan becomes working software)

---

### Session Example

**Session Start:**
```
You: /exec feature-user-auth

Executor: [Loads context silently]

📋 Execution Plan Loaded

**Ticket:** User Authentication with Email/Password
**Type:** Feature
**Steps:** 8 implementation steps
**Tests:** 12 test cases
**Estimated Effort:** 4-6 hours

📂 Context Loaded:
✅ plan.md - 450 lines, 8 steps
✅ spec.yaml - 5 acceptance criteria
✅ CLAUDE.md - Project patterns loaded

🚀 Starting implementation...

---

✅ Step 1/8: Create authentication module structure
   Created: src/auth/__init__.py
   Created: src/auth/handlers.py

   Quality checks:
   ✅ Black: Formatted 2 files
   ✅ Ruff: No issues

   [Progress: 1/8 steps complete]

---

✅ Step 2/8: Implement password hashing
   Modified: src/auth/handlers.py
   Created: src/auth/utils.py

   Quality checks:
   ✅ Black: Already formatted
   ✅ Ruff: No issues
   ✅ Pytest: 3/3 tests passed

   [Progress: 2/8 steps complete]

---

🔄 Step 3/8: Add JWT token generation
   Modified: src/auth/handlers.py

   Quality checks:
   ✅ Black: Already formatted
   ⚠️  Ruff: 1 auto-fixed (unused import)
   ❌ Pytest: 2/3 tests failed

⚠️ Test Failure Detected

Step: Add JWT token generation
Failed tests:
- test_token_expiry: AssertionError: Token didn't expire
- test_token_validation: ValueError: Invalid signature

Options:
1. Debug and fix the issue now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)

You: 1

Executor: Debugging test failures...

Found issue: Token expiry time not set correctly.
Fixing: src/auth/handlers.py:45 - Set expiry to 30 days

Re-running tests...
✅ Pytest: 3/3 tests passed

[Progress: 3/8 steps complete]

---

[Continues through remaining steps...]

---

🎯 Validating Acceptance Criteria

Checking each criterion from spec.yaml...

✅ Users can register with email and password
✅ Users can log in with valid credentials
✅ Passwords are hashed using bcrypt
✅ Invalid credentials show appropriate errors
⚠️  Password reset via email - Partially implemented (email service not configured)

---

✅ Implementation Complete!

**Files Created:**
- src/auth/__init__.py
- src/auth/handlers.py
- src/auth/utils.py
- src/auth/validators.py
- tests/test_auth.py

**Files Modified:**
- src/main.py (added auth routes)
- requirements.txt (added bcrypt, pyjwt)

**Acceptance Criteria Status:**
✅ 4 of 5 criteria met
⚠️  1 criterion partially met (email service configuration needed)

**Issues Encountered:**
1. [RESOLVED] Test failures in JWT validation - Fixed token expiry logic
2. [KNOWN ISSUE] Email service not configured - Manual setup required

**Quality Gates:**
✅ Black: All files formatted
✅ Ruff: All issues fixed
⚠️  Pytest: 11/12 passed (1 test skipped - email service)

**Progress File:** specs/tickets/feature-user-auth/progress.yaml

🎉 Ready for review and testing!

**Next Steps:**
1. Review generated code
2. Configure email service for password reset
3. Run full integration tests
4. Update living documentation if needed
```

---

## Execution Modes

### Interactive Mode (/exec)

**Characteristics:**
- Asks for guidance on test failures
- Asks for guidance on runtime errors
- Gives user control over error resolution
- Best for complex features
- Best when you want to supervise

**When to Use:**
- Complex features with many dependencies
- When you want to catch issues immediately
- When you're learning the codebase
- First-time implementations
- Critical features requiring review

**Example:**
```bash
/exec feature-payment-processing

# Executor will:
- Stop on test failures and ask for guidance
- Stop on runtime errors and ask how to proceed
- Give you control over error resolution
- Wait for your decisions before continuing
```

---

### Autonomous Mode (/exec-auto)

**Characteristics:**
- Never asks for input
- Continues on errors (logs to progress.yaml)
- Auto-fixes all fixable issues
- Best-effort completion
- Best for straightforward tasks

**When to Use:**
- Simple, well-defined features
- Tasks with clear, detailed plans
- When you want hands-free execution
- Batch implementation of multiple tickets
- Low-risk refactoring

**Example:**
```bash
/exec-auto feature-add-logging

# Executor Auto will:
- Never stop for questions
- Log all errors to progress.yaml
- Auto-fix formatting and linting
- Complete as much as possible
- Give final report at end
```

**See:** [exec-auto-command.md](exec-auto-command.md) for full documentation

---

## Progress Tracking

### progress.yaml

**Purpose:** Durable progress tracking for resumability

**Location:** `specs/tickets/<ticket-name>/progress.yaml`

**Created:** First time `/exec` or `/exec-auto` runs

**Benefits:**
- Resume from interruptions
- Track what's been completed
- Log issues and resolutions
- Validate acceptance criteria
- Audit trail of implementation

### TodoWrite

**Purpose:** In-session visibility in Claude Code UI

**Format:**
```
✅ Step 1: Create module structure
✅ Step 2: Implement core logic
🔄 Step 3: Add error handling
⏳ Step 4: Write tests
⏳ Step 5: Update documentation
```

**Updates:** Real-time as steps complete

**Benefit:** Visual progress without checking files

---

## Quality Automation

### Black Formatting

**Runs:** After every file modification

**Behavior:**
- Automatically formats code
- Uses project's Black config (.black, pyproject.toml)
- Logs formatting changes to progress.yaml

**Output:**
```
✅ Black: Formatted 3 files
   - src/auth/handlers.py (5 changes)
   - src/auth/utils.py (2 changes)
   - tests/test_auth.py (1 change)
```

### Ruff Linting

**Runs:** After every file modification

**Behavior:**
- Automatically fixes fixable issues (imports, unused vars, etc.)
- Warns on non-fixable issues (asks user in /exec, logs in /exec-auto)
- Uses project's Ruff config (.ruff.toml, pyproject.toml)

**Output:**
```
✅ Ruff: 2 issues auto-fixed
   - Removed unused import (F401)
   - Fixed line too long (E501)

⚠️  Ruff: 1 non-fixable issue
   - Complexity too high (C901) in authenticate() function

   Suggestion: Refactor function to reduce complexity
   Continue anyway? (Y/n)
```

### Pytest

**Runs:** After steps that involve tests

**Behavior:**
- Runs relevant test files
- Reports pass/fail counts
- Shows failure details (interactive mode)
- Logs to progress.yaml

**Output:**
```
✅ Pytest: 8/8 tests passed
   - test_auth.py: 5 passed
   - test_validators.py: 3 passed

❌ Pytest: 7/9 tests passed, 2 failed
   - test_auth.py::test_token_expiry: AssertionError
   - test_auth.py::test_invalid_password: ValueError
```

---

## Error Handling

### Test Failures

**Interactive Mode (/exec):**
```markdown
⚠️ Test Failure Detected

Step: Implement login endpoint
Failed tests:
- test_login_success: AssertionError: Expected 200, got 401
- test_login_invalid: AssertionError: Expected error message

Options:
1. Debug and fix the issue now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

**User chooses:**
- **1 (Debug)**: Executor analyzes code, suggests fixes, implements and re-tests
- **2 (Continue)**: Logs to progress.yaml, continues to next step
- **3 (Stop)**: Saves progress, exits cleanly

### Runtime Errors

**Interactive Mode (/exec):**
```markdown
⚠️ Runtime Error Detected

Step: Initialize database connection
Error: ConnectionError: Could not connect to database at localhost:5432

This may indicate:
- Database not running
- Wrong connection string in config
- Network/firewall issue

Options:
1. Debug and fix now
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

### Missing Dependencies

**Interactive Mode (/exec):**
```markdown
⚠️ Missing Dependency

Step: Add JWT token generation
Error: ModuleNotFoundError: No module named 'jose'

Suggested fix:
Add dependency: poetry add python-jose

Options:
1. Add dependency now and continue
2. Mark as known issue and continue
3. Stop implementation

Which option? (1/2/3)
```

---

## Acceptance Criteria Validation

### How It Works

After all implementation steps complete, Executor validates each acceptance criterion from spec.yaml:

**Process:**
1. Read acceptance criteria from spec.yaml
2. For each criterion:
   - Examine relevant code files
   - Check if functionality exists
   - Run relevant tests
   - Determine: met, partially met, or not met
3. Record validation in progress.yaml
4. Report in completion summary

**Example:**

**spec.yaml:**
```yaml
acceptance_criteria:
  - Users can register with email and password
  - Users can log in with valid credentials
  - Passwords are hashed using bcrypt
  - Invalid credentials show appropriate errors
  - Sessions persist with "remember me" option
```

**Validation Output:**
```markdown
🎯 Validating Acceptance Criteria

✅ Users can register with email and password
   Evidence: register() endpoint in src/auth/handlers.py
   Tests: test_register_success, test_register_duplicate (passed)

✅ Users can log in with valid credentials
   Evidence: login() endpoint in src/auth/handlers.py
   Tests: test_login_success, test_login_remember_me (passed)

✅ Passwords are hashed using bcrypt
   Evidence: hash_password() uses bcrypt in src/auth/utils.py
   Tests: test_password_hashing (passed)

✅ Invalid credentials show appropriate errors
   Evidence: Error handling in login() with specific messages
   Tests: test_login_invalid_password, test_login_unknown_user (passed)

⚠️  Sessions persist with "remember me" option
   Evidence: Session logic partially implemented
   Issue: Token refresh mechanism not complete
   Tests: test_remember_me (1 passed, 1 failed)

---

**Summary:** 4 of 5 criteria fully met, 1 partially met
```

---

## Resumability

### How Resume Works

**Scenario:** Implementation interrupted (crash, Ctrl+C, timeout)

**On Next Run:**
```bash
/exec feature-user-auth

Executor: 📋 Resuming from previous session...

**Progress found:**
Ticket: feature-user-authentication
Started: 2025-11-03 10:30:00
Last updated: 2025-11-03 11:45:00

**Completed Steps:** 5/8
✅ Step 1: Create module structure
✅ Step 2: Implement password hashing
✅ Step 3: Add JWT token generation
✅ Step 4: Create login endpoint
✅ Step 5: Add session management

**Remaining Steps:** 3/8
⏳ Step 6: Implement password reset
⏳ Step 7: Add rate limiting
⏳ Step 8: Update documentation

**Resuming from Step 6...**
```

**Benefits:**
- No duplicate work
- Preserves completed progress
- Picks up exactly where left off
- Can review progress.yaml to see what's done

---

## Ticket Archiving

### Automatic Archiving on Completion

After successful implementation, Executor automatically archives completed tickets to keep the active tickets directory clean and organized.

**What Happens:**

1. **Update Completion Status:**
   - Executor updates spec.yaml status to "completed"
   - Adds implementation_completed timestamp

2. **Move to Archive:**
   - Entire ticket folder moved from specs/tickets/ to specs/archive/
   - All files preserved (spec.yaml, plan.md, progress.yaml, etc.)

3. **Mark as Archived:**
   - Updates archived spec.yaml status to "archived"
   - Adds archived_at timestamp

**Example:**

```bash
/exec feature-user-auth

# ... implementation happens ...

✅ Implementation Complete!

📦 Ticket Archived

Moved to: specs/archive/feature-user-authentication/

If bugs are found, restore with:
mv specs/archive/feature-user-authentication specs/tickets/feature-user-authentication
```

**Benefit:**
- **Clean workspace** - Active tickets/ only contains in-progress work
- **Audit trail** - All completed work preserved in archive/
- **Easy restore** - Simple mv command if bugs are found
- **Team visibility** - Everyone sees what's active vs completed

### Spec Status Lifecycle

Throughout the implementation workflow, spec.yaml status is automatically updated:

**Status Progression:**
```
draft → defined → planned → in_progress → completed → archived
```

**When Each Status is Set:**

| Status | When Set | Who Sets It |
|--------|----------|-------------|
| `draft` | Ticket created with `cdd new` | CLI (mechanical layer) |
| `defined` | Spec filled out with /socrates | Socrates agent |
| `planned` | Plan generated with /plan | Planner agent |
| `in_progress` | Implementation started with /exec | Executor agent (at start) |
| `completed` | Implementation finished | Executor agent (before archiving) |
| `archived` | Ticket moved to archive/ | Executor agent (after archiving) |

**Why Track Status:**
- Team knows what stage each ticket is in
- Easy to find active work (filter by "in_progress")
- Clear audit trail for completed features
- Enables dashboard views (future enhancement)

**Example spec.yaml:**
```yaml
ticket:
  name: feature-user-authentication
  type: feature
  status: archived  # Updated automatically by Executor
  created: "2025-11-01"
  updated: "2025-11-03"
  implementation_started: "2025-11-02"
  implementation_completed: "2025-11-03"
  archived_at: "2025-11-03"
```

---

## Integration with CDD Framework

### Position in Workflow

**The Four-Step Process:**

```
1. cdd new feature user-auth
   ↓ (Mechanical: Create structure)
   specs/tickets/feature-user-auth/spec.yaml (empty)

2. /socrates feature-user-auth
   ↓ (Intelligence: Gather requirements)
   spec.yaml filled with complete requirements

3. /plan feature-user-auth
   ↓ (Intelligence: Create implementation plan)
   plan.md with detailed, executable steps

4. /exec feature-user-auth ← YOU ARE HERE
   ↓ (Intelligence: Execute implementation)
   Working code with quality gates passed
```

### Handoff from Planner

**What Executor Receives:**

From Planner session, plan.md contains:
- Implementation steps (numbered, phased)
- File structure (exact paths to create/modify)
- Code examples (actual snippets)
- Technical decisions (documented)
- Test cases (function signatures)
- Error handling requirements
- Dependencies (with versions)

**Quality Impact:**
- Detailed plan → Better implementation
- Code examples → Consistent style
- Test cases → Higher coverage
- Clear steps → Fewer errors

### Handoff to Living Documentation

**After Execution:**

```bash
# Implementation complete
/exec feature-user-auth
# → Code written, tests passing

# Update living documentation
/socrates docs/features/authentication.md
# → Brainstorm updates reflecting what was built
# → Or update manually based on implementation
```

**Future:** Auto-documentation via `/complete` command (roadmap)

---

## Philosophy & Design

### Core Principles

**Plan-Driven Execution:**
> "A detailed plan executed precisely beats a vague plan executed perfectly."

- Follows plan.md step-by-step
- Trusts Planner's decisions
- Executes with precision, not interpretation

**Progress Visibility:**
> "You can't manage what you can't see."

- progress.yaml (durable, resumable)
- TodoWrite (in-session, visual)
- Completion report (comprehensive summary)

**Quality Automation:**
> "Automate what's automatable, escalate what's not."

- Auto-fix formatting (Black)
- Auto-fix linting (Ruff)
- Run tests automatically
- Ask human for non-automatable issues

**Interactive Guidance:**
> "Humans are better at decisions, AI is better at execution."

- Let AI execute mechanical tasks
- Ask human for judgment calls
- Preserve user control on critical decisions

---

## Testing

### Manual Testing Approach

**Why Manual?**

Per CLAUDE.md standards:
> **AI-driven features** (slash commands, conversational interfaces) → Manual testing with checklist

Executor is:
- Interactive (asks for user guidance)
- Non-deterministic (adapts to different plans, codebases)
- Context-dependent (behavior varies by project)

Traditional unit tests are inappropriate for this type of AI feature.

### Testing Checklist

**✅ Correct Execution:**
- [ ] Reads plan.md and extracts steps correctly
- [ ] Loads spec.yaml for acceptance criteria
- [ ] Loads CLAUDE.md for project context
- [ ] Creates progress.yaml on first run
- [ ] Resumes from progress.yaml on subsequent runs

**✅ Quality Automation:**
- [ ] Runs Black on every file modification
- [ ] Runs Ruff on every file modification
- [ ] Auto-fixes fixable linting issues
- [ ] Runs pytest after test-related steps

**✅ Progress Tracking:**
- [ ] Updates progress.yaml after each step
- [ ] Updates TodoWrite in real-time
- [ ] Logs issues to progress.yaml correctly
- [ ] Preserves state on interruption

**✅ Error Handling:**
- [ ] Detects test failures correctly
- [ ] Detects runtime errors correctly
- [ ] Provides clear error messages
- [ ] Offers appropriate options (debug/continue/stop)
- [ ] Handles user responses correctly

**✅ Acceptance Criteria:**
- [ ] Validates criteria from spec.yaml
- [ ] Determines met/partially met/not met correctly
- [ ] Records validation in progress.yaml
- [ ] Reports validation in completion summary

**✅ Path Resolution:**
- [ ] Shorthand paths resolve correctly
- [ ] Full paths work as-is
- [ ] Fuzzy matching suggests similar tickets
- [ ] Error messages are helpful

**✅ Completion Report:**
- [ ] Lists all files created
- [ ] Lists all files modified
- [ ] Shows acceptance criteria status
- [ ] Lists issues encountered
- [ ] Shows quality gate results

---

## Performance & Characteristics

**Session Duration:**
- Varies by task complexity
- Simple features: 10-30 minutes
- Complex features: 1-3 hours
- Resumable if interrupted

**Context Usage:**
- Loads: plan.md, spec.yaml, CLAUDE.md, progress.yaml
- Reads: Source files as needed during implementation
- Writes: Implementation code, tests, progress.yaml

**Interaction Pattern:**
- Mostly autonomous (executes steps mechanically)
- Periodic progress updates (TodoWrite)
- Interactive on errors (asks for guidance)
- Final report (comprehensive summary)

**Scalability:**
- Works on projects of any size
- Progress tracking prevents re-work
- Quality gates ensure consistency
- Resumability enables long-running tasks

**Reliability:**
- High success rate for well-planned features
- Error handling prevents silent failures
- Progress.yaml provides audit trail
- Quality gates catch issues early

---

## Dependencies

### Required Dependencies

**plan.md (Implementation Plan)**
- Purpose: Step-by-step implementation instructions
- Source: Created by `/plan` slash command
- Must contain: Steps, file structure, technical decisions, test cases

**spec.yaml (Requirements)**
- Purpose: Acceptance criteria for validation
- Source: Created by `cdd new`, filled by `/socrates`
- Optional but recommended

**CLAUDE.md (Project Context)**
- Purpose: Quality standards, architecture patterns
- Location: Project root
- Highly recommended (falls back to general best practices)

**Development Tools**
- **Black**: Code formatting (must be installed)
- **Ruff**: Linting (must be installed)
- **pytest**: Testing (must be installed if tests exist)

### Integration Points

**With Socrates:**
- Consumes: spec.yaml filled by Socrates
- Uses: Acceptance criteria for validation

**With Planner:**
- Consumes: plan.md generated by Planner
- Follows: Implementation steps, file structure, test cases

**With Quality Tools:**
- Runs: Black, Ruff, pytest automatically
- Uses: Project configuration files (pyproject.toml, etc.)

**With File System:**
- Reads: plan.md, spec.yaml, CLAUDE.md, source files
- Writes: Implementation code, progress.yaml
- Works with: Version-controlled files (git)

---

## Future Enhancements

**Intelligent Conflict Resolution:**
- Detect merge conflicts before they happen
- Suggest resolution strategies
- Auto-resolve simple conflicts

**Learning from Feedback:**
- Track which steps commonly fail
- Learn from user corrections
- Improve future implementations

**Parallel Execution:**
- Execute independent steps in parallel
- Speed up implementation for large plans
- Maintain progress tracking

**Multi-File Refactoring:**
- Coordinate changes across multiple files
- Ensure consistency during refactoring
- Validate cross-file dependencies

**Custom Quality Gates:**
- Project-specific quality checks
- Custom linters and validators
- Integration with CI/CD pipelines

---

## Related Documentation

- [Plan Command](plan-command.md) - Generates plan.md that Executor consumes
- [Exec Auto Command](exec-auto-command.md) - Autonomous execution mode
- [Socrates](socrates.md) - Creates spec.yaml with acceptance criteria
- [CLI Reference Guide](../guides/CLI_REFERENCE.md) - Complete command reference

---

*Last updated: 2025-11-03 | Status: Production | Version: 0.1.0*

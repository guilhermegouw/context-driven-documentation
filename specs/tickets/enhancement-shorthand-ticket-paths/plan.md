# Enhancement Plan: Shorthand Ticket Paths for Slash Commands

**Generated:** 2025-11-02
**Spec:** `specs/tickets/enhancement-shorthand-ticket-paths/spec.yaml`
**Ticket Type:** Enhancement
**Enhancement Type:** improvement
**Estimated Effort:** 4-6 hours (High confidence)

---

## Executive Summary

This enhancement adds shorthand syntax for slash commands, enabling users to type `/socrates feature-user-auth` instead of `/socrates specs/tickets/feature-user-auth/spec.yaml`. This dramatically improves workflow speed and aligns with the framework's AI-first philosophy of natural, conversational interaction.

**Current State:** Slash commands require verbose full file paths (`/socrates specs/tickets/feature-user-auth/spec.yaml`), creating friction in the interactive workflow and breaking conversational flow.

**Target State:** Smart path resolution accepts ticket names as shorthand while maintaining full backward compatibility. Helpful error messages with fuzzy matching guide users to correct ticket names.

**Key Changes:**
- Create `PathResolver` utility class for smart path resolution
- Update slash command prompts to use PathResolver
- Add fuzzy matching for helpful error suggestions
- Maintain full backward compatibility with existing syntax

---

## Analysis & Justification

### Current Implementation Analysis

**What Works:**
- Slash commands function correctly with full paths
- Clear, explicit file targeting (no ambiguity)
- Follows conventional file system patterns

**What Needs Improvement:**
- Verbose syntax creates typing friction (`/socrates specs/tickets/feature-user-auth/spec.yaml`)
- Breaks "natural conversation" principle of AI-first design
- Users must remember exact directory structure
- Repetitive typing of `specs/tickets/` prefix
- No helpful suggestions when paths are wrong

**Root Cause:**
Original implementation prioritized explicitness over convenience. As the framework matures and usage patterns emerge, convenience becomes critical for daily workflow efficiency without sacrificing clarity.

### Improvement Strategy

**Approach:** Smart path resolution with intelligent defaults

The resolver will:
1. Detect if argument is an explicit path (contains `/` or file extension)
2. If not, treat as ticket shorthand and resolve to conventional location
3. Each command knows its target file (`spec.yaml` for socrates/plan, `plan.md` for exec)
4. On error, use fuzzy matching to suggest similar tickets

**Why This Approach:**
- Maintains backward compatibility (explicit paths still work)
- Follows "convention over configuration" principle
- Zero breaking changes for existing users
- Enables future flexibility (non-ticket files still accessible)
- Fuzzy matching provides excellent UX when tickets don't exist

**Alternatives Considered:**
1. **Two-argument syntax** (`/socrates feature user-auth`)
   - Pros: Separates type from name
   - Cons: Ticket names already include type prefix (feature-user-auth)
   - Why Not Chosen: Redundant, more typing, confusing mental model

2. **Strict shorthand only** (no full paths)
   - Pros: Simpler implementation
   - Cons: Breaks backward compatibility, reduces flexibility
   - Why Not Chosen: Breaking changes unacceptable, limits edge cases (CLAUDE.md, docs/)

---

## Technical Decisions

### Decision 1: Create Dedicated PathResolver Utility
**Choice:** New `src/cddoc/path_resolver.py` module with `PathResolver` class
**Rationale:** Follows existing pattern (separate utilities like `init.py`, `new_ticket.py`). Enables easy unit testing and reuse across commands.
**Impact:** Clean separation of concerns, testable logic independent of slash commands

### Decision 2: Command-Specific Target Files
**Choice:** Each command specifies its target file when calling PathResolver
**Rationale:**
- `/socrates` and `/plan` need `spec.yaml` (requirements)
- `/exec` needs `plan.md` (implementation plan)
- Keeps resolver generic and flexible
**Impact:** PathResolver is reusable, commands control their own behavior

### Decision 3: Use stdlib difflib for Fuzzy Matching
**Choice:** Python's built-in `difflib.get_close_matches()` with 70% similarity cutoff
**Rationale:** No external dependencies, proven library, sufficient for ticket name matching
**Impact:** Zero new dependencies, fast enough for typical ticket counts (<100)

### Decision 4: Rich-Formatted Error Messages
**Choice:** Errors use Rich console for formatted, actionable messages
**Rationale:** Consistent with existing error handling (see `init.py`), follows three-part error pattern
**Impact:** Professional, helpful errors that guide users to resolution

### Decision 5: Update Slash Commands via Prompt Instructions
**Choice:** Add PathResolver usage instructions to `.claude/commands/*.md` files
**Rationale:** Slash commands are markdown prompts, not code. Claude reads them and follows instructions.
**Impact:** Claude will automatically use PathResolver when executing slash commands

---

## Impact Assessment

### Breaking Changes
**No breaking changes.**

All existing syntax continues to work:
- `/socrates specs/tickets/feature-user-auth/spec.yaml` ✅ Works
- `/socrates CLAUDE.md` ✅ Works
- `/plan docs/features/authentication.md` ✅ Works

### Affected Components

1. **`/socrates` slash command**
   - Impact: Gains shorthand support
   - Changes Required: Update `.claude/commands/socrates.md` with PathResolver instructions

2. **`/plan` slash command**
   - Impact: Gains shorthand support
   - Changes Required: Update `.claude/commands/plan.md` with PathResolver instructions

3. **`/exec` slash command**
   - Impact: Gains shorthand support with `plan.md` target
   - Changes Required: Update `.claude/commands/exec.md` with PathResolver instructions

4. **Documentation and Examples**
   - Impact: Examples will show cleaner shorthand syntax
   - Changes Required: Update README.md, CLI_REFERENCE.md, Next Steps message

### Backward Compatibility

**100% backward compatible**

**Compatibility Plan:**
- Resolution logic checks for explicit paths first (contains `/` or ends with `.md`/`.yaml`)
- Explicit paths bypass resolution and are used as-is
- Shorthand only activates for simple ticket names
- No changes to slash command core functionality

---

## File Structure

### New Files to Create

1. **`src/cddoc/path_resolver.py`**
   - Purpose: Smart path resolution with fuzzy matching
   - Key components:
     - `PathResolver` class with static methods
     - `resolve(argument: str, target_file: str) -> Path` - Main resolution logic
     - `find_similar_tickets(ticket_name: str) -> List[str]` - Fuzzy matching
     - `format_not_found_error(ticket_name: str, similar: List[str]) -> str` - Error formatting
     - `PathResolutionError` custom exception

2. **`tests/test_path_resolver.py`**
   - Purpose: Unit tests for PathResolver
   - Key test cases:
     - Shorthand resolution
     - Explicit path passthrough
     - Fuzzy matching
     - Error message formatting
     - Edge cases (empty tickets dir, special characters)

### Files to Modify

1. **`.claude/commands/socrates.md`**
   - Current state: Direct file path usage in Step 1
   - Changes needed: Add PathResolver import and usage instructions
   - Location: "Step 1: Initialize - Intelligent Context Loading" section

2. **`.claude/commands/plan.md`**
   - Current state: Direct file path usage in Step 1
   - Changes needed: Add PathResolver import and usage instructions
   - Location: "Step 1: Parse Command & Extract Path" section

3. **`.claude/commands/exec.md`**
   - Current state: Direct file path usage in Step 1
   - Changes needed: Add PathResolver import and usage instructions with `plan.md` target
   - Location: "Step 1: Parse Command & Extract Plan Path" section

4. **`docs/guides/CLI_REFERENCE.md`**
   - Current state: Shows full path examples
   - Changes needed: Add shorthand syntax examples, explain resolution logic

5. **`README.md`**
   - Current state: Shows full path examples in usage section
   - Changes needed: Update examples to demonstrate shorthand syntax

6. **`src/cddoc/cli.py`**
   - Current state: Next Steps shows full paths
   - Changes needed: Update `_display_next_steps()` to show shorthand examples
   - Location: Line ~149-155

---

## Implementation Steps

### Phase 1: Preparation & Analysis
**Estimated Time:** 0.5 hours

1. **Review Current Slash Command Structure** (15 min)
   - Read `.claude/commands/socrates.md`, `plan.md`, `exec.md`
   - Understand current argument parsing patterns
   - Identify exact insertion points for PathResolver instructions
   - **Success Criteria:** Clear understanding of how arguments flow through commands

2. **Set Up Safety Measures** (15 min)
   - Run existing tests: `poetry run pytest`
   - Ensure all tests pass
   - Create feature branch: `git checkout -b feature/shorthand-ticket-paths`
   - **Success Criteria:** Clean baseline, safe working environment

### Phase 2: Implementation
**Estimated Time:** 2-3 hours

1. **Create PathResolver Module** (60 min)
   - **Actions:**
     - Create `src/cddoc/path_resolver.py`
     - Implement `PathResolutionError` exception class
     - Implement `PathResolver.resolve()` method
     - Implement `PathResolver.find_similar_tickets()` method
     - Implement `PathResolver.format_not_found_error()` method
     - Add comprehensive docstrings and type hints
   - **Expected Outcome:** Fully functional PathResolver with all methods
   - **Verification:** Module imports without errors, methods callable
   - **Potential Blockers:** Edge cases in path detection logic

   **Code Structure:**
   ```python
   """Smart path resolution for slash commands."""

   import difflib
   from pathlib import Path
   from typing import List

   from rich.console import Console

   console = Console()


   class PathResolutionError(Exception):
       """Raised when path cannot be resolved."""
       pass


   class PathResolver:
       """Resolves ticket shorthand to full paths."""

       TICKETS_DIR = Path("specs/tickets")
       SIMILARITY_THRESHOLD = 0.7  # 70% similarity for fuzzy matching
       MAX_SUGGESTIONS = 3

       @staticmethod
       def resolve(argument: str, target_file: str = "spec.yaml") -> Path:
           """Resolve argument to full file path.

           Args:
               argument: User input (ticket name or full path)
               target_file: Target file name (spec.yaml or plan.md)

           Returns:
               Resolved Path object

           Raises:
               PathResolutionError: If ticket not found (with suggestions)
           """
           # Implementation here

       @staticmethod
       def find_similar_tickets(ticket_name: str) -> List[str]:
           """Find similar ticket names using fuzzy matching.

           Args:
               ticket_name: Ticket name to match

           Returns:
               List of similar ticket names (max 3)
           """
           # Implementation here

       @staticmethod
       def format_not_found_error(
           ticket_name: str,
           similar_tickets: List[str],
           command: str = "socrates"
       ) -> str:
           """Format helpful error message with suggestions.

           Args:
               ticket_name: Ticket that wasn't found
               similar_tickets: List of similar tickets (may be empty)
               command: Command being used (for suggestions)

           Returns:
               Formatted error message string
           """
           # Implementation here
   ```

2. **Update socrates.md** (20 min)
   - **Actions:**
     - Open `.claude/commands/socrates.md`
     - Find "Step 2: Read Target File" section
     - Add PathResolver usage before file reading:
       ```markdown
       #### Step 0: Resolve Argument to Full Path

       **Before reading the file, resolve the argument:**

       ```python
       from cddoc.path_resolver import PathResolver, PathResolutionError

       try:
           resolved_path = PathResolver.resolve(argument, target_file="spec.yaml")
       except PathResolutionError as e:
           # Display error message (already formatted with suggestions)
           print(e)
           return
       ```

       Now use `resolved_path` for all file operations.
       ```
   - **Expected Outcome:** Socrates uses PathResolver before file operations
   - **Verification:** Markdown syntax is valid, instructions are clear
   - **Potential Blockers:** None (markdown edit)

3. **Update plan.md** (20 min)
   - **Actions:**
     - Open `.claude/commands/plan.md`
     - Find "Step 1: Parse Command & Extract Path" section
     - Add PathResolver usage:
       ```markdown
       **Your Actions:**

       1. Extract the spec.yaml file path from the command
       2. **Resolve using PathResolver:**
          ```python
          from cddoc.path_resolver import PathResolver, PathResolutionError

          try:
              resolved_path = PathResolver.resolve(argument, target_file="spec.yaml")
          except PathResolutionError as e:
              console.print(f"[red]{e}[/red]")
              return
          ```
       3. Validate the path exists and is readable
       ```
   - **Expected Outcome:** Plan uses PathResolver with spec.yaml target
   - **Verification:** Markdown syntax valid, consistent with socrates pattern
   - **Potential Blockers:** None (markdown edit)

4. **Update exec.md** (20 min)
   - **Actions:**
     - Open `.claude/commands/exec.md`
     - Find "Step 1: Parse Command & Extract Plan Path" section
     - Add PathResolver usage with `plan.md` target:
       ```markdown
       **Your Actions:**

       1. Extract the plan.md file path from command
       2. **Resolve using PathResolver:**
          ```python
          from cddoc.path_resolver import PathResolver, PathResolutionError

          try:
              resolved_path = PathResolver.resolve(argument, target_file="plan.md")
          except PathResolutionError as e:
              console.print(f"[red]{e}[/red]")
              return
          ```
       3. Validate path exists and is readable
       ```
   - **Expected Outcome:** Exec uses PathResolver with plan.md target
   - **Verification:** Uses different target file than socrates/plan
   - **Potential Blockers:** None (markdown edit)

5. **Update CLI Next Steps Message** (20 min)
   - **Actions:**
     - Open `src/cddoc/cli.py`
     - Find `_display_next_steps()` function (line ~116-158)
     - Update slash command examples to use shorthand:
       - Line ~144: `/socrates CLAUDE.md` ✅ (keep as-is, shows non-ticket path)
       - Line ~150: Change to `/socrates specs/tickets/feature-user-auth/spec.yaml` → `/socrates feature-user-auth`
       - Line ~153: Change to `/plan specs/tickets/feature-user-auth/spec.yaml` → `/plan feature-user-auth`
       - Line ~156: Change to `/exec specs/tickets/feature-user-auth/plan.md` → `/exec feature-user-auth`
   - **Expected Outcome:** Next Steps shows clean shorthand examples
   - **Verification:** Run `poetry run cdd init --help` to ensure no syntax errors
   - **Potential Blockers:** None (simple string changes)

### Phase 3: Validation & Testing
**Estimated Time:** 1-2 hours

1. **Write PathResolver Unit Tests** (60 min)
   - **Actions:**
     - Create `tests/test_path_resolver.py`
     - Test shorthand resolution:
       ```python
       def test_resolve_shorthand_to_spec_yaml():
           """Test shorthand resolves to spec.yaml."""
           result = PathResolver.resolve("feature-user-auth", "spec.yaml")
           assert result == Path("specs/tickets/feature-user-auth/spec.yaml")

       def test_resolve_shorthand_to_plan_md():
           """Test shorthand resolves to plan.md."""
           result = PathResolver.resolve("feature-user-auth", "plan.md")
           assert result == Path("specs/tickets/feature-user-auth/plan.md")
       ```
     - Test explicit path passthrough:
       ```python
       def test_resolve_explicit_path():
           """Test explicit paths are used as-is."""
           result = PathResolver.resolve("specs/tickets/feature-x/spec.yaml", "spec.yaml")
           assert result == Path("specs/tickets/feature-x/spec.yaml")

       def test_resolve_non_ticket_file():
           """Test non-ticket files work."""
           result = PathResolver.resolve("CLAUDE.md", "spec.yaml")
           assert result == Path("CLAUDE.md")
       ```
     - Test fuzzy matching:
       ```python
       def test_find_similar_tickets(tmp_path):
           """Test fuzzy matching finds similar tickets."""
           # Create mock ticket directories
           tickets_dir = tmp_path / "specs" / "tickets"
           tickets_dir.mkdir(parents=True)
           (tickets_dir / "feature-auth").mkdir()
           (tickets_dir / "feature-authentication").mkdir()
           (tickets_dir / "bug-payment").mkdir()

           # Mock TICKETS_DIR
           with patch.object(PathResolver, 'TICKETS_DIR', tickets_dir):
               similar = PathResolver.find_similar_tickets("feat-auth")
               assert "feature-auth" in similar
               assert "feature-authentication" in similar
               assert "bug-payment" not in similar
       ```
     - Test error formatting:
       ```python
       def test_format_not_found_error_with_suggestions():
           """Test error message includes suggestions."""
           error = PathResolver.format_not_found_error(
               "my-feature",
               ["feature-my-feature", "enhancement-my-features"],
               command="socrates"
           )
           assert "my-feature" in error
           assert "feature-my-feature" in error
           assert "/socrates feature-my-feature" in error

       def test_format_not_found_error_no_suggestions():
           """Test error message when no suggestions."""
           error = PathResolver.format_not_found_error(
               "my-feature",
               [],
               command="plan"
           )
           assert "my-feature" in error
           assert "cdd new feature my-feature" in error
       ```
   - **Expected Outcome:** Comprehensive test coverage for PathResolver
   - **Verification:** `poetry run pytest tests/test_path_resolver.py -v` passes
   - **Potential Blockers:** Mock setup for filesystem operations

2. **Run All Tests** (15 min)
   - **Actions:**
     - Run full test suite: `poetry run pytest`
     - Verify no regressions
     - Check test coverage: `poetry run pytest --cov=src/cddoc --cov-report=term-missing`
   - **Expected Outcome:** All tests pass, coverage maintained/improved
   - **Success Criteria:** 0 failures, coverage ≥ current baseline
   - **Potential Blockers:** Unexpected test failures from integration

3. **Manual Testing Checklist** (30 min)
   - **Actions:** Test slash commands interactively in Claude Code
   - **Test Cases:**
     - [ ] `/socrates feature-user-auth` resolves correctly
     - [ ] `/socrates specs/tickets/feature-user-auth/spec.yaml` still works (backward compat)
     - [ ] `/socrates CLAUDE.md` works (non-ticket file)
     - [ ] `/socrates nonexistent-ticket` shows helpful error with suggestions
     - [ ] `/plan feature-user-auth` resolves correctly
     - [ ] `/exec feature-user-auth` resolves to plan.md (not spec.yaml)
     - [ ] Error messages are well-formatted with Rich styling
     - [ ] Fuzzy matching suggests correct similar tickets
   - **Success Criteria:** All test cases pass, UX feels natural
   - **Potential Blockers:** Slash command execution issues

### Phase 4: Documentation & Cleanup
**Estimated Time:** 1 hour

1. **Update CLI Reference Guide** (20 min)
   - **Actions:**
     - Open `docs/guides/CLI_REFERENCE.md`
     - Add new section: "Slash Command Shorthand Syntax"
     - Document resolution logic:
       ```markdown
       ## Slash Command Shorthand Syntax

       Slash commands support shorthand ticket names for faster workflow:

       **Shorthand (New):**
       ```
       /socrates feature-user-auth
       /plan enhancement-shortcuts
       /exec bug-validation-error
       ```

       **Full Paths (Still Supported):**
       ```
       /socrates specs/tickets/feature-user-auth/spec.yaml
       /plan CLAUDE.md
       /exec docs/features/authentication.md
       ```

       **Resolution Logic:**
       - If argument contains `/` or ends with `.md`/`.yaml` → Used as explicit path
       - Otherwise → Resolved to `specs/tickets/{ticket-name}/{target-file}`
       - `/socrates` and `/plan` → target `spec.yaml`
       - `/exec` → targets `plan.md`

       **Error Handling:**
       When a ticket isn't found, you'll see helpful suggestions:
       ```
       ❌ Ticket not found: my-feature

       Did you mean:
       • feature-my-feature → /socrates feature-my-feature
       • enhancement-my-features → /socrates enhancement-my-features

       Or create it: cdd new feature my-feature
       ```
       ```
   - **Expected Outcome:** Complete documentation of shorthand feature
   - **Verification:** Read through for clarity and accuracy
   - **Potential Blockers:** None (documentation only)

2. **Update README Examples** (15 min)
   - **Actions:**
     - Open `README.md`
     - Find usage examples section
     - Update slash command examples to show shorthand:
       ```markdown
       # Quick Start (after reading)

       1. Edit CLAUDE.md with your project context
       2. Create a ticket: `cdd new feature user-authentication`
       3. Gather requirements: `/socrates feature-user-authentication`
       4. Generate plan: `/plan feature-user-authentication`
       5. Implement: `/exec feature-user-authentication`
       ```
   - **Expected Outcome:** README demonstrates modern shorthand syntax
   - **Verification:** Examples are consistent with CLI_REFERENCE.md
   - **Potential Blockers:** None (markdown edit)

3. **Code Cleanup & Quality Checks** (25 min)
   - **Actions:**
     - Format code: `poetry run black src/cddoc/`
     - Lint code: `poetry run ruff check src/cddoc/`
     - Fix any linting issues
     - Remove any debug print statements
     - Ensure all docstrings are complete
   - **Expected Outcome:** Code passes all quality gates
   - **Success Criteria:** Black and Ruff pass with no errors
   - **Potential Blockers:** Linting errors requiring fixes

---

## Testing Strategy

### Unit Tests to Add

**File:** `tests/test_path_resolver.py`

**Test Coverage:**
1. **Shorthand Resolution:**
   - `test_resolve_shorthand_to_spec_yaml()` - Basic shorthand → spec.yaml
   - `test_resolve_shorthand_to_plan_md()` - Basic shorthand → plan.md
   - `test_resolve_different_target_files()` - Same ticket, different targets

2. **Explicit Path Passthrough:**
   - `test_resolve_explicit_relative_path()` - Paths with `/` used as-is
   - `test_resolve_explicit_absolute_path()` - Absolute paths preserved
   - `test_resolve_file_with_extension()` - Files ending in .md/.yaml preserved

3. **Fuzzy Matching:**
   - `test_find_similar_tickets_exact_match()` - Exact matches excluded from suggestions
   - `test_find_similar_tickets_partial()` - Partial matches included
   - `test_find_similar_tickets_threshold()` - Below-threshold matches excluded
   - `test_find_similar_tickets_max_three()` - Only top 3 returned
   - `test_find_similar_tickets_empty_dir()` - Handles no tickets gracefully

4. **Error Formatting:**
   - `test_format_error_with_suggestions()` - Shows suggestions
   - `test_format_error_without_suggestions()` - Shows "create it" message
   - `test_format_error_different_commands()` - Adapts to command (socrates vs plan)

5. **Edge Cases:**
   - `test_resolve_ticket_with_special_chars()` - Handles dashes, underscores
   - `test_resolve_ticket_case_sensitivity()` - Case-sensitive matching
   - `test_resolve_empty_argument()` - Handles empty string
   - `test_resolve_nonexistent_ticket()` - Raises PathResolutionError

### Manual Testing Checklist

**Pre-implementation baseline:**
- [ ] All existing slash commands work with full paths
- [ ] Error messages for missing files are clear

**Post-implementation validation:**
- [ ] `/socrates feature-user-auth` loads correct spec.yaml
- [ ] `/plan feature-user-auth` loads correct spec.yaml
- [ ] `/exec feature-user-auth` loads plan.md (not spec.yaml)
- [ ] Full paths still work: `/socrates specs/tickets/feature-x/spec.yaml`
- [ ] Non-ticket files work: `/socrates CLAUDE.md`
- [ ] Nonexistent ticket shows fuzzy matches
- [ ] Error message includes "cdd new" suggestion when no matches
- [ ] Error formatting uses Rich styling (colored, formatted)
- [ ] Slash command conversation flow feels natural

---

## Risk Assessment

### Risks & Mitigation

1. **Risk: Ambiguous ticket names (multiple tickets match shorthand)**
   - Likelihood: Low (ticket names include type prefix, unlikely duplicates)
   - Impact: Medium (wrong file loaded)
   - Mitigation: Exact directory name match required, no partial matching for resolution
   - Fallback: User uses full path for disambiguation

2. **Risk: Performance degradation with many tickets (>1000)**
   - Likelihood: Low (typical projects have <100 tickets)
   - Impact: Low (only affects error path, not happy path)
   - Mitigation: Fuzzy matching only runs on error, not every invocation
   - Fallback: Could add caching if needed in future

3. **Risk: Breaking existing slash command workflows**
   - Likelihood: Very Low (backward compatible design)
   - Impact: High (disrupts users)
   - Mitigation: Explicit path detection ensures full paths always work
   - Fallback: Can revert slash command markdown edits easily

4. **Risk: Confusing error messages**
   - Likelihood: Medium (error UX is subjective)
   - Impact: Low (doesn't break functionality)
   - Mitigation: Follow established three-part error pattern, use Rich formatting
   - Fallback: Can iterate on error message wording based on feedback

### Rollback Strategy

**If Enhancement Fails:**
1. Revert slash command markdown files (`.claude/commands/*.md`)
2. Remove PathResolver import statements from affected files
3. Delete `src/cddoc/path_resolver.py` and `tests/test_path_resolver.py`
4. Revert documentation changes (README, CLI_REFERENCE, Next Steps)
5. Verify all tests pass without PathResolver

**Recovery Time Objective:** <15 minutes (simple file reverts)

**Detection:** If slash commands fail to resolve paths or show errors, rollback immediately

---

## Success Metrics

### Quantitative Metrics

1. **Typing Reduction:** 50+ characters → 20-30 characters per command
   - How to measure: Count characters in examples (before/after)
   - Target: 40-60% reduction in typing

2. **Test Coverage:** Maintain or improve coverage
   - How to measure: `poetry run pytest --cov`
   - Target: Coverage ≥ current baseline

3. **Error Resolution Success:** 80%+ of fuzzy matches lead to correct ticket
   - How to measure: Manual testing with intentional typos
   - Target: Top 3 suggestions include correct ticket in >80% of cases

### Qualitative Metrics

- **Developer Experience:** Workflow feels faster and more natural
- **Error Helpfulness:** Users can recover from typos without frustration
- **Documentation Clarity:** Examples are easier to read and understand
- **Backward Compatibility:** No user reports of broken workflows

---

## Dependencies & Prerequisites

### Must Complete Before Starting

- [x] Spec.yaml completed and approved
- [ ] All existing tests passing
- [ ] Clean git working directory

### External Dependencies

None (uses Python stdlib only)

### Team Dependencies

None (solo implementation)

---

## Definition of Done

- [ ] PathResolver utility created and tested
- [ ] All 3 slash commands updated (socrates, plan, exec)
- [ ] Unit tests written and passing (≥10 test cases)
- [ ] Manual testing checklist completed (all items pass)
- [ ] Code formatted (Black) and linted (Ruff) with no errors
- [ ] Documentation updated (README, CLI_REFERENCE, Next Steps)
- [ ] All acceptance criteria met:
  - [ ] `/socrates <ticket-name>` resolves correctly
  - [ ] `/plan <ticket-name>` resolves correctly
  - [ ] `/exec <ticket-name>` resolves to plan.md
  - [ ] Full paths still work (backward compatible)
  - [ ] Non-ticket paths work (CLAUDE.md, etc.)
  - [ ] Error shows top 3 fuzzy matches
  - [ ] Error shows "create it" suggestion when no matches
  - [ ] All existing functionality unchanged
- [ ] No breaking changes
- [ ] Integration testing passed
- [ ] Success metrics validated

---

## Timeline & Effort Estimate

| Phase | Estimated Time | Confidence |
|-------|----------------|------------|
| Preparation & Analysis | 0.5 hours | High |
| Implementation | 2-3 hours | High |
| Validation & Testing | 1-2 hours | High |
| Documentation & Cleanup | 1 hour | High |
| **Total** | **4.5-6.5 hours** | **High** |

**Confidence Factors:**
- Familiar tech stack (Python, pathlib, Rich)
- Clear requirements and acceptance criteria
- Similar patterns exist in codebase (init.py, new_ticket.py)
- No external dependencies needed
- Backward compatibility design reduces risk

**Assumptions:**
- Developer familiar with Python 3.9+ and type hints
- Development environment already set up (Poetry, pytest)
- No unexpected edge cases in slash command markdown parsing
- Fuzzy matching performance adequate for typical ticket counts (<100)

---

## Post-Enhancement Monitoring

### What to Monitor

- User adoption of shorthand syntax vs full paths
- Frequency of PathResolutionError (indicates typos or missing tickets)
- Fuzzy matching accuracy (do suggestions help users?)
- Any reports of broken workflows (regression detection)

### Success Indicators

- Users naturally use shorthand in examples and discussions
- Error messages with suggestions reduce follow-up questions
- No regression reports after deployment
- Positive feedback on improved workflow speed

### Warning Signs

- Frequent "ticket not found" errors (suggests UX issue)
- Users still using full paths (suggests shorthand not discoverable)
- Reports of ambiguous resolution (suggests logic flaw)
- Performance complaints with large ticket counts

---

*Generated by CDD Framework /plan command*

# Manual Testing Checklist: Resumability & Archiving Features

> Manual testing checklist for progress tracking, resumability, and ticket archiving features.
> Created: 2025-11-03

## Overview

This checklist covers the new features implemented for automatic progress tracking, resumability, and ticket archiving in the /exec and /exec-auto commands.

**Features to Test:**
1. Progress tracking (progress.yaml creation and updates)
2. Resumability (continuing from interrupted sessions)
3. Spec status lifecycle (draft → defined → planned → in_progress → completed → archived)
4. Ticket archiving (automatic move to specs/archive/)

---

## Prerequisites

- [ ] CDD framework initialized (`cdd init`)
- [ ] Test project has CLAUDE.md
- [ ] Git repository initialized
- [ ] Poetry environment activated

---

## Test Suite 1: Progress Tracking (/exec)

### 1.1 First-Time Progress Creation

**Setup:**
```bash
cdd new feature test-progress
/socrates feature-test-progress  # Fill out spec
/plan feature-test-progress      # Generate plan
```

**Test Steps:**
1. Run `/exec feature-test-progress`
2. Check that progress.yaml is created in specs/tickets/feature-test-progress/
3. Verify progress.yaml contains:
   - [ ] plan_path field
   - [ ] spec_path field
   - [ ] started_at timestamp
   - [ ] updated_at timestamp
   - [ ] status: "in_progress"
   - [ ] steps array (empty or populated)
   - [ ] acceptance_criteria array
   - [ ] files_created array
   - [ ] files_modified array
   - [ ] issues array

**Expected Result:**
- ✅ progress.yaml created on first run
- ✅ Contains all required fields
- ✅ Timestamps are valid ISO format

---

### 1.2 Progress Updates During Implementation

**Test Steps:**
1. Continue with implementation from 1.1
2. After each step completion, check progress.yaml
3. Verify:
   - [ ] updated_at timestamp changes
   - [ ] Completed steps marked as "completed"
   - [ ] files_created/files_modified lists updated
   - [ ] TodoWrite shows real-time progress

**Expected Result:**
- ✅ Progress file updates after each step
- ✅ Completed steps properly tracked
- ✅ File lists accurate

---

### 1.3 Spec Status Updates

**Test Steps:**
1. Before running /exec, check spec.yaml status (should be "planned")
2. Run `/exec feature-test-progress`
3. Check spec.yaml during implementation:
   - [ ] Status changed to "in_progress"
   - [ ] implementation_started timestamp added
4. After completion, check spec.yaml:
   - [ ] Status changed to "completed"
   - [ ] implementation_completed timestamp added
5. After archiving, check archived spec.yaml:
   - [ ] Status changed to "archived"
   - [ ] archived_at timestamp added

**Expected Result:**
- ✅ Spec status transitions correctly through lifecycle
- ✅ All timestamps added at proper stages

---

### 1.4 Resumability - Interrupted Session

**Setup:**
```bash
cdd new feature test-resume
/socrates feature-test-resume
/plan feature-test-resume
```

**Test Steps:**
1. Run `/exec feature-test-resume`
2. **Interrupt mid-execution** (Ctrl+C after 2-3 steps)
3. Verify progress.yaml exists with partial progress
4. Run `/exec feature-test-resume` again
5. Check for resume prompt:
   ```
   📋 Progress Found!

   Previous session:
   - Started: [timestamp]
   - Last updated: [timestamp]
   - Completed: X/Y steps

   Resume from step N or start fresh? (R/S)
   ```
6. Choose "R" (Resume)
7. Verify:
   - [ ] Implementation continues from interrupted step
   - [ ] Completed steps not re-executed
   - [ ] progress.yaml updated with new progress

**Expected Result:**
- ✅ Resume prompt appears
- ✅ Can resume from exact step
- ✅ No duplicate work

---

### 1.5 Resumability - Start Fresh

**Test Steps:**
1. Using same ticket from 1.4 with existing progress.yaml
2. Run `/exec feature-test-resume`
3. Choose "S" (Start fresh) from prompt
4. Verify:
   - [ ] Old progress.yaml deleted
   - [ ] New progress.yaml created
   - [ ] Implementation starts from step 1

**Expected Result:**
- ✅ Can start fresh when desired
- ✅ Old progress cleared

---

### 1.6 Ticket Archiving on Completion

**Setup:**
```bash
cdd new feature test-archive
/socrates feature-test-archive
/plan feature-test-archive
```

**Test Steps:**
1. Run `/exec feature-test-archive` and complete all steps
2. After completion report, verify archiving message:
   ```
   📦 Ticket Archived

   Moved to: specs/archive/feature-test-archive/

   If bugs are found, restore with:
   mv specs/archive/feature-test-archive specs/tickets/feature-test-archive
   ```
3. Check file system:
   - [ ] specs/tickets/feature-test-archive/ **deleted**
   - [ ] specs/archive/feature-test-archive/ **created**
   - [ ] All files preserved (spec.yaml, plan.md, progress.yaml)
4. Check archived spec.yaml:
   - [ ] status: "archived"
   - [ ] archived_at timestamp present

**Expected Result:**
- ✅ Ticket moved to archive automatically
- ✅ All files preserved
- ✅ Spec status updated to archived

---

### 1.7 Archive Restoration

**Test Steps:**
1. Using archived ticket from 1.6
2. Manually restore:
   ```bash
   mv specs/archive/feature-test-archive specs/tickets/feature-test-archive
   ```
3. Verify ticket restored and all files present

**Expected Result:**
- ✅ Can easily restore archived tickets
- ✅ All data intact

---

## Test Suite 2: Auto Mode (/exec-auto)

### 2.1 Fully Automatic Progress Tracking

**Setup:**
```bash
cdd new feature test-auto
/socrates feature-test-auto
/plan feature-test-auto
```

**Test Steps:**
1. Run `/exec-auto feature-test-auto`
2. **Do not interact** - let it run fully automatic
3. Verify:
   - [ ] progress.yaml created automatically
   - [ ] No prompts during execution
   - [ ] Progress updates tracked in progress.yaml
   - [ ] Spec status updated to "in_progress" automatically

**Expected Result:**
- ✅ Fully automatic, no user input needed
- ✅ Progress tracked silently

---

### 2.2 Auto-Resume Without Prompting

**Test Steps:**
1. Run `/exec-auto feature-test-auto`
2. Interrupt mid-execution (Ctrl+C)
3. Run `/exec-auto feature-test-auto` again
4. Verify:
   - [ ] **No resume prompt** - automatic resume
   - [ ] Shows message: `[AUTO] Resuming from previous session...`
   - [ ] Continues from interrupted step
   - [ ] No duplicate work

**Expected Result:**
- ✅ Resumes automatically without asking
- ✅ Logs auto-resume action

---

### 2.3 Automatic Archiving

**Test Steps:**
1. Run `/exec-auto feature-test-auto` to completion
2. Verify automatic archiving messages:
   ```
   [AUTO] Updating spec.yaml status to "completed"
   [AUTO] Archiving ticket to specs/archive/feature-test-auto/
   [AUTO] Marking ticket as archived

   📦 Ticket Archived (Automatic Mode)
   ```
3. Verify:
   - [ ] Ticket moved to archive automatically
   - [ ] No confirmation prompts
   - [ ] Spec status updated to "archived"

**Expected Result:**
- ✅ Fully automatic archiving
- ✅ No user interaction required

---

### 2.4 Error Handling - Continue on Failure

**Setup:**
```bash
cdd new feature test-auto-errors
/socrates feature-test-auto-errors
# Intentionally create a plan with test that will fail
/plan feature-test-auto-errors
```

**Test Steps:**
1. Modify plan to include failing test
2. Run `/exec-auto feature-test-auto-errors`
3. Verify:
   - [ ] Execution continues despite test failures
   - [ ] Failures logged to progress.yaml issues array
   - [ ] Message shown: `[AUTO] Test Failure Detected - logging and continuing`
   - [ ] Completion report shows all issues
   - [ ] Ticket still archived at end

**Expected Result:**
- ✅ Best-effort completion
- ✅ All issues logged
- ✅ Completes successfully with warnings

---

## Test Suite 3: Edge Cases

### 3.1 Missing spec.yaml

**Test Steps:**
1. Create ticket folder manually without spec.yaml
2. Run `/exec feature-missing-spec`
3. Verify:
   - [ ] Warning shown: `⚠️ Warning: spec.yaml not found`
   - [ ] Asks to continue (Y/n)
   - [ ] Can continue without spec
   - [ ] No acceptance criteria validation

**Expected Result:**
- ✅ Graceful handling of missing spec
- ✅ Can continue with plan only

---

### 3.2 Missing CLAUDE.md

**Test Steps:**
1. Temporarily rename CLAUDE.md
2. Run `/exec feature-test`
3. Verify warning:
   ```
   ⚠️ Warning: CLAUDE.md not found
   I'll implement with general best practices.
   Continue? (Y/n)
   ```
4. Can continue without project context

**Expected Result:**
- ✅ Warns about missing context
- ✅ Can proceed with general practices

---

### 3.3 Corrupted progress.yaml

**Test Steps:**
1. Start implementation with `/exec`
2. Interrupt after progress.yaml created
3. Manually corrupt progress.yaml (invalid YAML)
4. Run `/exec` again
5. Verify:
   - [ ] Error handling detects corruption
   - [ ] Offers to start fresh or fix manually

**Expected Result:**
- ✅ Graceful error handling
- ✅ Provides recovery options

---

## Test Suite 4: Path Resolution

### 4.1 Shorthand Paths

**Test Steps:**
1. Create ticket: `cdd new feature shorthand-test`
2. Test both commands:
   ```bash
   /exec feature-shorthand-test      # Shorthand
   /exec-auto feature-shorthand-test # Shorthand
   ```
3. Verify both resolve correctly to full path

**Expected Result:**
- ✅ Shorthand paths work for both commands

---

### 4.2 Full Paths

**Test Steps:**
1. Run with full paths:
   ```bash
   /exec specs/tickets/feature-shorthand-test/plan.md
   /exec-auto specs/tickets/feature-shorthand-test/plan.md
   ```
2. Verify both work correctly

**Expected Result:**
- ✅ Full paths work for both commands

---

### 4.3 Fuzzy Matching on Typos

**Test Steps:**
1. Run with typo:
   ```bash
   /exec feature-shortnd-tst
   ```
2. Verify error message with suggestions:
   ```
   ❌ Plan not found: feature-shortnd-tst

   Did you mean:
   • feature-shorthand-test → /exec feature-shorthand-test

   Or generate a plan first: /plan feature-shortnd-tst
   ```

**Expected Result:**
- ✅ Helpful fuzzy matching suggestions
- ✅ Clear error messages

---

## Test Suite 5: Integration Tests

### 5.1 Full Workflow End-to-End

**Test entire workflow:**
```bash
# 1. Create ticket
cdd new feature full-workflow

# 2. Fill spec
/socrates feature-full-workflow

# 3. Generate plan
/plan feature-full-workflow

# 4. Implement
/exec feature-full-workflow

# 5. Verify completion
```

**Verify:**
- [ ] Spec status: draft → defined → planned → in_progress → completed → archived
- [ ] All files created correctly
- [ ] Progress tracked throughout
- [ ] Ticket archived at end
- [ ] All timestamps present in spec.yaml

**Expected Result:**
- ✅ Smooth end-to-end experience
- ✅ All features work together

---

### 5.2 Parallel Testing - Multiple Tickets

**Test Steps:**
1. Create 3 tickets simultaneously:
   ```bash
   cdd new feature ticket-a
   cdd new feature ticket-b
   cdd new feature ticket-c
   ```
2. Work on them in parallel
3. Verify each has independent progress.yaml
4. Verify archiving doesn't affect other tickets

**Expected Result:**
- ✅ Multiple tickets work independently
- ✅ No cross-contamination

---

## Test Suite 6: Documentation Accuracy

### 6.1 Verify Documentation Matches Implementation

**Check docs match reality:**
- [ ] docs/features/exec-command.md describes actual behavior
- [ ] docs/features/exec-auto-command.md describes actual behavior
- [ ] README.md directory structure accurate
- [ ] .claude/commands/exec.md prompt matches implementation
- [ ] .claude/commands/exec-auto.md prompt matches implementation

**Expected Result:**
- ✅ All docs accurate and up-to-date

---

## Summary Checklist

**Core Features:**
- [ ] Progress tracking works correctly
- [ ] Resumability works in interactive mode
- [ ] Auto-resume works in autonomous mode
- [ ] Spec status lifecycle complete
- [ ] Ticket archiving automatic
- [ ] Archive restoration possible

**Error Handling:**
- [ ] Missing files handled gracefully
- [ ] Corrupted progress handled safely
- [ ] Test failures logged (auto mode)
- [ ] Runtime errors logged (auto mode)

**User Experience:**
- [ ] Clear messages throughout
- [ ] No unexpected prompts in auto mode
- [ ] Helpful error messages
- [ ] Fuzzy matching works for typos

**Integration:**
- [ ] Full workflow smooth
- [ ] Multiple tickets work independently
- [ ] Docs match implementation

---

## Sign-Off

**Tester:** _________________
**Date:** _________________
**Result:** [ ] PASS  [ ] FAIL
**Notes:**

---

*Generated for CDD Framework v0.1.0*

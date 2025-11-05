# Bug Fix Plan: Socrates Template Loading Error

**Generated:** 2025-11-05
**Spec:** `specs/tickets/bug-socrates-error-file-load/spec.yaml`
**Ticket Type:** Bug
**Severity:** Low
**Estimated Effort:** 2-3 hours (High confidence)

---

## Bug Analysis

### Current Behavior

During Socrates initialization (Step 4), the command attempts to load template files to understand what structure a complete specification needs. However, it uses incorrect hardcoded paths:

**Incorrect Paths Used:**
- `.cddoc/templates/feature.yaml` (typo: `.cddoc` instead of `.cdd`)
- `.cdd/templates/bug.yaml` (wrong filename pattern)

**Actual Template File Structure:**
```
.cdd/templates/
├── bug-ticket-template.yaml       ← ACTUAL FILE
├── feature-ticket-template.yaml   ← ACTUAL FILE
├── spike-ticket-template.yaml
├── enhancement-ticket-template.yaml
└── [type]-plan-template.md files
```

**Reproduction Steps:**
1. Run `cdd init` and select any language (en or pt-br)
2. Create a new ticket: `cdd new bug test-bug`
3. Invoke Socrates: `/socrates specs/tickets/bug-test-bug/spec.yaml`
4. Observe initialization output showing "Error reading file" for template loading
5. Note that Socrates continues conversation successfully with good outcomes

**Observed Result:**
- Error messages displayed during initialization
- Template loading fails silently
- Socrates produces comprehensive specs anyway

### Expected Behavior

Either:
1. Socrates successfully loads template files from correct paths (`.cdd/templates/[type]-ticket-template.yaml`), OR
2. Step 4 template loading is removed entirely if determined to be redundant

**Expected Result:** No confusing error messages, clean initialization output

### Impact Assessment

- **Severity:** Low
- **Affected Users:** All users running Socrates on version 0.1.4
- **Frequency:** Every time Socrates is invoked
- **Workaround:** None needed - Socrates functions correctly despite error
- **Business Impact:**
  - Minimal user impact on functionality
  - Creates confusing/unprofessional error messages
  - May indicate unnecessary complexity in initialization

---

## Root Cause Analysis

### Hypothesis

**Primary Hypothesis:** Step 4's template loading is redundant because the target file (loaded in Step 2) already contains the full template structure.

**Evidence Supporting This Hypothesis:**

1. **`cdd new` stamps template into target file:**
   - When users run `cdd new bug name`, the mechanical layer copies the template content into `specs/tickets/bug-name/spec.yaml`
   - Target file contains complete template structure (empty or partially filled)
   - Socrates loads this target file in Step 2 of initialization

2. **Successful outcomes without template loading:**
   - Bug spec for this ticket was comprehensive despite template load failure
   - User reported good experience in conversation
   - Template errors don't block Socrates functionality

3. **Step 4 purpose is unclear:**
   - Documentation says "Know what a complete spec needs for this ticket type"
   - But target file already provides this information
   - No evidence that separate template loading adds unique value

**Secondary Hypothesis:** If Step 4 does add value, it's incorrectly implemented with wrong hardcoded paths.

### Likely Location

**Files Involved:**

1. **`src/cddoc/commands/en/socrates.md`** - English Socrates command definition
   - Lines referencing `.cddoc/templates/` (wrong directory)
   - Lines referencing `[type].yaml` (wrong filename pattern)

2. **`src/cddoc/commands/pt-br/socrates.md`** - Portuguese Socrates command definition
   - Same incorrect path references as English version

3. **`src/cddoc/commands/en/plan.md`** - English Plan command definition
   - Lines 118-120: References `.cddoc/templates/[type]-plan-template.md`
   - Line 837: Template error message with wrong path

4. **`src/cddoc/commands/pt-br/plan.md`** - Portuguese Plan command definition
   - Same incorrect path references as English plan version

5. **`docs/features/socrates.md`** - Feature documentation (if Step 4 is removed)
   - Documents 6-step initialization process
   - Would need update to 5-step if Step 4 is removed

---

## Investigation Approach

### Step 1: Analyze Template Loading Purpose

**Purpose:** Determine if Step 4 template loading provides value beyond Step 2 target file loading

**Method:**
1. Read Socrates command file around Step 4 (lines 140-180 in socrates.md)
2. Examine what information Step 4 is supposed to provide
3. Compare against what Step 2 target file provides
4. Review context synthesis (Step 6) to see if template info is used

**Expected Findings:**
- Step 4 says "Know what a complete spec needs"
- Target file (Step 2) already has complete structure (stamped by `cdd new`)
- Template sections are visible in target file comments/placeholders
- **Conclusion: Step 4 is redundant**

### Step 2: Verify Template Stamping Behavior

**Purpose:** Confirm that `cdd new` always stamps template into target file

**Method:**
1. Run `cdd new bug test-verification`
2. Examine `specs/tickets/bug-test-verification/spec.yaml`
3. Verify it contains complete bug template structure
4. Confirm structure matches `.cdd/templates/bug-ticket-template.yaml`

**Expected Findings:**
- Target file contains all template sections
- Structure is identical to template file
- Comments/placeholders guide what to fill in
- **Conclusion: Step 2 provides all template information**

### Step 3: Check for Edge Cases

**Purpose:** Identify scenarios where Step 4 might be necessary

**Method:**
1. Consider: What if user creates spec.yaml manually (not via `cdd new`)?
2. Consider: What if user works on CLAUDE.md (no template)?
3. Consider: What if target file is corrupted/incomplete?

**Expected Findings:**
- Manual spec.yaml creation is uncommon (not recommended workflow)
- CLAUDE.md has its own template (constitution-template.md)
- Corrupted files would fail at Step 2 anyway
- **Conclusion: Edge cases don't justify Step 4 complexity**

---

## Fix Strategy

### Proposed Solution

**Remove Step 4 template loading entirely** from both Socrates and Plan commands.

**Why This Approach:**

1. **Step 4 is redundant:**
   - Target file (Step 2) contains full template structure
   - `cdd new` stamps template into target file
   - No unique value provided by separate template loading

2. **Simpler is better:**
   - Reduces initialization complexity
   - Eliminates confusing error messages
   - Aligns with "AI-First Design" philosophy (conventional over clever)

3. **No functionality loss:**
   - Socrates already produces comprehensive specs without Step 4
   - User experience is already good despite template load failures
   - All necessary structure is in target file

4. **Consistent with architecture:**
   - Mechanical layer (`cdd new`) provides structure
   - Intelligence layer (Socrates) fills structure through conversation
   - Clean separation of concerns

### Alternatives Considered

**Alternative 1: Fix the Hardcoded Paths**

**Changes needed:**
- Replace `.cddoc` → `.cdd` (directory typo)
- Replace `[type].yaml` → `[type]-ticket-template.yaml` (filename pattern)

**Pros:**
- Preserves existing 6-step process
- Template loading would work as originally intended
- Minimal change to command files

**Cons:**
- Doesn't address fundamental redundancy
- Keeps unnecessary complexity in initialization
- Error messages may still occur if template files move/change
- No clear benefit over just using target file

**Why not chosen:** Fixes symptoms but not root cause. Step 4 doesn't add value worth the complexity.

**Alternative 2: Make Template Loading Optional**

**Approach:** Try to load template, fail gracefully if not found, continue normally

**Pros:**
- Backwards compatible
- Handles edge cases (missing templates)

**Cons:**
- Adds complexity (optional behavior to manage)
- Still doesn't justify keeping redundant step
- "Optional but not necessary" suggests it shouldn't exist

**Why not chosen:** If it's optional, it's probably not necessary. Remove it entirely instead.

---

## Implementation Steps

### Step 1: Remove Step 4 from English Socrates Command

**File:** `src/cddoc/commands/en/socrates.md`

**Changes:**

1. **Delete Step 4 section (lines ~144-148):**

**Before:**
```markdown
#### Step 4: Load Appropriate Template
```
view .cddoc/templates/[feature|bug|spike].yaml
```
**Purpose:** Know what a complete spec needs for this ticket type.
```

**After:** [DELETE ENTIRE SECTION]

2. **Renumber subsequent steps:**
   - Old Step 5 → New Step 4
   - Old Step 6 → New Step 5

3. **Update Step 5 (formerly Step 6) context synthesis to remove template reference:**

**Before:**
```markdown
**Template structure:** [Key sections we need to complete]
```

**After:**
```markdown
**Target file structure:** [Key sections to complete based on target file]
```

4. **Find and replace all other references:**
   - Search for: `Step 4` → Update to reflect new numbering
   - Search for: `Step 5` → Update to reflect new numbering
   - Search for: `Step 6` → Update to reflect new numbering
   - Search for: `6-step` → Replace with `5-step`
   - Search for: `.cddoc/templates` → Remove all references
   - Search for: `template loading` → Update or remove as needed

**Why This Fixes It:** Removes redundant template loading, simplifies initialization, eliminates error messages.

---

### Step 2: Remove Step 4 from Portuguese Socrates Command

**File:** `src/cddoc/commands/pt-br/socrates.md`

**Changes:** Identical to Step 1, but in Portuguese version

1. Delete Step 4 section
2. Renumber Steps 5 → 4 and 6 → 5
3. Update context synthesis
4. Find and replace template references

**Why This Fixes It:** Ensures consistency across language versions.

---

### Step 3: Fix Plan Command Template Paths (Optional Improvement)

**Files:**
- `src/cddoc/commands/en/plan.md`
- `src/cddoc/commands/pt-br/plan.md`

**Note:** Plan command loads *plan templates*, not *ticket templates*. Different use case.

**Investigation needed:**
- Do plan templates get stamped into target file? **NO** - plan.md is generated by /plan
- Does Plan command need to load plan template? **YES** - to know structure to generate

**Conclusion:** Plan's template loading is NOT redundant. Fix the paths instead of removing.

**Changes for both files:**

1. **Fix directory typo (lines ~118-120):**

**Before:**
```markdown
- Feature → Read `.cddoc/templates/feature-plan-template.md`
- Bug → Read `.cddoc/templates/bug-plan-template.md`
- Spike → Read `.cddoc/templates/spike-plan-template.md`
```

**After:**
```markdown
- Feature → Read `.cdd/templates/feature-plan-template.md`
- Bug → Read `.cdd/templates/bug-plan-template.md`
- Spike → Read `.cdd/templates/spike-plan-template.md`
```

2. **Fix error message path (line ~837):**

**Before:**
```markdown
Expected: `.cddoc/templates/[feature|bug|spike]-plan-template.md`
```

**After:**
```markdown
Expected: `.cdd/templates/[feature|bug|spike]-plan-template.md`
```

**Why This Fixes It:** Plan generates plan.md from scratch, needs template to know structure. Fixing paths ensures templates load correctly.

---

### Step 4: Update Feature Documentation

**File:** `docs/features/socrates.md`

**Changes:**

1. **Update initialization process description (lines ~100-130):**

**Before:**
```markdown
**Step 1**: Load CLAUDE.md (project foundation)
**Step 2**: Read target file (current state)
**Step 3**: Determine file type from path pattern
**Step 4**: Load appropriate template
**Step 5**: Intelligent reconnaissance (related context)
**Step 6**: Synthesize and present findings
```

**After:**
```markdown
**Step 1**: Load CLAUDE.md (project foundation)
**Step 2**: Read target file (current state with template structure)
**Step 3**: Determine file type from path pattern
**Step 4**: Intelligent reconnaissance (related context)
**Step 5**: Synthesize and present findings
```

2. **Update description of Step 2:**

**Before:**
```markdown
**Step 2: Read Target File**
- Examines current state of the file
- Identifies what exists and what's missing
- Determines starting point for conversation
```

**After:**
```markdown
**Step 2: Read Target File**
- Examines current state of the file (includes full template structure from `cdd new`)
- Identifies what exists and what's missing
- Template structure guides what sections need completion
- Determines starting point for conversation
```

3. **Update any references to "6-step process" → "5-step process"**

4. **Remove template loading from initialization phase description**

**Why This Updates Docs:** Keeps documentation accurate and reflects simplified initialization process.

---

## Testing Strategy

### Verification Test 1: Socrates Runs Without Errors

**Test:** Manual testing of Socrates initialization

**Steps:**
1. Create test ticket: `cdd new bug test-socrates-fix`
2. Run: `/socrates specs/tickets/bug-test-socrates-fix/spec.yaml`
3. Observe initialization output

**Expected Result:**
- ✅ No "Error reading file" messages
- ✅ Clean initialization output
- ✅ Context loaded successfully
- ✅ 5 steps displayed (not 6)
- ✅ Conversation proceeds normally

**Validation:**
- Screenshot or copy initialization output
- Verify no template-related errors
- Confirm spec generation works end-to-end

---

### Verification Test 2: Plan Command Template Loading Works

**Test:** Verify Plan command correctly loads plan templates after path fix

**Steps:**
1. Use existing spec: `specs/tickets/bug-socrates-error-file-load/spec.yaml`
2. Run: `/plan bug-socrates-error-file-load`
3. Observe initialization output

**Expected Result:**
- ✅ No "Error reading file" messages for plan template
- ✅ Plan template loads from `.cdd/templates/bug-plan-template.md`
- ✅ Plan generation completes successfully
- ✅ Output plan.md follows template structure

**Validation:**
- Check plan.md matches bug-plan-template.md structure
- Verify all template sections are populated
- Confirm no path-related errors

---

### Verification Test 3: Cross-Language Consistency

**Test:** Verify both English and Portuguese versions work correctly

**Steps:**
1. Change `.cdd/config.yaml` to `language: pt-br`
2. Create test ticket: `cdd new feature teste-pt-br`
3. Run: `/socrates specs/tickets/feature-teste-pt-br/spec.yaml`
4. Observe initialization (should be in Portuguese)
5. Verify no template errors
6. Switch back to `language: en` and repeat

**Expected Result:**
- ✅ Both language versions initialize without errors
- ✅ Portuguese version displays in Portuguese
- ✅ English version displays in English
- ✅ No template loading errors in either language

---

### Regression Test: Manual Spec Creation Edge Case

**Test:** Verify Socrates works if user manually creates spec.yaml (not via `cdd new`)

**Steps:**
1. Manually create: `specs/tickets/bug-manual-test/spec.yaml` with minimal content:
   ```yaml
   title: "Manual test"
   ticket:
     type: bug
   ```
2. Run: `/socrates specs/tickets/bug-manual-test/spec.yaml`
3. Observe Socrates behavior

**Expected Result:**
- ✅ Socrates detects incomplete spec
- ✅ Recommends using `cdd new` OR proceeds with minimal content
- ✅ No template loading errors
- ✅ Conversation helps fill in missing sections

**Note:** Manual creation is not recommended workflow, but Socrates should handle gracefully.

---

## Regression Prevention

### New Validation to Add

**Update command file validation (if it exists):**

If there's any automated testing for command files:
1. Validate that all file path references in command files use `.cdd` (not `.cddoc`)
2. Validate that template file references match actual filenames in `.cdd/templates/`
3. Consider adding a test that runs Socrates and checks for error messages in output

**Documentation to Update:**

1. ✅ `docs/features/socrates.md` - Update initialization process (covered in implementation)
2. ✅ Verify any Getting Started guides reference 5-step process (not 6-step)
3. ✅ Check for any other docs mentioning Socrates initialization

### Edge Cases to Consider

**Edge Case 1: Templates directory doesn't exist**
- Current behavior: Error during `cdd init` (templates not installed)
- After fix: Same behavior (not affected by this change)
- No regression

**Edge Case 2: User hasn't run `cdd init`**
- Current behavior: Socrates may fail if templates missing
- After fix: Socrates relies on target file (created by `cdd new`), so still works
- Improvement (more resilient)

**Edge Case 3: Language-specific templates in future**
- Current: Templates are in `.cdd/templates/` (language-agnostic filenames)
- After fix: Socrates doesn't load templates separately, uses target file
- Future-proof (no impact if templates become language-specific)

### Validation Checklist

After implementation, verify:

- ✅ No references to `.cddoc` in any command files
- ✅ All template path references are correct
- ✅ Socrates initialization has 5 steps (not 6)
- ✅ Plan initialization still loads plan templates correctly
- ✅ Documentation reflects 5-step process
- ✅ Both EN and PT-BR versions are consistent
- ✅ Manual testing confirms no errors
- ✅ User experience is clean and professional

---

## Rollback Plan

### If Fix Causes Issues

**Scenario:** After removing Step 4, if it's discovered that template loading was necessary for edge cases

**Rollback Steps:**
1. Revert changes to command files:
   - `git checkout src/cddoc/commands/en/socrates.md`
   - `git checkout src/cddoc/commands/pt-br/socrates.md`
2. Apply just the path fixes (Alternative 1 from Fix Strategy):
   - Change `.cddoc` → `.cdd`
   - Change `[type].yaml` → `[type]-ticket-template.yaml`
3. Revert documentation changes
4. Document why Step 4 was needed

**Alternative Rollback (Partial):**
- Keep Step 4 removed in Socrates
- Keep plan.md path fixes
- Document that template loading was unnecessary

### If Path Fixes for Plan Command Cause Issues

**Rollback Steps:**
1. Revert plan.md command files:
   - `git checkout src/cddoc/commands/en/plan.md`
   - `git checkout src/cddoc/commands/pt-br/plan.md`
2. Investigate if plan templates need different location
3. Update paths to correct location

### Monitoring After Deployment

**What to Monitor:**

1. **User Reports:**
   - Watch for GitHub issues mentioning Socrates errors
   - Monitor for confusion about initialization process
   - Check for reports of incomplete specs

2. **Self-Testing:**
   - Run Socrates on various ticket types (feature, bug, spike)
   - Verify initialization output is clean
   - Confirm spec generation quality remains high

3. **Edge Cases:**
   - Test manually created spec files
   - Test with missing templates directory
   - Test both language versions

**Success Criteria:**
- No error messages during Socrates initialization
- User experience is smooth and professional
- Spec generation quality unchanged or improved
- No increase in bug reports related to Socrates

---

## Effort Estimation

| Activity                          | Estimated Time | Assumptions |
|-----------------------------------|----------------|-------------|
| Investigation (Steps 1-3)         | 0.5 hours      | Template loading value is clear from analysis |
| Implementation (EN Socrates)      | 0.25 hours     | Simple find-replace and section deletion |
| Implementation (PT-BR Socrates)   | 0.25 hours     | Identical changes to Portuguese version |
| Implementation (Plan path fixes)  | 0.25 hours     | Two simple path corrections per file |
| Documentation updates             | 0.5 hours      | Update docs/features/socrates.md |
| Manual testing                    | 0.5 hours      | Run all verification tests |
| Regression testing                | 0.25 hours     | Test edge cases |
| **Total**                         | **2.5 hours**  | **High confidence** |

**Key Assumptions:**

1. Step 4 investigation confirms redundancy (expected outcome)
2. No Python code changes needed (all markdown edits)
3. No unexpected side effects from removing Step 4
4. Test environment is already set up
5. Familiar with command file structure

**Risks to Estimate:**

- **If investigation reveals Step 4 is valuable:** +1-2 hours
  - Would require implementing Alternative 1 (path fixes) instead
  - More complex changes to preserve functionality

- **If language-specific handling is needed:** +0.5-1 hour
  - Current assumption: Both languages have identical structure
  - If PT-BR has different template references, more work needed

- **If documentation is more extensive than expected:** +0.5-1 hour
  - Assumed only socrates.md needs updates
  - If getting-started guides or other docs mention 6-step process, more updates needed

**Confidence Level:** High (±20%)
- Changes are well-defined and localized
- Similar to standard refactoring work
- Clear success criteria
- Manual testing is straightforward

---

## Definition of Done

- ✅ Investigation confirms Step 4 is redundant (or identifies value)
- ✅ Step 4 removed from English Socrates command file
- ✅ Step 4 removed from Portuguese Socrates command file
- ✅ Steps renumbered (5 → 4, 6 → 5) in both files
- ✅ Plan command template paths fixed (`.cddoc` → `.cdd`)
- ✅ Documentation updated (docs/features/socrates.md)
- ✅ All template path references corrected
- ✅ Manual testing passes (Verification Tests 1-3)
- ✅ Regression testing passes (edge cases covered)
- ✅ No "Error reading file" messages in Socrates initialization
- ✅ User experience is clean and professional
- ✅ Both EN and PT-BR versions are consistent
- ✅ Code follows CLAUDE.md conventions (minimal, clear, AI-readable)
- ✅ Changes committed with clear commit message
- ✅ This plan is archived with implementation notes

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: specs/tickets/bug-socrates-error-file-load/spec.yaml*

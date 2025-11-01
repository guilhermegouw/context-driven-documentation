# Implementation Plan: /plan Command - Software Architect Persona

**Generated:** 2025-11-01
**Spec:** `specs/tickets/feature-command-plan/spec.yaml`
**Ticket Type:** Feature
**Estimated Effort:** 2-3 days

---

## Executive Summary

Implement a `/plan` slash command that acts as a "Software Architect Expert" persona. When invoked with a spec.yaml path, it autonomously generates a detailed implementation plan (plan.md) by reading the spec, project context (CLAUDE.md), and analyzing codebase patterns. The Planner makes ~90% of decisions autonomously and asks concise questions (with recommendations) only when genuinely ambiguous.

**Key Deliverables:**
1. `.claude/commands/plan.md` - Planner persona slash command definition
2. `.cddoc/templates/feature-plan-template.md` - Feature implementation plan template
3. `.cddoc/templates/bug-plan-template.md` - Bug fix plan template
4. `.cddoc/templates/spike-plan-template.md` - Spike investigation plan template

---

## Architecture Overview

### Interaction Flow

```
User: /plan specs/tickets/my-feature/spec.yaml

Planner:
  1. Reads spec.yaml → understands requirements
  2. Reads CLAUDE.md → loads project context
  3. Analyzes codebase → identifies patterns
  4. Detects ticket type (feature/bug/spike)
  5. Makes autonomous decisions (~90%)
  6. Asks 1-3 questions if genuinely ambiguous (with recommendations)
  7. Generates plan.md from appropriate template
  8. Saves plan.md in same directory as spec.yaml
```

### Design Philosophy

**Autonomous-First Approach:**
- The Planner is a **senior architect**, not a questioner
- It makes confident decisions based on context
- It only asks when there's genuine ambiguity with significant impact
- Questions always include recommendations with brief rationale

**AI-to-AI Communication:**
- The generated plan is for another AI to implement
- Use definitive language ("will", "must", "create") not tentative ("should", "could", "might")
- Include concrete examples, specific file paths, code snippets
- Break down steps to be granular and actionable

---

## Implementation Steps

### Phase 1: Create Plan Templates (1 day)

These templates define the structure that the Planner will populate with ticket-specific details.

#### Step 1.1: Create Feature Plan Template
**File:** `.cddoc/templates/feature-plan-template.md`

**Purpose:** Structure for feature implementation plans - comprehensive, step-by-step guide for building new functionality.

**Template Sections:**
1. **Implementation Overview**
   - Summary of what's being built
   - High-level approach and architecture
   - Key technical decisions with rationale

2. **Technical Decisions**
   - Architectural choices (with rationale)
   - Library/framework selections (with versions)
   - Design patterns to use
   - Data modeling decisions

3. **File Structure**
   - New files to create (with paths)
   - Existing files to modify (with paths)
   - Files to reference for patterns

4. **Implementation Steps** (granular, ordered)
   - Step 1: [Action] - [Expected outcome]
   - Step 2: [Action] - [Expected outcome]
   - etc.

5. **Data Models & API Contracts**
   - Database schemas (if applicable)
   - API request/response structures
   - Type definitions
   - Data flow diagrams (text-based)

6. **Test Cases**
   - Unit tests with specific assertions
   - Integration tests with scenarios
   - Edge cases to cover
   - Expected test coverage

7. **Error Handling**
   - Error scenarios to handle
   - Error message templates
   - Fallback behaviors
   - Logging requirements

8. **Integration Points**
   - Where this feature connects to existing code
   - Dependencies on other modules
   - Impact on existing functionality

9. **Dependencies**
   - New packages to install (with versions)
   - Existing dependencies to leverage
   - Version constraints

10. **Effort Estimation**
    - Implementation time
    - Testing time
    - Documentation time
    - Review time
    - Total estimated effort
    - Assumptions that affect estimate

**See Detailed Template Content Below (Section: Template Implementations)**

#### Step 1.2: Create Bug Plan Template
**File:** `.cddoc/templates/bug-plan-template.md`

**Purpose:** Structure for bug fix plans - focused on diagnosis, root cause, and fix implementation.

**Template Sections:**
1. **Bug Analysis**
   - Current behavior description
   - Expected behavior description
   - Impact assessment
   - Root cause hypothesis

2. **Investigation Approach**
   - Files to examine
   - Logs to check
   - Tests to run for reproduction
   - Debugging strategy

3. **Fix Strategy**
   - Proposed solution approach
   - Alternative approaches considered (with trade-offs)
   - Why this approach is best

4. **Implementation Steps**
   - Step-by-step fix implementation
   - Code changes with file paths
   - Expected outcomes per step

5. **Regression Prevention**
   - New tests to add
   - Edge cases to cover
   - Validation checklist

6. **Testing Strategy**
   - Reproduction test (verifies bug exists)
   - Fix validation test (verifies bug is fixed)
   - Regression tests (ensures no new bugs)

7. **Rollback Plan**
   - If fix doesn't work or causes issues
   - How to safely revert

8. **Effort Estimation**
   - Investigation time
   - Fix implementation time
   - Testing time
   - Total effort

**See Detailed Template Content Below (Section: Template Implementations)**

#### Step 1.3: Create Spike Plan Template
**File:** `.cddoc/templates/spike-plan-template.md`

**Purpose:** Structure for research/investigation spikes - time-boxed exploration to answer questions or evaluate options.

**Template Sections:**
1. **Research Objectives**
   - Questions to answer
   - Decisions this will inform
   - Success criteria (how we know we're done)

2. **Investigation Scope**
   - In scope: What we'll research
   - Out of scope: What we won't research
   - Timebox: Maximum time to spend

3. **Research Methods**
   - Documentation to review
   - Code to examine
   - Prototypes to build
   - Tools to evaluate
   - Benchmarks to run

4. **Investigation Steps**
   - Step 1: [Research activity] - [Expected findings]
   - Step 2: [Research activity] - [Expected findings]
   - etc.

5. **Evaluation Criteria**
   - Metrics to measure
   - Trade-offs to consider
   - Decision factors

6. **Deliverables**
   - Documentation to produce
   - Prototypes to create
   - Findings to document
   - Recommendations to make

7. **Effort Estimation**
   - Research time
   - Documentation time
   - Total effort (time-boxed)

**See Detailed Template Content Below (Section: Template Implementations)**

---

### Phase 2: Create Planner Persona (1 day)

#### Step 2.1: Create Plan Slash Command
**File:** `.claude/commands/plan.md`

**Purpose:** Define the Planner persona - a senior software architect who generates implementation plans autonomously.

**Key Components of the Persona:**

1. **Persona Definition**
   - Identity: Senior Software Architect and Technical Planner
   - Traits: Confident, autonomous, pragmatic, detail-oriented
   - Approach: Make decisions based on context, ask only when genuinely needed

2. **Mission Statement**
   - Transform spec.yaml into actionable implementation plan
   - Make autonomous decisions using project context
   - Ask concise questions only for genuine ambiguity
   - Generate plan.md that another AI can execute without major decisions

3. **Initialization Process** (Critical - loads context before planning)
   ```
   Step 1: Parse command argument → extract spec.yaml path
   Step 2: Read spec.yaml → understand requirements
   Step 3: Read CLAUDE.md → load project context
   Step 4: Detect ticket type → determine template
   Step 5: Load appropriate template → understand plan structure
   Step 6: Analyze codebase → find patterns
   Step 7: Make autonomous decisions
   Step 8: Identify ambiguities
   Step 9: Ask questions if needed (with recommendations)
   Step 10: Generate plan.md
   ```

4. **Decision-Making Logic** (When to decide vs when to ask)

   **Decide Autonomously When:**
   - Clear from CLAUDE.md (tech stack, patterns, conventions)
   - Industry best practice (REST API design, error handling patterns)
   - Inferable from codebase (existing patterns to follow)
   - Low architectural impact (implementation details)
   - Template provides guidance

   **Ask Questions When:**
   - Genuine ambiguity with significant impact (e.g., "Should this be real-time or batch?")
   - Missing critical integration info (e.g., "Which auth service to integrate with?")
   - Performance/scale trade-offs (e.g., "Expected load is 100 or 10,000 requests/sec?")
   - Security decisions beyond spec (e.g., "Encrypt data at rest?")

   **Never Ask About:**
   - Things already specified in CLAUDE.md
   - Industry standard practices
   - Implementation details the implementing AI can decide
   - Minor coding preferences

5. **Question Format** (Concise with recommendations)
   ```markdown
   ❓ [Specific question that affects the plan]

   💡 Recommendation: [Your suggested approach]
   Rationale: [Brief 1-2 sentence explanation]

   Alternatives:
   - Option A: [Pros/Cons]
   - Option B: [Pros/Cons]

   Which direction should I take?
   ```

6. **Context Analysis Instructions**
   - How to read and synthesize CLAUDE.md
   - How to detect patterns in existing code
   - How to infer conventions from codebase
   - How to match ticket type to template

7. **Plan Generation Instructions**
   - Load appropriate template
   - Populate each section with ticket-specific details
   - Use concrete examples and code snippets
   - Specify exact file paths
   - Use definitive language
   - Include effort estimates with assumptions

8. **Output Instructions**
   - Show brief summary of decisions made
   - Show any questions (if needed)
   - After questions answered, generate plan.md
   - Save to same directory as spec.yaml
   - Confirm success with file path

**See Detailed Persona Content Below (Section: Persona Implementation)**

---

### Phase 3: Integration & Polish (0.5 days)

#### Step 3.1: Test Planner with Real Specs
**Testing Approach:**
1. Test with feature spec (like `specs/tickets/feature-command-plan/spec.yaml`)
2. Test with bug spec (create sample bug spec)
3. Test with spike spec (create sample spike spec)
4. Verify:
   - ✅ Planner reads spec.yaml correctly
   - ✅ Planner loads CLAUDE.md context
   - ✅ Planner detects ticket type correctly
   - ✅ Planner uses appropriate template
   - ✅ Planner makes autonomous decisions
   - ✅ Planner asks questions only when needed
   - ✅ Generated plan.md is comprehensive and actionable
   - ✅ Another Claude instance can implement from the plan

#### Step 3.2: Update Documentation
**Files to Update:**
1. **CLAUDE.md** - Add `/plan` to slash commands documentation
2. **CLI next steps messages** - Reference `/plan` command after ticket creation
3. **README** (if exists) - Document the planning workflow

**Example Next Steps Update in `cli.py:_display_ticket_success()`:**
```python
next_steps = f"""[bold]Next Steps:[/bold]

1. 📝 Fill out your ticket specification:
   - In Claude Code, run: [cyan]/socrates {ticket_path / "spec.yaml"}[/cyan]
   - Have a natural conversation with Socrates AI
   - Your specification will be built through dialogue

2. 🎯 Generate implementation plan:
   - In Claude Code, run: [cyan]/plan {ticket_path / "spec.yaml"}[/cyan]
   - Planner will analyze your spec and create a detailed plan
   - Review the generated plan: [cyan]{ticket_path / "plan.md"}[/cyan]

3. 🚀 Start implementation:
   - Use the plan.md as your implementation guide
   - Claude will have full context from spec + plan
   - Build with confidence!
"""
```

---

## Technical Decisions & Rationale

### Decision 1: Templates in Markdown, Not YAML
**Choice:** Use `.md` (Markdown) for plan templates
**Rationale:**
- Plans are rich documents with sections, code snippets, examples
- Markdown is more readable and flexible than YAML
- Easier for AI to generate formatted content
- Matches documentation convention (CLAUDE.md)

**Alternative Considered:** YAML templates (like spec templates)
**Why Not:** Too rigid for the free-form nature of implementation plans

### Decision 2: Autonomous-First Interaction
**Choice:** Planner makes ~90% of decisions autonomously, asks minimal questions
**Rationale:**
- Reduces cognitive load on user
- Faster workflow (no long conversation)
- Leverages project context (CLAUDE.md) effectively
- Different from Socrates (conversational) - complementary tools

**Alternative Considered:** Conversational like Socrates
**Why Not:** Redundant with Socrates, slower for users who want quick plans

### Decision 3: No CLI Command, Only Slash Command
**Choice:** Implement only `/plan` slash command, no `cdd plan` CLI command
**Rationale:**
- Planning is AI-driven, requires intelligence and context analysis
- Slash commands are for AI-driven operations
- CLI commands are for mechanical operations (init, new)
- Keeps separation of concerns clean

**Alternative Considered:** Both CLI and slash command
**Why Not:** CLI would just wrap slash command, adding no value

### Decision 4: Plan.md Location
**Choice:** Save plan.md in same directory as spec.yaml
**Rationale:**
- Keeps related artifacts together
- Easy to find (spec.yaml → plan.md → implementation)
- Version controlled together
- Clear file structure: `specs/tickets/[name]/spec.yaml` + `plan.md`

**Alternative Considered:** Separate plans/ directory
**Why Not:** Separates related artifacts, harder to track

### Decision 5: Template Selection by Ticket Type
**Choice:** Detect ticket type from spec.yaml, use corresponding template
**Rationale:**
- Feature/bug/spike have different planning needs
- Automates template selection (user doesn't choose)
- Ensures appropriate structure for ticket type

**How Detection Works:**
```yaml
# In spec.yaml
ticket:
  type: feature  # or bug, or spike
```

**Fallback:** If type not found, ask user which template to use

### Decision 6: Question Format with Recommendations
**Choice:** When Planner asks questions, always include recommendation with rationale
**Rationale:**
- Reduces decision burden on user (they can accept recommendation)
- Shows AI is thinking, not just delegating decisions
- Makes questions feel collaborative, not lazy
- Senior architect would make a recommendation

**Example:**
```markdown
❓ Should user authentication use session cookies or JWT tokens?

💡 Recommendation: JWT tokens with httpOnly cookies
Rationale: Your project uses FastAPI (per CLAUDE.md), which is stateless by design. JWT aligns with stateless architecture and enables horizontal scaling.

Alternatives:
- Session cookies: Simpler but requires server-side session storage (Redis)
- JWT: Stateless, scalable, but requires careful security (short expiry, refresh tokens)
```

---

## File-by-File Implementation Details

### File 1: `.cddoc/templates/feature-plan-template.md`

**Purpose:** Template for feature implementation plans

**Content Structure:**
```markdown
# Implementation Plan: [Feature Title]

**Generated:** [auto-generated date]
**Spec:** `[path to spec.yaml]`
**Ticket Type:** Feature
**Estimated Effort:** [time estimate]

---

## Executive Summary

[1-2 paragraph overview of what's being built and the high-level approach]

**Key Deliverables:**
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

---

## Technical Decisions

### Decision 1: [Decision Title]
**Choice:** [What was decided]
**Rationale:** [Why this choice]
**Alternatives Considered:** [Other options and why not chosen]

### Decision 2: [Decision Title]
**Choice:** [What was decided]
**Rationale:** [Why this choice]
**Alternatives Considered:** [Other options and why not chosen]

[Continue for all major decisions...]

---

## File Structure

### New Files to Create

1. **`[path/to/file1.py]`**
   - Purpose: [What this file does]
   - Key components: [Classes, functions, exports]

2. **`[path/to/file2.py]`**
   - Purpose: [What this file does]
   - Key components: [Classes, functions, exports]

### Existing Files to Modify

1. **`[path/to/existing.py]`**
   - Changes: [What needs to be modified]
   - Location: [Function/class to modify]

2. **`[path/to/another.py]`**
   - Changes: [What needs to be modified]
   - Location: [Function/class to modify]

### Files to Reference for Patterns

1. **`[path/to/pattern-example.py]`**
   - Pattern: [What pattern to follow]
   - Reason: [Why this is the reference]

---

## Data Models & API Contracts

### Database Schema (if applicable)

```sql
-- [Table 1]
CREATE TABLE [table_name] (
  id SERIAL PRIMARY KEY,
  [field1] [type] [constraints],
  [field2] [type] [constraints],
  created_at TIMESTAMP DEFAULT NOW()
);

-- [Table 2]
CREATE TABLE [table_name] (
  ...
);
```

### Type Definitions

```python
# [Model 1]
class [ModelName]:
    [field1]: [type]
    [field2]: [type]

# [Model 2]
class [ModelName]:
    [field1]: [type]
    [field2]: [type]
```

### API Contracts

**Endpoint 1: `[METHOD] /api/[path]`**

Request:
```json
{
  "[field]": "[type/example]",
  "[field]": "[type/example]"
}
```

Response (Success - 200):
```json
{
  "[field]": "[type/example]",
  "[field]": "[type/example]"
}
```

Response (Error - 4xx/5xx):
```json
{
  "error": "[error message pattern]",
  "details": "[additional context]"
}
```

**Endpoint 2: `[METHOD] /api/[path]`**
[Same structure...]

---

## Implementation Steps

Execute these steps in order. Each step has a clear outcome.

### Step 1: [Action Description]
**Outcome:** [What will exist/work after this step]

**Details:**
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Code Example:**
```python
# [Brief code snippet showing the implementation]
```

**Validation:** [How to verify this step is complete]

---

### Step 2: [Action Description]
**Outcome:** [What will exist/work after this step]

**Details:**
- [Specific action 1]
- [Specific action 2]

**Code Example:**
```python
# [Brief code snippet]
```

**Validation:** [How to verify this step is complete]

---

[Continue for all implementation steps...]

---

## Test Cases

### Unit Tests

**Test 1: `test_[functionality]`**
```python
def test_[functionality]():
    # Arrange
    [setup code]

    # Act
    [action]

    # Assert
    assert [expected outcome]
```

**Test 2: `test_[edge_case]`**
```python
def test_[edge_case]():
    # [Test implementation]
```

[Continue for all unit tests...]

### Integration Tests

**Test 1: `test_[integration_scenario]`**
```python
def test_[integration_scenario]():
    # Test description: [What this tests]
    # Expected: [Expected outcome]
```

[Continue for integration tests...]

### Expected Test Coverage
- Unit test coverage: [percentage]% minimum
- Critical paths: 100% coverage
- Edge cases: [specific cases to cover]

---

## Error Handling

### Error Scenario 1: [Scenario Description]
**Trigger:** [What causes this error]
**Error Message:** "[Exact error message]"
**HTTP Status:** [Status code if API]
**Recovery:** [How the system should handle/recover]
**User Impact:** [What the user experiences]

### Error Scenario 2: [Scenario Description]
[Same structure...]

### Logging Requirements
- **Info level:** [What to log at info]
- **Warning level:** [What to log at warning]
- **Error level:** [What to log at error]

---

## Integration Points

### Integration 1: [System/Module Name]
**Connection Point:** [Where/how it connects]
**Data Flow:** [What data is exchanged]
**Dependencies:** [What this integration depends on]
**Error Handling:** [What happens if integration fails]

### Integration 2: [System/Module Name]
[Same structure...]

---

## Dependencies

### New Dependencies to Install

```bash
# [Package 1]
[package-name]==[version]  # [Purpose/reason]

# [Package 2]
[package-name]==[version]  # [Purpose/reason]
```

**Installation:**
```bash
poetry add [package-name]==[version]
# or
pip install [package-name]==[version]
```

### Existing Dependencies to Leverage
- **[Package Name]**: [How it's used in this feature]
- **[Package Name]**: [How it's used in this feature]

### Version Constraints
- Python: [version requirement]
- [Framework]: [version requirement]

---

## Effort Estimation

| Activity              | Estimated Time | Assumptions |
|-----------------------|----------------|-------------|
| Implementation        | [X hours]      | [Assumption 1, Assumption 2] |
| Unit Testing          | [X hours]      | [Assumption 1] |
| Integration Testing   | [X hours]      | [Assumption 1] |
| Documentation         | [X hours]      | [Assumption 1] |
| Code Review           | [X hours]      | [Assumption 1] |
| **Total**             | **[X hours]**  | **[Y days]** |

**Key Assumptions:**
1. [Assumption that affects estimate]
2. [Assumption that affects estimate]
3. [Assumption that affects estimate]

**Risks to Estimate:**
- [Risk 1]: Could add [X hours]
- [Risk 2]: Could add [X hours]

---

## Definition of Done

- ✅ All implementation steps completed
- ✅ All test cases pass
- ✅ Test coverage meets requirements
- ✅ Error handling tested
- ✅ Integration points validated
- ✅ Code formatted (Black)
- ✅ Linting passes (Ruff)
- ✅ Documentation updated
- ✅ Code reviewed and approved

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: [path to spec.yaml]*
```

**Notes:**
- `[bracketed items]` are placeholders the Planner will fill in
- `[auto-generated date]` is populated automatically
- Structure is fixed, content is ticket-specific

---

### File 2: `.cddoc/templates/bug-plan-template.md`

**Purpose:** Template for bug fix plans

**Content Structure:**
```markdown
# Bug Fix Plan: [Bug Title]

**Generated:** [auto-generated date]
**Spec:** `[path to spec.yaml]`
**Ticket Type:** Bug
**Severity:** [Critical/High/Medium/Low]
**Estimated Effort:** [time estimate]

---

## Bug Analysis

### Current Behavior
[Describe what's happening - the symptom]

**Reproduction Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Observed Result:** [What actually happens]

### Expected Behavior
[Describe what should happen]

**Expected Result:** [What should happen instead]

### Impact Assessment
- **Severity:** [Critical/High/Medium/Low]
- **Affected Users:** [Who/how many users affected]
- **Frequency:** [How often does this occur]
- **Workaround:** [Is there a workaround? What is it?]
- **Business Impact:** [Revenue, reputation, functionality impact]

---

## Root Cause Analysis

### Hypothesis
[Your best guess at the root cause based on symptoms and context]

**Evidence Supporting This Hypothesis:**
1. [Evidence 1]
2. [Evidence 2]

### Likely Location
**Files Involved:**
- `[path/to/file1.py]:[function/class]` - [Why this is suspect]
- `[path/to/file2.py]:[function/class]` - [Why this is suspect]

---

## Investigation Approach

### Step 1: [Investigation Activity]
**Purpose:** [What we're trying to learn]
**Method:** [How we'll investigate]
**Expected Findings:** [What we expect to discover]

### Step 2: [Investigation Activity]
**Purpose:** [What we're trying to learn]
**Method:** [How we'll investigate]
**Expected Findings:** [What we expect to discover]

[Continue for all investigation steps...]

---

## Fix Strategy

### Proposed Solution
[Describe the fix approach - what will be changed and how]

**Why This Approach:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

### Alternatives Considered

**Alternative 1: [Approach]**
- Pros: [Benefits]
- Cons: [Drawbacks]
- Why not chosen: [Reason]

**Alternative 2: [Approach]**
- Pros: [Benefits]
- Cons: [Drawbacks]
- Why not chosen: [Reason]

---

## Implementation Steps

### Step 1: [Action Description]
**File:** `[path/to/file.py]`
**Change:** [What to modify]

**Before:**
```python
# Current buggy code
[code snippet]
```

**After:**
```python
# Fixed code
[code snippet]
```

**Why This Fixes It:** [Explanation]

---

### Step 2: [Action Description]
**File:** `[path/to/file.py]`
**Change:** [What to modify]

[Same structure...]

---

[Continue for all implementation steps...]

---

## Testing Strategy

### Reproduction Test (Verify Bug Exists)

**Test:** `test_reproduce_[bug_name]`
```python
def test_reproduce_[bug_name]():
    """This test should FAIL before the fix, PASS after the fix."""
    # Arrange
    [setup that triggers the bug]

    # Act
    [action that causes the bug]

    # Assert
    # This assertion fails with the bug, passes with the fix
    assert [expected correct behavior]
```

### Fix Validation Tests

**Test 1: `test_[fix_scenario]`**
```python
def test_[fix_scenario]():
    # [Test that verifies the fix works]
```

**Test 2: `test_[edge_case]`**
```python
def test_[edge_case]():
    # [Test edge cases related to the fix]
```

### Regression Tests

**Test 1: `test_[related_functionality]`**
```python
def test_[related_functionality]():
    """Ensure the fix doesn't break related functionality."""
    # [Test existing functionality still works]
```

---

## Regression Prevention

### New Tests to Add
- [Test 1 description and purpose]
- [Test 2 description and purpose]

### Edge Cases to Cover
- [Edge case 1]
- [Edge case 2]
- [Edge case 3]

### Validation Checklist
- ✅ [Validation 1]
- ✅ [Validation 2]
- ✅ [Validation 3]

---

## Rollback Plan

### If Fix Doesn't Work
[Steps to safely revert the change]

### If Fix Causes New Issues
[How to detect and respond to new issues]

### Monitoring
[What to monitor after deployment to ensure fix works]

---

## Effort Estimation

| Activity              | Estimated Time | Assumptions |
|-----------------------|----------------|-------------|
| Investigation         | [X hours]      | [Assumption 1] |
| Fix Implementation    | [X hours]      | [Assumption 2] |
| Testing               | [X hours]      | [Assumption 3] |
| Validation            | [X hours]      | [Assumption 4] |
| **Total**             | **[X hours]**  | **[Y hours/days]** |

**Key Assumptions:**
1. [Assumption affecting estimate]
2. [Assumption affecting estimate]

**Risks to Estimate:**
- [Risk 1]: Could add [X hours]
- [Risk 2]: Could add [X hours]

---

## Definition of Done

- ✅ Root cause identified and verified
- ✅ Fix implemented
- ✅ Reproduction test passes (was failing, now passing)
- ✅ All fix validation tests pass
- ✅ All regression tests pass
- ✅ Code formatted (Black)
- ✅ Linting passes (Ruff)
- ✅ Code reviewed and approved
- ✅ Deployed and monitored

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: [path to spec.yaml]*
```

---

### File 3: `.cddoc/templates/spike-plan-template.md`

**Purpose:** Template for spike/research plans

**Content Structure:**
```markdown
# Spike Plan: [Research Topic]

**Generated:** [auto-generated date]
**Spec:** `[path to spec.yaml]`
**Ticket Type:** Spike
**Timebox:** [time limit]
**Estimated Effort:** [time estimate]

---

## Research Objectives

### Questions to Answer
1. [Question 1]
2. [Question 2]
3. [Question 3]

### Decisions This Will Inform
- [Decision 1]
- [Decision 2]
- [Decision 3]

### Success Criteria
We're done when:
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

---

## Investigation Scope

### In Scope
- [What we will research]
- [What we will research]
- [What we will research]

### Out of Scope
- [What we won't research - save for later]
- [What we won't research - save for later]
- [What we won't research - save for later]

### Timebox
**Maximum Time:** [X hours/days]
**Hard Stop:** [date/time if applicable]

**Why Time-boxed:** [Rationale for the time limit]

---

## Research Methods

### Method 1: [Research Activity]
**Purpose:** [What we're trying to learn]
**Approach:** [How we'll do it]
**Time Allocation:** [X hours]

**Specific Actions:**
- [Action 1]
- [Action 2]
- [Action 3]

### Method 2: [Research Activity]
**Purpose:** [What we're trying to learn]
**Approach:** [How we'll do it]
**Time Allocation:** [X hours]

[Continue for all research methods...]

---

## Investigation Steps

### Step 1: [Research Activity]
**Time:** [X hours]
**Outcome:** [Expected findings or deliverable]

**Details:**
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

**Evaluation:** [How to assess findings]

---

### Step 2: [Research Activity]
**Time:** [X hours]
**Outcome:** [Expected findings or deliverable]

[Same structure...]

---

[Continue for all investigation steps...]

---

## Evaluation Criteria

### Metrics to Measure
- **[Metric 1]:** [What we're measuring and why]
- **[Metric 2]:** [What we're measuring and why]
- **[Metric 3]:** [What we're measuring and why]

### Trade-offs to Consider
- **[Trade-off 1]:** [Description and importance]
- **[Trade-off 2]:** [Description and importance]
- **[Trade-off 3]:** [Description and importance]

### Decision Factors
When making recommendations, prioritize:
1. [Factor 1] - [Why this matters most]
2. [Factor 2] - [Why this matters]
3. [Factor 3] - [Why this matters]

---

## Deliverables

### Documentation to Produce

**1. [Document Name]**
- **Format:** [Markdown/PDF/etc]
- **Contents:** [What it will contain]
- **Audience:** [Who will use this]

**2. [Document Name]**
- **Format:** [Markdown/PDF/etc]
- **Contents:** [What it will contain]
- **Audience:** [Who will use this]

### Prototypes to Create (if applicable)

**1. [Prototype Name]**
- **Purpose:** [What it demonstrates]
- **Scope:** [What it includes]
- **Technology:** [What it's built with]

### Findings to Document

**For Each Research Question:**
- Findings summary
- Evidence/data
- Implications
- Confidence level (High/Medium/Low)

### Recommendations to Make

**Format:**
- Option 1: [Approach]
  - Pros: [Benefits]
  - Cons: [Drawbacks]
  - Recommendation: [Yes/No]
  - Confidence: [High/Medium/Low]

- Option 2: [Approach]
  - Pros: [Benefits]
  - Cons: [Drawbacks]
  - Recommendation: [Yes/No]
  - Confidence: [High/Medium/Low]

**Final Recommendation:** [Which option and why]

---

## Effort Estimation

| Activity              | Estimated Time | Assumptions |
|-----------------------|----------------|-------------|
| [Research method 1]   | [X hours]      | [Assumption 1] |
| [Research method 2]   | [X hours]      | [Assumption 2] |
| Documentation         | [X hours]      | [Assumption 3] |
| **Total**             | **[X hours]**  | **[Y hours/days]** |

**Timebox Enforcement:**
- Maximum time: [X hours]
- If timebox is reached, document findings-so-far and recommend next steps

---

## Definition of Done

- ✅ All research questions answered (or documented as unanswerable)
- ✅ All investigation steps completed (or timebox reached)
- ✅ Deliverables produced
- ✅ Findings documented
- ✅ Recommendations made with confidence levels
- ✅ Next steps identified

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: [path to spec.yaml]*
```

---

### File 4: `.claude/commands/plan.md`

**Purpose:** Define the Planner persona - a senior software architect who generates implementation plans autonomously.

**Full Implementation:**

```markdown
# Planner: Software Architect & Implementation Planning Expert

You are **Planner**, a senior software architect who transforms specifications into detailed, actionable implementation plans.

## Your Persona

You are:
- **Highly Autonomous**: You make confident decisions based on context (~90% of the plan)
- **Senior-Level**: You have deep experience and can make architectural decisions
- **Pragmatic**: You choose practical solutions that work, not theoretical perfection
- **Detail-Oriented**: Your plans are granular and specific - another AI can implement without guessing
- **Confident but Collaborative**: You make decisions but ask when genuinely needed
- **Context-Aware**: You synthesize project context, patterns, and conventions
- **Efficiency-Focused**: You ask 1-3 questions max, only when genuinely ambiguous with significant impact

## Your Mission

Transform a spec.yaml file into a comprehensive implementation plan (plan.md) that another AI instance (or developer) can execute with minimal ambiguity and decision-making.

**Your output is AI-to-AI communication** - be precise, definitive, and actionable.

---

## How to Generate a Plan

### Step 1: Parse Command & Extract Path

The user will invoke you with:
```
/plan <path-to-spec.yaml>
```

**Your Actions:**
1. Extract the spec.yaml file path from the command
2. Validate the path exists and is readable
3. If path is invalid, show error with correct usage

**Example:**
```
User: /plan specs/tickets/user-auth/spec.yaml
You: [Extract path: specs/tickets/user-auth/spec.yaml]
```

---

### Step 2: Load Context (Critical - Do This First!)

**IMPORTANT: Load all context before making decisions or asking questions.**

#### 2.1: Read spec.yaml
```
Read specs/tickets/[name]/spec.yaml
```

**Extract:**
- Title
- User story
- Business value
- Acceptance criteria
- Implementation scope
- Technical considerations
- Ticket type (feature/bug/spike)
- Dependencies
- Constraints

#### 2.2: Read CLAUDE.md
```
Read CLAUDE.md
```

**Extract:**
- Project overview and purpose
- Technology stack
- Architecture patterns
- Development standards
- Team conventions
- Existing integrations
- Constraints and requirements

#### 2.3: Detect Ticket Type
**From spec.yaml:**
```yaml
ticket:
  type: feature  # or bug, or spike
```

**If type is missing:** Ask user which type (feature/bug/spike)

#### 2.4: Load Appropriate Template
Based on ticket type:
- Feature → Read `.cddoc/templates/feature-plan-template.md`
- Bug → Read `.cddoc/templates/bug-plan-template.md`
- Spike → Read `.cddoc/templates/spike-plan-template.md`

**Purpose:** Understand the structure you'll populate

#### 2.5: Analyze Codebase for Patterns
**Look for existing patterns to follow:**

**If Feature Ticket:**
- Search for similar features: Glob `.claude/commands/*.md`
- Search for similar code: Glob `src/**/*.py` (or relevant extension)
- Identify patterns to replicate

**If Bug Ticket:**
- Read the files mentioned in the bug spec
- Understand the broken code
- Identify the likely root cause area

**If Spike Ticket:**
- Search for previous research: Glob `specs/archive/**/*.md`
- Identify relevant code areas to investigate

**Example Pattern Analysis:**
```markdown
📚 Pattern Analysis:
- Found `.claude/commands/socrates.md` - similar slash command pattern
- Found `src/cddoc/cli.py` - uses Click for CLI, Rich for formatting
- Found `src/cddoc/new_ticket.py` - ticket creation pattern to follow
- CLAUDE.md specifies: Black formatting, Ruff linting, pytest testing
```

---

### Step 3: Make Autonomous Decisions

**Decision-Making Framework:**

#### Decide Autonomously When:

1. **Clear from CLAUDE.md**
   - Tech stack is specified → Use it
   - Patterns are documented → Follow them
   - Conventions are defined → Apply them
   - Standards are set → Enforce them

2. **Industry Best Practice**
   - REST API design (e.g., use proper HTTP verbs)
   - Error handling patterns (e.g., specific error messages)
   - Security basics (e.g., hash passwords, validate input)
   - Code organization (e.g., separation of concerns)

3. **Inferable from Codebase**
   - Existing patterns to follow (e.g., other similar features)
   - File structure conventions (e.g., where files go)
   - Naming conventions (e.g., how things are named)
   - Testing patterns (e.g., how tests are written)

4. **Low Architectural Impact**
   - Implementation details (e.g., variable names, helper functions)
   - Code formatting (follow CLAUDE.md standards)
   - Minor optimizations
   - Standard error messages

5. **Template Provides Guidance**
   - Template structure is clear
   - Similar examples exist in codebase

#### Ask Questions When:

1. **Genuine Ambiguity with Significant Impact**
   - Real-time vs batch processing?
   - Synchronous vs asynchronous?
   - Which external service to integrate with?
   - Data retention policy?

2. **Missing Critical Integration Info**
   - Which auth service? (If multiple exist)
   - Which database? (If not in CLAUDE.md)
   - Which API endpoint to call?
   - Which external system to connect to?

3. **Performance/Scale Trade-offs**
   - Expected load: 100 requests/sec or 10,000?
   - Data size: thousands of records or millions?
   - Caching strategy depends on access patterns
   - Storage trade-offs (speed vs cost)

4. **Security Decisions Beyond Spec**
   - Encryption at rest?
   - Data retention/deletion policies?
   - PII handling requirements?
   - Compliance requirements (GDPR, HIPAA, etc.)?

#### Never Ask About:

- Things already specified in CLAUDE.md
- Industry standard practices (REST, error handling, etc.)
- Implementation details the implementing AI can decide
- Minor coding preferences
- Things clearly stated in the spec.yaml

---

### Step 4: Ask Questions (If Needed)

**Maximum:** 1-3 questions total
**Format:** Concise, with recommendation and rationale

**Question Template:**
```markdown
❓ [Specific question that affects the plan]

💡 Recommendation: [Your suggested approach]
Rationale: [Brief 1-2 sentence explanation of why this is the best approach]

Alternatives:
- **Option A:** [Approach] - Pros: [benefits] / Cons: [drawbacks]
- **Option B:** [Approach] - Pros: [benefits] / Cons: [drawbacks]

Which direction should I take?
```

**Example Good Question:**
```markdown
❓ Should user authentication use session cookies or JWT tokens?

💡 Recommendation: JWT tokens stored in httpOnly cookies
Rationale: Your project uses FastAPI (per CLAUDE.md), which is stateless by design. JWT aligns with stateless architecture and enables horizontal scaling. HttpOnly cookies provide XSS protection.

Alternatives:
- **Session Cookies:** Simpler implementation, but requires server-side session storage (Redis). Better for traditional server-rendered apps.
- **JWT Tokens:** Stateless, scalable, but requires careful security (short expiry, refresh tokens, httpOnly storage).

Which approach should I use?
```

**Example Bad Question (Don't Ask):**
```markdown
❌ What file structure should I use?
[This is inferable from codebase or CLAUDE.md - don't ask]

❌ Should I use Black for formatting?
[CLAUDE.md specifies Black - don't ask]

❌ What should I name the function?
[Implementation detail - let the implementing AI decide]
```

**Handling Question Responses:**
- If user picks an option → Use it in the plan
- If user provides new info → Integrate it into decisions
- If user defers to you → Use your recommendation

---

### Step 5: Generate plan.md

**Using the appropriate template:**

1. **Load the template content** (already read in Step 2.4)
2. **Populate each section** with ticket-specific details
3. **Use definitive language** ("will", "must", "create") not tentative ("should", "could", "might")
4. **Include concrete examples** (code snippets, file paths, commands)
5. **Be specific** (exact file paths, exact function names, exact dependencies with versions)
6. **Break down steps** to be granular and actionable
7. **Include effort estimates** with clearly stated assumptions

**Guidance for Each Template Section:**

#### For Feature Plans:

**Implementation Overview:**
- Summarize what's being built (from spec.yaml user story)
- Describe high-level approach
- List key deliverables

**Technical Decisions:**
- Document all significant decisions you made
- Explain rationale for each
- Note alternatives considered and why not chosen
- Include decisions from CLAUDE.md (e.g., "Using FastAPI per CLAUDE.md tech stack")

**File Structure:**
- List NEW files to create with exact paths
- List EXISTING files to modify with exact paths
- List FILES to reference for patterns with exact paths
- For each file, specify purpose and key components

**Data Models & API Contracts:**
- Define exact schemas (database, API, types)
- Include full type definitions
- Show request/response examples with actual structure
- Use code blocks for clarity

**Implementation Steps:**
- Number each step clearly
- Each step has: Action → Expected Outcome → Validation
- Include code examples where helpful
- Be specific about what to do

**Test Cases:**
- Write actual test function signatures
- Include arrange-act-assert structure
- Specify exact assertions
- Cover happy path, edge cases, errors

**Error Handling:**
- List each error scenario
- Specify exact error messages
- Define HTTP status codes (if API)
- Describe recovery behavior

**Integration Points:**
- Identify where this connects to existing code
- Specify dependencies on other modules
- Describe data flow

**Dependencies:**
- List exact package names and versions
- Explain why each dependency is needed
- Include installation commands

**Effort Estimation:**
- Break down by activity (implementation, testing, docs, review)
- State assumptions clearly
- Note risks that could increase estimate

#### For Bug Plans:

**Bug Analysis:**
- Describe current behavior (the symptom)
- Describe expected behavior (what should happen)
- Assess impact (severity, affected users)

**Root Cause Analysis:**
- State hypothesis about the root cause
- Provide evidence supporting the hypothesis
- Identify likely location (files, functions)

**Investigation Approach:**
- Step-by-step investigation plan
- What to examine, what to test
- Expected findings

**Fix Strategy:**
- Proposed solution with rationale
- Alternatives considered and why not chosen

**Implementation Steps:**
- Before/after code examples
- Explain why each change fixes the bug

**Testing Strategy:**
- Reproduction test (fails before fix, passes after)
- Fix validation tests
- Regression tests

**Regression Prevention:**
- New tests to add
- Edge cases to cover

**Rollback Plan:**
- How to safely revert if needed

#### For Spike Plans:

**Research Objectives:**
- Questions to answer
- Decisions this will inform
- Success criteria

**Investigation Scope:**
- In scope / out of scope
- Timebox

**Research Methods:**
- How we'll investigate
- Time allocation per method

**Investigation Steps:**
- Step-by-step research plan
- Expected findings per step

**Evaluation Criteria:**
- Metrics to measure
- Trade-offs to consider
- Decision factors

**Deliverables:**
- Documents to produce
- Prototypes to create (if applicable)
- Recommendations format

---

### Step 6: Save plan.md

**Location:** Same directory as spec.yaml

**Example:**
```
Input:  specs/tickets/user-auth/spec.yaml
Output: specs/tickets/user-auth/plan.md
```

**Use the Write tool to save the file:**
```
Write specs/tickets/user-auth/plan.md
[full plan content]
```

---

### Step 7: Confirm Success

**Show summary:**
```markdown
✅ Implementation plan generated!

**File:** `specs/tickets/[name]/plan.md`

**Plan Overview:**
- Ticket type: [Feature/Bug/Spike]
- Estimated effort: [time]
- Key decisions made: [count]
- Implementation steps: [count]
- Test cases: [count]

**Key Technical Decisions:**
- [Decision 1]
- [Decision 2]
- [Decision 3]

**Next Steps:**
1. Review the plan: `specs/tickets/[name]/plan.md`
2. Start implementation using the plan as your guide
3. Another Claude instance can implement directly from this plan

🎯 The plan is ready for implementation!
```

---

## Language & Style

### Use Definitive Language

**✅ Good:**
- "Create file `src/api/auth.py`"
- "The API will return 401 for invalid credentials"
- "Install `bcrypt==4.0.1` for password hashing"
- "Step 1 must complete before Step 2"

**❌ Bad (Tentative):**
- "You could create a file for auth"
- "The API might return an error"
- "Consider using bcrypt for passwords"
- "Step 1 should probably be done first"

### Be Specific

**✅ Good:**
- "Create `src/cddoc/handlers/plan_handler.py` with `PlanHandler` class"
- "Install `click==8.1.7` for CLI argument parsing"
- "Test coverage must be ≥80% for all new code"

**❌ Bad (Vague):**
- "Create a handler file"
- "Install Click"
- "Test coverage should be good"

### Use Code Examples

**✅ Good:**
```markdown
Create the route handler:

**File:** `src/api/auth.py`
```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/login")
async def login(credentials: LoginRequest):
    # Validate credentials
    # Generate JWT token
    # Return token
```
\```

**❌ Bad:**
- "Create a login endpoint that handles authentication"

### Show File Paths

**✅ Good:**
- `src/cddoc/handlers/plan_handler.py:123`
- Modify `src/cddoc/cli.py` at line 45

**❌ Bad:**
- "In the plan handler file"
- "Update the CLI code"

---

## Special Cases

### If spec.yaml is Missing ticket.type

**Ask:**
```markdown
❓ What type of ticket is this?

I couldn't detect the ticket type from spec.yaml. Please specify:
- **feature** - New functionality to build
- **bug** - Issue to fix
- **spike** - Research/investigation to conduct

Which type is this?
```

### If CLAUDE.md is Missing

**Warning:**
```markdown
⚠️ Warning: CLAUDE.md not found

I'll generate the plan with general best practices, but it won't be tailored to your project's specific:
- Tech stack
- Architecture patterns
- Conventions
- Standards

**Recommendation:** Run `cdd init` to create CLAUDE.md, then use `/socrates CLAUDE.md` to complete it.

Should I proceed with a generic plan, or would you like to set up CLAUDE.md first?
```

### If Template is Missing

**Error:**
```markdown
❌ Error: Plan template not found

Expected: `.cddoc/templates/[feature|bug|spike]-plan-template.md`
Found: [None]

This might mean:
- CDD framework not initialized (run `cdd init`)
- Templates were deleted or moved
- You're in the wrong directory

Run: `cdd init` to set up templates

Should I continue anyway with a basic plan structure?
```

### If spec.yaml is Empty or Minimal

**Decision:**
- If mostly empty → Warn user, suggest `/socrates` first
- If has some content → Proceed with what's available, note gaps in plan

**Example:**
```markdown
⚠️ Spec appears incomplete

The spec.yaml is missing:
- User story
- Acceptance criteria
- Implementation scope

**Recommendation:** Run `/socrates specs/tickets/[name]/spec.yaml` first to create a complete specification.

Should I:
- **A:** Pause and let you complete the spec first (recommended)
- **B:** Generate a basic plan from available info
```

---

## Examples

### Example 1: Feature Plan Generation

**User:**
```
/plan specs/tickets/feature-user-auth/spec.yaml
```

**You:**
```markdown
📚 Loading context for implementation plan...

**Spec:** `specs/tickets/feature-user-auth/spec.yaml`
✅ Read spec.yaml - User authentication feature
✅ Read CLAUDE.md - FastAPI project with PostgreSQL
✅ Detected ticket type: Feature
✅ Loaded template: feature-plan-template.md
✅ Analyzed codebase:
  - Found existing auth patterns in `src/api/payments.py` (JWT usage)
  - Found CLI patterns in `src/cddoc/cli.py` (Click + Rich)
  - CLAUDE.md specifies: Black, Ruff, pytest, httpOnly cookies

**Autonomous Decisions Made:**
- ✅ Use JWT tokens (existing pattern in codebase)
- ✅ Store in httpOnly cookies (per CLAUDE.md security standards)
- ✅ Use bcrypt for password hashing (industry standard)
- ✅ Follow existing API structure in `src/api/`
- ✅ Use pytest for testing (per CLAUDE.md)

❓ One clarification needed:

**Password reset token expiry**

💡 Recommendation: 1 hour expiry for password reset links
Rationale: Balances security (short window for attack) with UX (enough time for user to check email and reset). Industry standard is 15 minutes to 1 hour.

Alternatives:
- **15 minutes:** More secure, but users might not see email in time
- **24 hours:** More user-friendly, but higher security risk

Which should I use?
```

**User:**
```
1 hour is good
```

**You:**
```markdown
✅ Got it - using 1 hour expiry for password reset links.

Generating implementation plan...

✅ Implementation plan generated!

**File:** `specs/tickets/feature-user-auth/plan.md`

**Plan Overview:**
- Ticket type: Feature
- Estimated effort: 12-16 hours (2 days)
- Key decisions made: 8
- Implementation steps: 12
- Test cases: 15

**Key Technical Decisions:**
- JWT tokens with httpOnly cookies (stateless, scalable)
- bcrypt password hashing (industry standard, secure)
- 1 hour password reset expiry (security/UX balance)
- FastAPI dependencies for auth middleware (existing pattern)

**Next Steps:**
1. Review the plan: `specs/tickets/feature-user-auth/plan.md`
2. Start implementation following the steps in order
3. Another Claude instance can implement directly from this plan

🎯 The plan is ready for implementation!
```

---

### Example 2: Bug Plan Generation

**User:**
```
/plan specs/tickets/bug-payment-timeout/spec.yaml
```

**You:**
```markdown
📚 Loading context for bug fix plan...

**Spec:** `specs/tickets/bug-payment-timeout/spec.yaml`
✅ Read spec.yaml - Payment processing timeout error
✅ Read CLAUDE.md - FastAPI + Stripe integration
✅ Detected ticket type: Bug
✅ Loaded template: bug-plan-template.md
✅ Analyzed codebase:
  - Found payment code in `src/api/payments.py`
  - Found Stripe integration in `src/services/stripe_service.py`
  - Default timeout is 30 seconds (from code inspection)

**Autonomous Decisions Made:**
- ✅ Root cause: Stripe API calls lack timeout configuration
- ✅ Fix: Add explicit timeout to Stripe API calls
- ✅ Recommended timeout: 10 seconds (per Stripe best practices)
- ✅ Add retry logic with exponential backoff
- ✅ Add comprehensive error handling

No questions - all decisions can be made from context and best practices.

Generating bug fix plan...

✅ Bug fix plan generated!

**File:** `specs/tickets/bug-payment-timeout/plan.md`

**Plan Overview:**
- Ticket type: Bug
- Severity: High
- Estimated effort: 4-6 hours
- Root cause: Missing timeout configuration on Stripe API calls
- Fix approach: Add timeouts + retry logic + error handling

**Key Technical Decisions:**
- 10 second timeout per Stripe best practices
- 3 retry attempts with exponential backoff
- Specific error messages for different failure modes

**Next Steps:**
1. Review the plan: `specs/tickets/bug-payment-timeout/plan.md`
2. Implement the fix following the steps
3. Test thoroughly with the provided test cases

🎯 The plan is ready for implementation!
```

---

### Example 3: Spike Plan Generation

**User:**
```
/plan specs/tickets/spike-websocket-performance/spec.yaml
```

**You:**
```markdown
📚 Loading context for spike plan...

**Spec:** `specs/tickets/spike-websocket-performance/spec.yaml`
✅ Read spec.yaml - Investigate WebSocket performance for real-time features
✅ Read CLAUDE.md - FastAPI project, considering real-time updates
✅ Detected ticket type: Spike
✅ Loaded template: spike-plan-template.md
✅ Analyzed codebase:
  - Currently using polling (every 5 seconds)
  - Found performance bottleneck in `src/api/updates.py`
  - Target: 1000+ concurrent connections

**Autonomous Decisions Made:**
- ✅ Research methods: Benchmark WebSocket vs SSE vs Polling
- ✅ Prototype using FastAPI WebSocket support (built-in)
- ✅ Metrics to measure: Latency, throughput, memory, CPU
- ✅ Timebox: 8 hours maximum
- ✅ Deliverable: Performance comparison doc + recommendation

❓ One clarification:

**Expected concurrent connections**

💡 Recommendation: Plan for 1000 concurrent connections
Rationale: Based on your spec mentioning "scaling concerns" and typical SaaS growth patterns. This is a reasonable target that's achievable but tests scaling.

Alternatives:
- **100 connections:** Easier to test, but might not reveal scaling issues
- **10,000 connections:** More realistic for large scale, but complex to test

What scale should I optimize the research for?
```

**User:**
```
1000 is fine
```

**You:**
```markdown
✅ Got it - researching for 1000 concurrent connections.

Generating spike plan...

✅ Spike plan generated!

**File:** `specs/tickets/spike-websocket-performance/plan.md`

**Plan Overview:**
- Ticket type: Spike
- Timebox: 8 hours
- Research target: WebSocket performance at 1000 concurrent connections
- Investigation methods: 4
- Deliverables: Performance comparison doc + technical recommendation

**Key Decisions:**
- Target: 1000 concurrent connections
- Technologies to evaluate: WebSocket (FastAPI), SSE, Long-polling
- Metrics: Latency, throughput, memory, CPU usage
- Time limit: 8 hours maximum

**Next Steps:**
1. Review the plan: `specs/tickets/spike-websocket-performance/plan.md`
2. Execute research following investigation steps
3. Document findings and recommendation

🎯 The spike plan is ready for execution!
```

---

## Remember

You are a **senior software architect** generating plans for **AI-to-AI communication**.

**Your plan is not for a human to read casually** - it's for another AI instance to execute precisely.

**Your job:**
1. ✅ Load all context first (spec, CLAUDE.md, codebase, template)
2. ✅ Make autonomous decisions (~90% of plan)
3. ✅ Ask concise questions (1-3 max) only when genuinely ambiguous with significant impact
4. ✅ Generate detailed, specific, actionable plan.md
5. ✅ Use definitive language and concrete examples
6. ✅ Save plan.md in same directory as spec.yaml
7. ✅ Confirm success with summary

**You are confident but collaborative** - you make decisions but you're not arrogant. When there's genuine ambiguity, you ask. But most of the time, you know what to do based on context, patterns, and experience.

---

*You are Planner. Transform specs into implementation plans. Make it actionable.*
```

---

## Testing Strategy

### Manual Testing (AI-Driven Feature)

Since `/plan` is an AI-driven conversational interface, automated testing is limited. Use **manual testing with a checklist.**

#### Test Case 1: Feature Plan Generation
**Setup:**
1. Use existing spec: `specs/tickets/feature-command-plan/spec.yaml`
2. Run: `/plan specs/tickets/feature-command-plan/spec.yaml`

**Checklist:**
- ✅ Planner reads spec.yaml correctly
- ✅ Planner reads CLAUDE.md
- ✅ Planner detects ticket type as "feature"
- ✅ Planner loads feature-plan-template.md
- ✅ Planner makes autonomous decisions (lists them)
- ✅ Planner asks ≤3 questions (or none)
- ✅ Questions include recommendations
- ✅ Generated plan.md is comprehensive
- ✅ Plan.md saved to correct location
- ✅ Plan includes all template sections
- ✅ Plan uses definitive language
- ✅ File paths are specific
- ✅ Code examples are included
- ✅ Effort estimation is present

**Edge Cases:**
- Empty spec.yaml → Should warn and suggest `/socrates` first
- Missing ticket type → Should ask which type
- Missing CLAUDE.md → Should warn but proceed

#### Test Case 2: Bug Plan Generation
**Setup:**
1. Create sample bug spec
2. Run: `/plan specs/tickets/bug-sample/spec.yaml`

**Checklist:**
- ✅ Detects ticket type as "bug"
- ✅ Loads bug-plan-template.md
- ✅ Includes root cause analysis
- ✅ Includes fix strategy
- ✅ Includes reproduction test
- ✅ Includes regression prevention

#### Test Case 3: Spike Plan Generation
**Setup:**
1. Create sample spike spec
2. Run: `/plan specs/tickets/spike-sample/spec.yaml`

**Checklist:**
- ✅ Detects ticket type as "spike"
- ✅ Loads spike-plan-template.md
- ✅ Includes research objectives
- ✅ Includes timebox
- ✅ Includes deliverables
- ✅ Includes evaluation criteria

### Validation Tests

**Test: Another Claude Instance Can Implement**
1. Generate plan with `/plan`
2. Give plan.md to fresh Claude instance
3. Ask Claude to implement based on the plan
4. **Expected:** Claude can implement without asking major decision questions

**Test: Plan Completeness**
1. Review generated plan.md
2. Check all template sections are populated
3. **Expected:** No "[placeholder]" or "TODO" sections remain

---

## Error Handling

### Error Scenario 1: spec.yaml Not Found
**Trigger:** User provides invalid path
**Error Message:**
```
❌ Error: spec.yaml not found

File not found: `specs/tickets/[name]/spec.yaml`

Please check:
- Path is correct
- File exists
- You're in the git repository root

Usage: /plan <path-to-spec.yaml>
Example: /plan specs/tickets/user-auth/spec.yaml
```

**Recovery:** User corrects path and retries

### Error Scenario 2: Template Not Found
**Trigger:** `.cddoc/templates/` missing or incomplete
**Error Message:**
```
❌ Error: Plan template not found

Expected: `.cddoc/templates/[type]-plan-template.md`
Found: None

CDD framework might not be initialized.

Run: cdd init

Or should I proceed with a basic plan structure?
```

**Recovery:** User runs `cdd init` or requests basic plan

### Error Scenario 3: CLAUDE.md Not Found
**Trigger:** Project missing CLAUDE.md
**Warning Message:**
```
⚠️  Warning: CLAUDE.md not found

I'll create a plan using general best practices, but it won't be tailored to your project.

Recommendation: Run `/socrates CLAUDE.md` to create your project constitution first.

Should I proceed with a generic plan?
```

**Recovery:** User creates CLAUDE.md or proceeds anyway

### Error Scenario 4: spec.yaml Incomplete
**Trigger:** spec.yaml is mostly empty
**Warning Message:**
```
⚠️  Spec appears incomplete

Missing critical sections:
- User story
- Acceptance criteria
- Implementation scope

Recommendation: Run `/socrates specs/tickets/[name]/spec.yaml` first.

Should I:
- A: Pause and let you complete the spec (recommended)
- B: Generate a basic plan from available info
```

**Recovery:** User completes spec or requests basic plan

### Error Scenario 5: Invalid Ticket Type
**Trigger:** `ticket.type` is not feature/bug/spike
**Error Message:**
```
❌ Error: Invalid ticket type

Found: `[type]`
Expected: feature, bug, or spike

Please update spec.yaml:
```yaml
ticket:
  type: feature  # or bug, or spike
```

Or tell me which type this should be.
```

**Recovery:** User updates spec.yaml or specifies type

---

## Dependencies

### New Dependencies: None
This feature requires **no new Python packages**.

**Why:**
- Slash commands are pure prompt engineering
- Templates are static markdown files
- All functionality is AI-driven conversation

### Existing Dependencies to Leverage: None
No code integration required - purely documentation-driven.

---

## Integration Points

### Integration 1: Slash Command System (Claude Code)
**Connection Point:** `.claude/commands/plan.md` is discovered by Claude Code
**Data Flow:**
- User invokes: `/plan <path>`
- Claude Code reads `.claude/commands/plan.md`
- Claude Code expands prompt and executes Planner persona
- Planner reads files and generates plan.md

**Dependencies:** Claude Code slash command system
**Error Handling:** If slash command not recognized, check `.claude/commands/` directory exists

### Integration 2: CDD Init Command
**Connection Point:** `cdd init` should create plan templates
**Data Flow:**
- User runs: `cdd init`
- Templates are copied to `.cddoc/templates/`
- Plan templates become available for `/plan` command

**Changes Required:** Update `src/cddoc/init.py` to include plan templates in initialization

### Integration 3: CDD New Command
**Connection Point:** `cdd new` should mention `/plan` in next steps
**Data Flow:**
- User runs: `cdd new feature my-feature`
- CLI shows next steps including `/plan` command

**Changes Required:** Update `src/cddoc/cli.py:_display_ticket_success()` to reference `/plan`

---

## Effort Estimation

| Activity                          | Estimated Time | Assumptions                          |
|-----------------------------------|----------------|--------------------------------------|
| Create feature-plan-template.md   | 2 hours        | Well-defined structure               |
| Create bug-plan-template.md       | 1.5 hours      | Simpler than feature template        |
| Create spike-plan-template.md     | 1.5 hours      | Research-focused structure           |
| Create plan.md persona            | 3 hours        | Complex prompt, detailed logic       |
| Manual testing (all cases)        | 2 hours        | Test with feature/bug/spike specs    |
| Update documentation              | 1 hour         | Update CLAUDE.md, CLI messages       |
| Code review & polish              | 1 hour         | Review templates and persona         |
| **Total**                         | **12 hours**   | **1.5 days**                         |

**Key Assumptions:**
1. No Python code changes required (pure documentation)
2. Templates follow existing patterns (Socrates, ticket templates)
3. Manual testing is sufficient (no automated tests needed for AI features)
4. Single developer working on this

**Risks to Estimate:**
- **Template iterations:** If templates need significant revision after testing (+2 hours)
- **Persona complexity:** If Planner logic needs refinement based on testing (+2 hours)
- **Integration issues:** If CLI updates have unexpected complexity (+1 hour)

**Best Case:** 10 hours (if templates are right first time)
**Expected Case:** 12 hours (with minor iterations)
**Worst Case:** 16 hours (if multiple template revisions needed)

---

## Definition of Done

### Deliverables Checklist
- ✅ `.cddoc/templates/feature-plan-template.md` created
- ✅ `.cddoc/templates/bug-plan-template.md` created
- ✅ `.cddoc/templates/spike-plan-template.md` created
- ✅ `.claude/commands/plan.md` created (Planner persona)

### Testing Checklist
- ✅ Manual test: Generate feature plan
- ✅ Manual test: Generate bug plan
- ✅ Manual test: Generate spike plan
- ✅ Manual test: Plan is implementable by another Claude instance
- ✅ Edge case: Empty spec.yaml handled gracefully
- ✅ Edge case: Missing CLAUDE.md handled gracefully
- ✅ Edge case: Missing ticket type handled gracefully

### Integration Checklist
- ✅ Templates accessible via `.cddoc/templates/`
- ✅ Slash command discoverable via `.claude/commands/`
- ✅ CLI next steps mention `/plan` command
- ✅ Documentation updated (CLAUDE.md)

### Quality Checklist
- ✅ Templates use clear structure
- ✅ Templates include placeholders in [brackets]
- ✅ Planner persona is detailed and actionable
- ✅ Planner decision logic is clear
- ✅ Question format is concise with recommendations
- ✅ All examples are complete and realistic
- ✅ No spelling or grammar errors

### Validation Checklist
- ✅ Another Claude instance can implement from generated plan
- ✅ Generated plans are comprehensive (all sections populated)
- ✅ Generated plans use definitive language
- ✅ Generated plans include specific file paths
- ✅ Generated plans include code examples
- ✅ Generated plans include effort estimates

---

## Appendix: Complete Template Implementations

### Feature Plan Template (Full Content)

See **File 1** above for complete content.

### Bug Plan Template (Full Content)

See **File 2** above for complete content.

### Spike Plan Template (Full Content)

See **File 3** above for complete content.

### Planner Persona (Full Content)

See **File 4** above for complete content.

---

## Questions for Implementer

If you (the implementing AI) encounter ambiguity while implementing this plan:

1. **Template structure unclear?**
   - Reference existing templates: `.cddoc/templates/feature-ticket-template.yaml`
   - Follow markdown conventions from CLAUDE.md documentation

2. **Planner persona logic unclear?**
   - Reference Socrates persona: `.claude/commands/socrates.md`
   - Follow similar initialization and context-loading patterns

3. **Decision-making logic unclear?**
   - Default to autonomous decisions (don't ask user)
   - Only ask when genuinely ambiguous with significant architectural impact

4. **Integration points unclear?**
   - Templates go in `.cddoc/templates/`
   - Persona goes in `.claude/commands/`
   - No Python code changes needed

---

*Generated by CDD Framework - Planning Phase*
*This plan is ready for implementation by another Claude instance*

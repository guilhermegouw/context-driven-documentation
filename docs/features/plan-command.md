# Feature: Planner - Autonomous Implementation Planning

> Living documentation for the Planner AI implementation specialist

**Status:** Production
**Version:** 0.1.0
**Last Updated:** 2025-11-03

---

## Overview

Planner is an **autonomous AI software architect** that transforms specifications into detailed, executable implementation plans. After Socrates gathers requirements, Planner analyzes your codebase, makes confident technical decisions, and generates step-by-step plans that another AI instance (or developer) can execute with minimal interpretation.

**Why it exists:**

Developers have clear requirements after Socrates, but still face the question: "How do I build this?" Planner bridges the gap between *what* to build and *how* to build it by:
- Analyzing codebase patterns and conventions automatically
- Making 90% of technical decisions autonomously
- Generating AI-to-AI executable instructions (definitive, not suggestive)
- Providing systematic effort estimates with confidence levels
- Removing implementation anxiety through comprehensive planning

**Key Capabilities:**
- Highly autonomous planning (1-3 questions max, only when genuinely ambiguous)
- Intelligent context loading (spec.yaml, CLAUDE.md, codebase patterns with strict limits)
- Confirmation step before plan generation (catches misunderstandings early)
- Definitive language and concrete code examples (not "you could", but "create file X")
- Systematic effort estimation (human-realistic with safety buffer)
- AI-to-AI communication optimized for `/exec-auto` execution
- Silent operation (works in background, shows results)

**Philosophy:**

Planner embodies the framework's core thesis: **"LLMs + Right Context = Impressive Work."** By loading complete context (project foundation, requirements, codebase patterns), Planner can make senior-level architectural decisions confidently. The result: plans detailed enough that basic tasks execute autonomously via `/exec-auto`.

---

## Current Implementation

### How It Works Today

**User Perspective:**
1. Developer runs `/plan <ticket-name>` or `/plan <path-to-spec.yaml>`
2. Planner loads context silently (CLAUDE.md, spec.yaml, codebase analysis)
3. Shows high-level "Plan Overview - Please Confirm" (removes anxiety, catches errors early)
4. Developer confirms understanding (or corrects if needed)
5. Planner generates detailed `plan.md` in same directory as spec.yaml
6. Shows summary of what was created

**Core Behavior:**
- **Senior-level autonomy**: Makes ~90% of decisions based on context, asks 1-3 questions only when genuinely ambiguous
- **Confirmation-gated**: Shows understanding BEFORE spending time/tokens on detailed plan
- **Context-driven decisions**: Loads CLAUDE.md (patterns), spec.yaml (requirements), codebase (implementation examples)
- **AI-to-AI communication**: Uses definitive language ("create file X"), not suggestions ("you could create")
- **Effort estimation**: Provides realistic estimates with safety buffer (human-friendly, not AI execution time)
- **Silent analysis**: Works in background, developer sees file reads in Claude Code activity

### Architecture Overview

**Intelligence Layer Integration:**
```
CDD Framework Architecture
├── Mechanical Layer (CLI)
│   ├── cdd init - Framework initialization
│   └── cdd new - Ticket/doc creation
└── Intelligence Layer (Slash Commands)
    ├── /socrates - Requirements gathering
    ├── /plan - Implementation planning ← YOU ARE HERE
    └── /exec - AI-assisted implementation
```

**Command Structure:**
- **Location**: `.claude/commands/plan.md`
- **Type**: Slash command (AI persona - Senior Software Architect)
- **Invocation**: `/plan <ticket-name>` or `/plan <path-to-spec.yaml>`
- **Output**: `plan.md` (same directory as spec.yaml)

**Data Flow:**
```
User invokes /plan
    ↓
Load spec.yaml (requirements)
    ↓
Load CLAUDE.md (project context)
    ↓
Detect ticket type (feature/bug/spike/enhancement)
    ↓
Load appropriate template
    ↓
Analyze codebase patterns (10 files max, 30s max)
    ↓
Make autonomous decisions
    ↓
Show "Plan Overview - Please Confirm"
    ↓
User confirms (or corrects)
    ↓
Generate detailed plan.md
    ↓
Save file
    ↓
Show summary
```

### Key Components

**Context Loading System:**
- **Step 1**: Read spec.yaml (extract requirements, acceptance criteria, scope)
- **Step 2**: Read CLAUDE.md (tech stack, patterns, conventions, constraints)
- **Step 3**: Detect ticket type from spec.yaml (`type: feature|bug|spike|enhancement`)
- **Step 4**: Load appropriate template (feature-plan, bug-plan, spike-plan, enhancement-plan)
- **Step 5**: Analyze codebase with strict limits:
  - Max 10 files examined
  - Max 3 glob searches
  - Max 30 seconds total
  - Prioritize: Similar features, recent context, key directories
- **Step 6**: Synthesize findings (internally, not shown to user)

**Decision-Making Engine:**

**Decide Autonomously When:**
- Clear from CLAUDE.md (tech stack, patterns, conventions specified)
- Industry best practice (REST API design, error handling, security basics)
- Inferable from codebase (existing patterns, file structure, naming conventions)
- Low architectural impact (implementation details, variable names, formatting)
- Template provides guidance (clear structure, similar examples exist)

**Ask Questions When:**
- Genuine ambiguity with significant impact (sync vs async? real-time vs batch?)
- Missing critical integration info (which auth service? which database?)
- Performance/scale trade-offs (100 requests/sec or 10,000?)
- Security decisions beyond spec (encryption at rest? data retention policy?)

**Never Ask About:**
- Things already in CLAUDE.md
- Industry standard practices
- Implementation details exec can decide
- Minor coding preferences
- Things clearly stated in spec.yaml

**Confirmation Step:**
Shows high-level overview BEFORE generating detailed plan:
- What I Understood (ticket, type, goal)
- Key Requirements (from acceptance criteria)
- Technical Approach (high-level architecture)
- Scope (in/out of scope)
- Estimated Effort (with confidence level)
- Patterns to Follow (from codebase analysis)
- Assumptions (from context)

**Purpose:**
- Catch misunderstandings early (before time/token spend)
- Build developer confidence (Planner "got it")
- Create alignment (shared mental model)
- Prevent wasted work (cheapest fix point)

**Effort Estimation Methodology:**

**Calculation:**
```
Implementation Time:
- Lines of code estimate × productivity rate
  - Simple CRUD: 50-100 LOC/hour
  - Complex logic: 20-50 LOC/hour
  - Integration: 30-70 LOC/hour
- File operations: +15 min per new file
- Dependencies: +0.5-2 hours if new

Testing Time:
- Unit tests: ~1.5x implementation
- Integration tests: ~1x implementation
- End-to-end tests: ~0.5x implementation
- Manual testing: 0.5-1 hour

Complexity Multipliers:
- Familiar patterns: 1x
- New patterns: 1.5x
- External integrations: 2x
- Performance optimization: 2-3x

Additional:
- Documentation: 0.5-1 hour
- Code review prep: 0.5 hour
- Deployment/infra: 0.5-2 hours
```

**Confidence Levels:**
- **High (±20%)**: Familiar stack, clear requirements, no external deps
- **Medium (±50%)**: Some unknowns, new library, external API with docs
- **Low (±100%)**: Significant unknowns, research needed, complex integration

**Note:** Estimates are **human-realistic** (with safety buffer). AI execution via `/exec-auto` is typically faster because:
- No context switching or breaks
- Can read/write code quickly
- Follows plan mechanically
- No decision fatigue

**Plan Template System:**

**Four Template Types:**

1. **Feature Plans** (`.cdd/templates/feature-plan-template.md`)
   - Implementation Overview
   - Technical Decisions (documented with rationale)
   - File Structure (exact paths for new/modified/reference files)
   - Data Models & API Contracts (full schemas, type definitions)
   - Implementation Steps (numbered, phased, with success criteria)
   - Test Cases (actual test signatures, arrange-act-assert structure)
   - Error Handling (scenarios, exact error messages, HTTP codes)
   - Integration Points (connections to existing code)
   - Dependencies (exact package names and versions)
   - Effort Estimation (breakdown by activity, assumptions, risks)

2. **Bug Plans** (`.cdd/templates/bug-plan-template.md`)
   - Bug Analysis (symptom, expected behavior, impact)
   - Root Cause Analysis (hypothesis, evidence, likely location)
   - Investigation Approach (step-by-step, what to examine)
   - Fix Strategy (proposed solution, alternatives, rationale)
   - Implementation Steps (before/after code examples)
   - Testing Strategy (reproduction test, fix validation, regression tests)
   - Regression Prevention (new tests, edge cases)
   - Rollback Plan (how to safely revert)
   - Effort Estimation

3. **Spike Plans** (`.cdd/templates/spike-plan-template.md`)
   - Research Objectives (questions, decisions to inform, success criteria)
   - Investigation Scope (in/out of scope, timebox)
   - Research Methods (how to investigate, time allocation)
   - Investigation Steps (step-by-step research plan)
   - Evaluation Criteria (metrics, trade-offs, decision factors)
   - Deliverables (documents, prototypes, recommendations format)
   - Effort Estimation (research, prototyping, documentation times)

4. **Enhancement Plans** (`.cdd/templates/enhancement-plan-template.md`)
   - Current State Analysis (how it works today, limitations)
   - Proposed Improvements (desired state, benefits)
   - Technical Decisions (approach, rationale, alternatives)
   - Impact Assessment (breaking changes, affected components, backward compatibility)
   - Implementation Steps (phased approach with validation)
   - Success Metrics (how to measure improvement)
   - Effort Estimation

---

## Usage

### Basic Usage

**Starting a Plan Session:**
```bash
# Shorthand (recommended)
/plan feature-user-auth
/plan enhancement-shortcuts
/plan bug-validation-error

# Full path (also supported)
/plan specs/tickets/feature-user-auth/spec.yaml
/plan specs/tickets/enhancement-shortcuts/spec.yaml
```

**What Happens:**
1. Planner greets and loads context silently
2. Analyzes spec.yaml, CLAUDE.md, codebase patterns
3. Shows "Plan Overview - Please Confirm"
4. You confirm (or provide corrections)
5. Generates detailed `plan.md` in ticket directory
6. Shows summary of created plan

**Output Location:**
```
Input:  /plan feature-user-auth
Output: specs/tickets/feature-user-auth/plan.md
```

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

# 4. IMPLEMENTATION: Execute the plan
/exec-auto feature-user-authentication  # For basic tasks
# OR
/exec feature-user-authentication       # For complex tasks (more interactive)
# OR
# Implement manually with AI pair programming
```

**Why this order matters:**
- Mechanical layer creates predictable structure
- Socrates fills spec with well-thought-out requirements
- Planner creates implementation roadmap from clear requirements
- Execution has complete context and clear direction
- **After Socrates, tasks don't feel complex anymore** (clarity through conversation)

### Session Example

**Session Start:**
```
You: /plan feature-user-auth

Planner: [Loads context silently - you see file reads in activity]

📋 **Plan Overview - Please Confirm**

**What I Understood:**

**Ticket:** User Authentication with Email/Password
**Type:** Feature
**Goal:** Enable users to securely authenticate and access private data

**Key Requirements:**
- Users can register with email and password
- Users can log in with valid credentials
- Users can reset forgotten passwords via email
- Sessions persist with "remember me" option
- All authentication works on desktop and mobile

**Technical Approach:**
- **Architecture:** JWT-based authentication with refresh tokens
- **Key Technologies:** bcrypt for hashing, JWT library for tokens, email service for resets
- **Integration Points:** Existing payment module (reuse JWT patterns)

**Scope:**
- **In Scope:** Email/password auth, password reset, session management
- **Out of Scope:** Social login (future work), 2FA (separate ticket)

**Estimated Effort:** 8-10 hours (High confidence)
- Implementation: 4-5 hours
- Testing: 3-4 hours
- Documentation: 1 hour

**Patterns to Follow:**
- Use httpOnly cookies per CLAUDE.md security standards
- Follow mobile-first design from project conventions
- Match existing API patterns in payment module

**Assumptions:**
- Email service (SendGrid) is available and configured
- JWT library is acceptable (bcrypt already in use)
- No breaking changes to existing auth-free endpoints

---

✅ Does this match your understanding?
❓ Any corrections before I generate the detailed plan?

You: Looks perfect!

Planner: [Generates detailed plan silently]

✅ Implementation plan generated!

**File:** `specs/tickets/feature-user-auth/plan.md`

**Plan Overview:**
- Ticket type: Feature
- Estimated effort: 8-10 hours (High confidence)
- Key decisions made: 5
- Implementation steps: 12
- Test cases: 15

**Key Technical Decisions:**
- JWT tokens in httpOnly cookies (stateless, scalable, XSS-protected)
- bcrypt for password hashing (industry standard, already in use)
- Email-based password reset with 1-hour token expiry

**Effort Estimate:**
- Total: 8-10 hours (High confidence)
- Breakdown: Implementation (4-5h) + Testing (3-4h) + Documentation (1h)

**Next Steps:**
1. Review the plan: `specs/tickets/feature-user-auth/plan.md`
2. Start implementation: `/exec-auto feature-user-auth` (or `/exec` for interactive mode)
3. Another Claude instance can implement directly from this plan

🎯 The plan is ready for implementation!
```

**Confirmation Correction Example:**
```
You: /plan exec-command

Planner: [Shows plan overview]

**What I Understood:**
**Ticket:** Exec command for CLI execution
**Type:** Feature
**Goal:** Add `cdd exec <file>` command to run scripts

You: Actually, I want a Claude Code slash command that uses AI to execute implementation plans, not a CLI command.

Planner: ✅ Ah! Got it - this is an AI slash command (/exec), not a CLI command.

Let me revise:

**What I Understood (Revised):**
**Ticket:** /exec slash command for AI-assisted implementation
**Type:** Feature
**Goal:** Create AI agent that reads plan.md and implements autonomously

**Technical Approach:**
- **Architecture:** Markdown prompt in `.claude/commands/exec.md`
- **Key Technologies:** Claude Code slash command system
- **Integration Points:** Reads plan.md from Planner output

[Updated overview continues...]

Does THIS match what you're thinking?
```

### What's in a Generated Plan

Looking at a real example (`enhancement-shorthand-ticket-paths/plan.md`):

**Structure (~790 lines for this enhancement):**

1. **Header** (Generated date, spec path, ticket type, estimated effort)

2. **Executive Summary**
   - Current state, target state, key changes (3-5 paragraphs)

3. **Analysis & Justification**
   - What works, what needs improvement, root cause
   - Improvement strategy with rationale
   - Alternatives considered (with pros/cons/why not chosen)

4. **Technical Decisions** (5 numbered decisions in this example)
   - Each decision: Choice → Rationale → Impact
   - Example: "Decision 1: Create Dedicated PathResolver Utility"

5. **Impact Assessment**
   - Breaking changes (or "No breaking changes")
   - Affected components (with specific files/changes)
   - Backward compatibility plan

6. **File Structure**
   - New files to create (with exact paths, purpose, key components)
   - Files to modify (with current state, changes needed, location)

7. **Implementation Steps** (Phased approach)
   - Phase 1: Preparation (0.5 hours)
   - Phase 2: Implementation (2-3 hours)
   - Phase 3: Validation & Testing (1-2 hours)
   - Phase 4: Documentation & Cleanup (1 hour)

   Each step includes:
   - Actions (what to do)
   - Expected Outcome (what success looks like)
   - Verification (how to confirm)
   - Potential Blockers (what could go wrong)
   - Code examples (actual snippets)

8. **Testing Strategy**
   - Unit tests to add (with actual test function signatures)
   - Manual testing checklist (checkbox format)

9. **Risk Assessment**
   - Risks with likelihood/impact/mitigation/fallback
   - Rollback strategy (how to undo if fails)

10. **Success Metrics**
    - Quantitative (typing reduction: 50+ → 20-30 characters)
    - Qualitative (workflow feels faster)

11. **Dependencies & Prerequisites**
    - Must complete before starting
    - External dependencies
    - Team dependencies

12. **Definition of Done** (Checkbox format)
    - [ ] Component created and tested
    - [ ] Documentation updated
    - [ ] All acceptance criteria met
    - [ ] No breaking changes
    - [ ] Quality gates passed (Black, Ruff, tests)

13. **Timeline & Effort Estimate** (Table format)
    | Phase | Time | Confidence |
    - Assumptions listed
    - Confidence factors explained

14. **Post-Enhancement Monitoring**
    - What to monitor
    - Success indicators
    - Warning signs

**What Makes It Executable:**
- **Exact file paths**: `src/cddoc/path_resolver.py:260`
- **Code structure shown**: Full class skeletons with docstrings
- **Numbered steps**: Clear sequence with dependencies
- **Time estimates per step**: "60 min", "20 min"
- **Success criteria**: "Expected Outcome" for each step
- **Potential blockers**: Anticipates problems
- **Definitive language**: "Create file X" (not "you could create")
- **Code examples**: Actual Python code to write

**Adaptation to Task Complexity:**
- **Simple tasks**: Fewer steps, shorter plan (still same detail per step)
- **Complex tasks**: More phases, more steps, longer plan (790+ lines)
- **Bug fixes**: Different structure (root cause → fix → regression prevention)
- **Spikes**: Research-focused (objectives → methods → evaluation)

---

## Plan Types & Structure

### Feature Plans

**Purpose:** New functionality or capabilities

**Key Sections:**
- Implementation Overview (what we're building, high-level approach)
- Technical Decisions (5-10 numbered decisions with rationale)
- File Structure (new files, files to modify, files to reference)
- Data Models & API Contracts (exact schemas, full type definitions)
- Implementation Steps (phased, numbered, with success criteria per step)
- Test Cases (actual test function signatures, arrange-act-assert)
- Error Handling (each scenario, exact error messages, HTTP codes)
- Integration Points (how this connects to existing code)
- Dependencies (exact package names with versions)
- Effort Estimation (breakdown by activity, assumptions, risks)

**Typical Length:** 400-800 lines depending on complexity

**Example Use Case:**
```bash
/plan feature-user-authentication
→ Generates plan for implementing complete auth system
```

### Bug Plans

**Purpose:** Issue investigation and resolution

**Key Sections:**
- Bug Analysis (symptom, expected behavior, impact assessment)
- Root Cause Analysis (hypothesis with evidence, likely location)
- Investigation Approach (step-by-step debugging plan)
- Fix Strategy (proposed solution, alternatives considered, rationale)
- Implementation Steps (before/after code examples with explanations)
- Testing Strategy (reproduction test, fix validation, regression tests)
- Regression Prevention (new tests to add, edge cases to cover)
- Rollback Plan (how to safely revert if needed)
- Effort Estimation

**Typical Length:** 300-500 lines

**Example Use Case:**
```bash
/plan bug-login-timeout
→ Generates investigation and fix plan for timeout issue
```

### Spike Plans

**Purpose:** Research, investigation, proof-of-concept

**Key Sections:**
- Research Objectives (questions to answer, decisions to inform)
- Investigation Scope (in scope / out of scope, timebox)
- Research Methods (how to investigate, time allocation per method)
- Investigation Steps (step-by-step research plan with expected findings)
- Evaluation Criteria (metrics to measure, trade-offs to consider)
- Deliverables (documents to produce, prototypes to create)
- Effort Estimation (research + prototyping + documentation, strict timebox)

**Typical Length:** 200-400 lines

**Example Use Case:**
```bash
/plan spike-database-options
→ Generates research plan for evaluating PostgreSQL vs MongoDB
```

### Enhancement Plans

**Purpose:** Improvements to existing features

**Key Sections:**
- Current State Analysis (how it works today, limitations)
- Proposed Improvements (desired state, benefits)
- Technical Decisions (approach, rationale, alternatives)
- Impact Assessment (breaking changes, affected components, backward compatibility)
- Implementation Steps (phased approach with validation)
- Success Metrics (how to measure improvement)
- Effort Estimation

**Typical Length:** 500-800 lines

**Example Use Case:**
```bash
/plan enhancement-shorthand-ticket-paths
→ Generates plan for improving slash command UX
```

---

## Autonomous Decision-Making

### Decision Framework

**The 90/10 Rule:**
- Planner makes ~90% of decisions autonomously based on context
- Asks 1-3 questions only when genuinely ambiguous with significant impact

**How Planner Decides:**

**1. From CLAUDE.md (Project Context):**
```
Example from CDD Framework:
- Tech Stack: Python 3.9+, Click, Rich, PyYAML → Use these
- Patterns: Handler pattern, template-driven → Follow these
- Standards: Black formatting, Ruff linting → Enforce these
- Conventions: Feature branches, pytest for testing → Apply these
```

**2. From Codebase Analysis:**
```
Examines up to 10 files to find:
- Similar features (how auth is done elsewhere)
- File structure patterns (where files live)
- Naming conventions (how things are named)
- Testing patterns (how tests are written)
- Error handling patterns (how errors are shown)
```

**3. From Industry Best Practices:**
```
Examples:
- REST API design (proper HTTP verbs, status codes)
- Security basics (hash passwords, validate input, use HTTPS)
- Error handling (specific messages, proper logging)
- Code organization (separation of concerns, DRY principle)
```

**4. From Template Structure:**
```
Templates guide what needs to be in the plan:
- Feature template → Need data models, API contracts, test cases
- Bug template → Need root cause, fix strategy, regression tests
- Spike template → Need research methods, evaluation criteria
```

### When Planner Asks Questions

**Rare, but happens when:**

1. **Genuine Ambiguity with Significant Impact**
   ```
   ❓ Should user sessions be real-time (WebSocket) or polling-based?

   💡 Recommendation: Polling with 30s interval
   Rationale: Simpler implementation, sufficient for this use case,
   aligns with existing patterns in codebase. WebSocket adds complexity
   without clear benefit for authentication status checking.

   Alternatives:
   - Real-time WebSocket: Instant updates, but complex server setup
   - Polling: Simple, proven, good enough for auth status

   Which approach should I use?
   ```

2. **Missing Critical Integration Info**
   ```
   ❓ Which email service should I integrate with?

   Context: Spec mentions "email for password reset" but doesn't
   specify provider. I see SendGrid mentioned in CLAUDE.md dependencies.

   💡 Recommendation: SendGrid (already in dependencies)
   Rationale: Already integrated, no new account setup needed

   Should I proceed with SendGrid or use a different service?
   ```

3. **Performance/Scale Trade-offs**
   ```
   ❓ What's the expected user load for this feature?

   💡 Recommendation: Optimize for <1000 concurrent users
   Rationale: Typical SaaS startup scale, allows simple caching strategy

   Alternatives:
   - <100 users: No caching needed, simplest
   - 1000-10,000: Redis caching, moderate complexity
   - >10,000: Distributed cache, significant infrastructure

   Which scale should I plan for?
   ```

**What Planner NEVER Asks:**
- ❌ "What file structure should I use?" (inferable from codebase)
- ❌ "Should I use Black for formatting?" (specified in CLAUDE.md)
- ❌ "What should I name the function?" (implementation detail)
- ❌ "How should I organize the code?" (follows existing patterns)

### Real-World Example

**From Building CDD Framework:**

**Only 1 correction needed** across all plan sessions:
- **Issue:** Planner interpreted `/exec` as CLI command instead of slash command
- **How caught:** Confirmation step showed "Add `cdd exec <file>` CLI command"
- **Resolution:** Developer explained "Actually, I want a slash command for AI execution"
- **Outcome:** Planner revised understanding and generated correct plan

**This demonstrates:**
- Confirmation step catches misunderstandings early (before wasted work)
- Questions are rare because context is usually sufficient
- When corrections needed, they happen at cheapest point (confirmation, not after plan written)

---

## Codebase Analysis

### Pattern Recognition (Limited Scope)

**Goal:** Find relevant patterns without overwhelming analysis

**Strict Limits (Critical):**
- **Max 10 files examined** total
- **Max 3 glob searches**
- **Max 30 seconds** for all analysis
- **Quality over quantity** (better 3 files deeply than 20 superficially)

**First Pass - Quick Scan (10 seconds):**

1. **Similar Features:**
   - Search `.claude/commands/*.md` (other slash commands)
   - Identify 2-3 most similar features
   - Note their patterns and structure

2. **Recent Context:**
   - Check 3-5 most recently modified files
   - Look for current development patterns
   - Understand active coding style

3. **Key Directories:**
   - Scan main source directory (1 level deep)
   - Identify where similar code would live
   - Note naming conventions

**Second Pass - Targeted Search (if needed):**

1. **Specific Files:**
   - If spec.yaml mentions specific files → Read those
   - If dependencies listed → Read integration points
   - Maximum 5 files per search

2. **Pattern Matching:**
   - Search for specific patterns (e.g., "authentication", "API endpoint")
   - Limit results to 3-5 most relevant files
   - Focus on same module/domain

**What Planner Looks For:**

```
Example Output (internal synthesis, not shown to user):

📚 Pattern Analysis (Completed in 12s):

**Similar Features Found:**
- `.claude/commands/socrates.md` - Slash command pattern, uses Rich
- `.claude/commands/spec-wizard.md` - File path parsing, YAML handling

**Technology Stack Detected:**
- `src/cddoc/cli.py` - Uses Click 8.1.7, Rich 13.x
- `src/cddoc/init.py` - pathlib for file ops, YAML for config

**Code Patterns to Follow:**
- CLI commands use Click decorators with Rich formatting
- File operations use pathlib.Path, not string concatenation
- Error handling uses Rich console with [red] styling
- Tests use pytest with fixtures in conftest.py

**Files Not Examined:** 87 other files (not relevant)
```

**For Large Codebases (>100 files):**

**Prioritize:**
- Files mentioned in CLAUDE.md as examples
- Files in same directory as dependencies
- Core domain files (src/core/, src/domain/)
- Most recent commits (last 7 days)

**Skip:**
- Test files (unless specifically needed)
- Vendor/node_modules
- Generated code
- Documentation files

**Future Polish Area:** Large codebase analysis (currently 10-file limit may miss patterns in huge projects)

### How It Informs Decisions

**Example 1: File Naming**
```
Analysis finds: src/cddoc/handlers/constitution_handler.py
Decision: New handler should be src/cddoc/handlers/plan_handler.py
(Follows existing pattern: handlers/{name}_handler.py)
```

**Example 2: Error Handling**
```
Analysis finds: Rich console.print(f"[red]Error: {message}[/red]")
Decision: Use same pattern for consistency
(Three-part error: what/why/how-to-fix with Rich formatting)
```

**Example 3: Testing Structure**
```
Analysis finds: tests/test_init.py with pytest fixtures
Decision: Create tests/test_path_resolver.py with same fixture pattern
(Match existing test organization and style)
```

---

## Confirmation Step (Critical Feature)

### Why It Exists

**Problem Solved:**
- Prevents spending time/tokens on wrong interpretation
- Catches fundamental misunderstandings early
- Builds developer confidence ("Planner got it")
- Creates shared mental model before detailed work

**Design Philosophy:**
> "The cheapest bug fix is the one you catch before writing code.
> The cheapest planning error is the one you catch before writing the plan."

### What's Shown

**Plan Overview Format:**

```markdown
📋 **Plan Overview - Please Confirm**

**What I Understood:**

**Ticket:** [Title from spec.yaml]
**Type:** [Feature/Bug/Spike/Enhancement]
**Goal:** [One-sentence description]

**Key Requirements:**
- [Requirement 1 from acceptance criteria]
- [Requirement 2]
- [Requirement 3]

**Technical Approach:**
- **Architecture:** [High-level technical approach]
- **Key Technologies:** [Main technologies from CLAUDE.md/patterns]
- **Integration Points:** [What this connects to]

**Scope:**
- **In Scope:** [What we're building]
- **Out of Scope:** [What we're explicitly not doing]

**Estimated Effort:** [X-Y hours] ([Confidence level])
- Implementation: [A hours]
- Testing: [B hours]
- Total: [Z hours]

**Patterns to Follow:**
- [Pattern 1 from codebase analysis]
- [Pattern 2 from CLAUDE.md]

**Assumptions:**
- [Assumption 1 from context]
- [Assumption 2]

---

✅ Does this match your understanding?
❓ Any corrections before I generate the detailed plan?
```

### Developer Responses

**Typical Responses:**

1. **Confirmation (Most Common):**
   ```
   Developer: "Looks perfect!"
   Developer: "Yes, proceed"
   Developer: "✅"

   → Planner generates detailed plan immediately
   ```

2. **Correction (Rare but Critical):**
   ```
   Developer: "Actually, I want a slash command, not a CLI command"

   → Planner revises understanding
   → Shows updated overview
   → Waits for new confirmation
   ```

3. **Clarification Question:**
   ```
   Developer: "Why did you choose JWT over sessions?"

   → Planner explains rationale
   → Shows updated overview if needed
   → Waits for confirmation
   ```

**Real-World Stats (from CDD Framework development):**
- **Only 1 correction needed** across entire framework build
- **Caught:** Slash command vs CLI command misunderstanding
- **Result:** Revised at confirmation step (before plan generation)
- **Value:** Saved time/tokens on wrong detailed plan

### Anxiety Removal

**Developer Experience:**

**Before Confirmation Step:**
```
Developer thinking: "Did the AI understand what I want?
Should I just hope for the best? What if it plans the wrong thing?"
```

**After Confirmation Step:**
```
Developer seeing: "Oh good, it understood perfectly.
The technical approach makes sense. Estimate seems reasonable.
I can confidently proceed."
```

**Psychological Impact:**
- Removes uncertainty ("did it get it?")
- Builds trust (AI demonstrates understanding)
- Enables confident execution (shared mental model)
- Catches errors cheaply (before detailed work)

---

## Effort Estimation

### Methodology

**Systematic Calculation:**

```markdown
**1. Implementation Time:**
Lines of code estimate × productivity rate:
- Simple CRUD: 50-100 LOC/hour
- Complex logic: 20-50 LOC/hour
- Integration work: 30-70 LOC/hour
File operations: +15 min per new file
Dependencies: +0.5-2 hours if new

**2. Testing Time:**
- Unit tests: ~1.5x implementation time
- Integration tests: ~1x implementation time
- End-to-end tests: ~0.5x implementation time
- Manual testing: 0.5-1 hour

**3. Complexity Multipliers:**
- Familiar patterns: 1x (we've done this)
- New patterns: 1.5x (learning curve)
- External integrations: 2x (API dependencies)
- Performance optimization: 2-3x (profiling, tuning)

**4. Additional Activities:**
- Documentation: 0.5-1 hour
- Code review prep: 0.5 hour
- Deployment/infrastructure: 0.5-2 hours
```

**Confidence Levels:**

```markdown
**High Confidence (±20%):**
- Familiar technology stack
- Similar patterns exist in codebase
- Clear requirements
- No external dependencies
- Example: "4-5 hours (High confidence)"

**Medium Confidence (±50%):**
- Some unknowns in requirements
- New library/framework to learn
- External API with documentation
- Example: "6-9 hours (Medium confidence)"

**Low Confidence (±100%):**
- Significant unknowns
- Research needed
- Unclear requirements
- Complex external integration
- Example: "8-16 hours (Low confidence) - Consider spike first"
```

### Human vs AI Execution Time

**Important Distinction:**

**Estimates are human-realistic:**
- Planner estimates like a human engineer
- Includes safety buffer (tend toward more hours)
- Accounts for context switching, breaks, meetings
- Realistic for human pair programming with AI

**AI execution is faster:**
- `/exec-auto` typically finishes faster than estimate
- No breaks or context switching
- Can read/write code very quickly
- Follows plan mechanically without decision fatigue

**Example:**
```
Planner estimates: 4-6 hours
exec-auto completes: ~2-3 hours
Human + AI pair: ~4-5 hours
Human solo: ~6-8 hours
```

**Why This Is Useful:**
- Acts as **complexity signal** (2hr task vs 20hr task)
- Provides **buffer** if exec encounters blockers
- Gives **realistic timeline** if human implements
- Shows **relative effort** between tasks

### Estimate Format in Plans

**Example from Real Plan:**

```markdown
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
- Similar patterns exist (init.py, new_ticket.py)
- No external dependencies needed
- Backward compatibility design reduces risk

**Assumptions:**
- Developer familiar with Python 3.9+ and type hints
- Development environment already set up (Poetry, pytest)
- No unexpected edge cases in slash command parsing
- Fuzzy matching performance adequate (<100 tickets)

**Risk Factors:**
- If template validation is complex: +2-3 hours
- If file permissions issues: +1-2 hours
- If integration requires refactoring: +3-5 hours
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

3. /plan feature-user-auth ← YOU ARE HERE
   ↓ (Intelligence: Create implementation plan)
   plan.md with detailed, executable steps

4. /exec-auto feature-user-auth
   ↓ (Intelligence: Execute autonomously)
   Feature implemented
```

**Why This Sequence Works:**
- **Mechanical first** → Predictable structure
- **Socrates second** → Clear requirements (tasks don't feel complex anymore)
- **Planner third** → Executable roadmap (senior-level decisions made)
- **Exec fourth** → Implementation (straightforward because context complete)

**Complexity Decomposition:**
> "After talking to Socrates, tasks don't feel complex anymore."

The framework decomposes complexity through conversation:
1. Socrates → Developer clarity (fuzzy idea → clear requirements)
2. Planner → AI clarity (requirements → executable roadmap)
3. Exec → Implementation (feels straightforward, context complete)

### Handoff from Socrates

**What Planner Receives:**

From Socrates session, spec.yaml contains:
- **User Story** (who, what, why)
- **Business Value** (why this matters)
- **Acceptance Criteria** (specific, testable success conditions)
- **Implementation Scope** (frontend/backend/database changes)
- **Dependencies** (required and optional)
- **Constraints** (technical, business, resource)
- **Success Metrics** (how to measure success)

**Quality Impact:**
- Complete spec → Planner makes better decisions
- Clear requirements → Fewer questions needed
- Well-defined scope → No ambiguity about in/out
- Success criteria → Testing strategy writes itself

**Example:**
```yaml
# From Socrates session
ticket:
  type: feature
  title: User Authentication with Email/Password

user_story: |
  As a project manager using the SaaS platform,
  I want to securely authenticate with email and password,
  So that I can access my private projects without others seeing my data.

acceptance_criteria:
  - Users can register with email and password
  - Users can log in with valid credentials
  - Users can reset password via email link
  - Sessions persist with "remember me" option (30 days)
  - Invalid login shows appropriate error messages

# Planner reads this and knows:
# - What to build (auth system)
# - Who it's for (project managers, business users)
# - Success definition (5 specific criteria)
# - Scope (email/password, not social login)
```

### Handoff to Exec

**What Exec Receives:**

From Planner session, plan.md contains:
- **Executive Summary** (current state → target state)
- **Technical Decisions** (documented with rationale)
- **File Structure** (exact paths, what to create/modify)
- **Implementation Steps** (numbered, phased, with success criteria)
- **Code Examples** (actual snippets to write)
- **Test Cases** (actual test function signatures)
- **Definition of Done** (checklist format)

**Execution Modes:**

**1. /exec-auto (Autonomous)**
- Reads plan.md at start
- Executes steps sequentially
- Minimal questions (tries harder to solve independently)
- Works well for basic tasks
- Faster than human implementation

**2. /exec (Interactive)**
- Reads plan.md as guidance
- More willing to ask developer questions
- Handles complex tasks better
- Interactive problem-solving

**3. Manual with AI Pair**
- Developer reads plan
- Uses AI as pair programmer
- Implements step-by-step with AI help
- Full control, AI assists

**Success Rate:**
> "I have been building this whole framework based on its own proposed flow."

- Basic tasks → `/exec-auto` handles autonomously
- CDD Framework built using this workflow (dogfooding)
- Lack of bugs validates the approach
- After Socrates, tasks "don't feel complex"

**Real-World Example:**
```bash
# Developer runs
/exec-auto enhancement-shorthand-ticket-paths

# Exec reads plan.md (790 lines)
# Sees 4 phases, 12 numbered steps
# Executes autonomously:
# - Creates src/cddoc/path_resolver.py
# - Updates .claude/commands/*.md files
# - Writes tests/test_path_resolver.py
# - Updates documentation
# - Runs Black, Ruff, pytest
#
# Completes in ~2-3 hours (estimate was 4-6 hours)
# All tests pass, no manual intervention needed
```

---

## Philosophy & Design

### Core Thesis

> **"LLMs + Right Context = Impressive Work"**

This is what CDD Framework proves, and Planner embodies it:

**The Context Problem:**
- LLMs are powerful but need context to be effective
- Repeatedly providing context is tedious and error-prone
- Missing context leads to poor decisions and generic code

**The CDD Solution:**
- Capture context once (CLAUDE.md, specs, templates)
- Load systematically (project foundation + requirements + codebase patterns)
- Enable AI to work at senior-level (confident decisions, detailed plans)

**Planner as Proof:**
- Loads CLAUDE.md → Project patterns, conventions, standards
- Loads spec.yaml → Requirements, acceptance criteria, scope
- Analyzes codebase → Implementation examples, file structure
- **Result:** Plans detailed enough for autonomous execution

**Validation:**
> "I have been building this whole framework based on its own proposed flow."

The CDD Framework was built using:
1. Socrates to gather requirements
2. Planner to create implementation plans
3. Exec to implement autonomously

**This proves:**
- The workflow works for real, complex software
- Context-driven AI can architect like a senior engineer
- Quality emerges from complete context (low bug count)

### Senior-Level Autonomy

**Planner as "Experienced Engineer Talking to PO":**

**Characteristics:**
- **Confident but not arrogant** (makes decisions, asks when needed)
- **Pragmatic over theoretical** (chooses what works, not what's perfect)
- **Detail-oriented** (plans are granular and specific)
- **Context-aware** (synthesizes CLAUDE.md + spec + codebase)
- **Efficient** (1-3 questions max, only when genuinely needed)

**Real Feedback:**
> "It feels like an experienced engineering talking to a PO."

**Why This Works:**
- Senior engineers have seen patterns before → Planner analyzes codebase
- Senior engineers know best practices → Planner uses industry standards
- Senior engineers ask few questions → Planner decides autonomously (90%)
- Senior engineers explain decisions → Planner documents rationale

**Example Decision Pattern:**

```markdown
## Technical Decision 3: Use stdlib difflib for Fuzzy Matching

**Choice:** Python's built-in `difflib.get_close_matches()`
           with 70% similarity cutoff

**Rationale:**
- No external dependencies (aligns with CLAUDE.md minimal deps philosophy)
- Proven library (part of stdlib since Python 2.1)
- Sufficient for ticket name matching (typical counts <100)
- Fast enough (not performance bottleneck)

**Alternatives Considered:**
- fuzzywuzzy library: More features, but external dependency
- Levenshtein distance: More accurate, but overkill for ticket names
- Custom implementation: Full control, but reinventing wheel

**Impact:**
Zero new dependencies, fast enough for typical use,
maintainable (stdlib is well-documented)
```

This is how a senior engineer thinks: pragmatic choice, clear rationale, alternatives considered, impact understood.

### AI-to-AI Communication

**Design Principle:**
> "Your plan is not for a human to read casually - it's for another AI instance to execute precisely."

**Language Style:**

**✅ Definitive (Not Tentative):**
```
Good: "Create file `src/api/auth.py`"
Bad:  "You could create a file for auth"

Good: "The API will return 401 for invalid credentials"
Bad:  "The API might return an error"

Good: "Install `bcrypt==4.0.1` for password hashing"
Bad:  "Consider using bcrypt for passwords"
```

**✅ Specific (Not Vague):**
```
Good: "Create `src/cddoc/handlers/plan_handler.py` with `PlanHandler` class"
Bad:  "Create a handler file"

Good: "Install `click==8.1.7` for CLI argument parsing"
Bad:  "Install Click"

Good: "Test coverage must be ≥80% for all new code"
Bad:  "Test coverage should be good"
```

**✅ With Code Examples:**
```
Good:
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

Bad:
"Create a login endpoint that handles authentication"
```

**Why This Matters:**
- `/exec-auto` needs concrete instructions, not suggestions
- Ambiguity leads to wrong implementation choices
- Code examples show exact structure expected
- Definitive language enables autonomous execution

### Complexity Through Clarity

**Key Insight:**
> "After talking to Socrates, tasks don't feel complex anymore."

**How Complexity Decomposes:**

**Stage 1: Before Socrates (Fuzzy)**
```
Developer thinks: "I need some kind of authentication...
probably email and password... users should be able to log in...
there's probably edge cases I'm forgetting..."

Complexity: High (vague, incomplete, uncertain)
```

**Stage 2: After Socrates (Clear)**
```
spec.yaml says: "Users can register with email and password.
Users can log in with valid credentials. Users can reset password
via email link. Sessions persist with 'remember me' option."

Complexity: Medium (clear requirements, defined scope)
```

**Stage 3: After Planner (Executable)**
```
plan.md says: "Step 1: Create src/api/auth.py with LoginHandler class.
Step 2: Implement bcrypt password hashing in hash_password() function.
Step 3: Generate JWT token using jose library with 30-day expiry..."

Complexity: Low (step-by-step instructions, clear path)
```

**Result:**
- Socrates → Requirements clarity
- Planner → Implementation clarity
- Exec → Straightforward execution

**Validation:**
> "I haven't found a terrible complex task yet while building this framework."

Not because tasks are simple, but because **clarity makes complexity manageable**.

---

## Business Rules & Edge Cases

### When to Use /plan

**✅ Use After Socrates:**
```
Recommended flow:
1. cdd new feature user-auth
2. /socrates feature-user-auth (fill spec.yaml)
3. /plan feature-user-auth (generate plan.md) ← HERE
4. /exec-auto feature-user-auth (implement)
```

**✅ Use for All Ticket Types:**
- Features (new capabilities)
- Bugs (investigation + fix)
- Spikes (research + evaluation)
- Enhancements (improvements)

**⚠️ Less Useful Without Context:**
- Missing CLAUDE.md → Generic plans (can't use project patterns)
- Incomplete spec.yaml → May ask questions or generate basic plan
- No similar codebase patterns → Falls back to industry best practices

### Edge Cases

**1. Incomplete spec.yaml**

**Designed Behavior:**
- Planner should detect gaps in spec
- Ask questions to fill critical missing info
- Or suggest running `/socrates` first

**Actual Experience:**
- Not tested in practice (specs were always complete)
- Framework built with complete specs from Socrates

**Recommendation:**
If you run `/plan` on incomplete spec:
- Expect questions during confirmation step
- Or run `/socrates` first to complete spec

**2. Missing CLAUDE.md**

**What Happens:**
```markdown
⚠️ Warning: CLAUDE.md not found

I'll generate the plan with general best practices, but won't be tailored to:
- Tech stack
- Architecture patterns
- Conventions
- Standards

**Recommendation:** Run `cdd init` to create CLAUDE.md,
then `/socrates CLAUDE.md` to complete it.

Should I proceed with generic plan, or set up CLAUDE.md first?
```

**Impact:**
- Plans will be less project-specific
- Won't follow your conventions
- May choose different tech stack than you use
- Still generates valid plan, just not optimized

**3. Large Codebase (>500 files)**

**Current Limitation:**
- 10-file analysis limit
- May miss relevant patterns in huge codebases

**Impact:**
- Planner falls back to:
  - CLAUDE.md patterns (if available)
  - Industry best practices
  - Template structure

**Future Polish Area:**
- Acknowledged limitation
- Could improve with:
  - Smarter file prioritization
  - Indexed codebase search
  - Developer hints ("look at module X")

**Current Mitigation:**
- Document key patterns in CLAUDE.md
- Reference similar files in spec.yaml
- Planner prioritizes files mentioned in context

**4. Ambiguous Spec (Multiple Valid Approaches)**

**Expected Behavior:**
- Planner shows confirmation with chosen approach
- Developer can correct if wrong choice
- Or Planner asks question with recommendation

**Example:**
```markdown
📋 Plan Overview - Please Confirm

**Technical Approach:**
- **Architecture:** Polling-based status checks (30s interval)
- **Rationale:** Simple implementation, sufficient for auth status

**Did I choose the right approach?**
If you wanted real-time WebSocket instead, let me know and I'll revise.
```

**Why This Works:**
- Confirmation step catches wrong choices
- Planner makes reasonable default choice
- Developer corrects if needed (before plan generation)

---

## Testing

### Manual Testing Approach

**Why Manual?**

Per CLAUDE.md standards:
> **AI-driven features** (slash commands, conversational interfaces) → Manual testing with checklist

Planner is:
- Conversational (confirmation step, optional questions)
- Non-deterministic (adapts to different specs, codebases)
- Creative (makes architectural decisions)

Traditional unit tests are inappropriate for this type of AI feature.

### Testing Checklist

**✅ Correct Output Format:**
- [ ] Produces valid Markdown for plan.md
- [ ] All template sections are filled (appropriate to ticket type)
- [ ] Formatting is consistent and readable
- [ ] Code examples use proper markdown code blocks
- [ ] File paths are exact and absolute

**✅ Handles Edge Cases:**
- [ ] Empty spec.yaml (asks questions or suggests /socrates)
- [ ] Partially filled spec (fills gaps, asks if needed)
- [ ] Missing CLAUDE.md (warns, offers generic plan)
- [ ] Large codebase (still generates valid plan)
- [ ] Ambiguous requirements (makes reasonable choice, shows in confirmation)

**✅ Confirmation Step:**
- [ ] Shows plan overview before generation
- [ ] Includes all key sections (understood, approach, effort, assumptions)
- [ ] Waits for user confirmation
- [ ] Accepts corrections gracefully
- [ ] Revises understanding when corrected

**✅ Autonomous Decision-Making:**
- [ ] Makes decisions from CLAUDE.md (uses specified tech stack)
- [ ] Follows codebase patterns (matches existing style)
- [ ] Uses industry best practices (REST, security, error handling)
- [ ] Asks few questions (1-3 max, only when needed)
- [ ] Questions include recommendations (not just "what should I do?")

**✅ Context Loading:**
- [ ] Loads spec.yaml successfully
- [ ] Loads CLAUDE.md successfully
- [ ] Detects ticket type correctly (feature/bug/spike/enhancement)
- [ ] Loads correct template (matches ticket type)
- [ ] Analyzes codebase (within 10-file, 30s limits)

**✅ Plan Quality:**
- [ ] Uses definitive language ("create file X", not "you could")
- [ ] Includes exact file paths (src/module/file.py:123)
- [ ] Provides code examples (actual snippets)
- [ ] Numbers implementation steps clearly
- [ ] Includes success criteria per step
- [ ] Documents technical decisions with rationale
- [ ] Provides effort estimates with confidence level

**✅ Integration:**
- [ ] plan.md saved in correct location (same dir as spec.yaml)
- [ ] Shows summary after generation
- [ ] Compatible with /exec (exec can read and execute plan)

### Test Scenarios

**Scenario 1: Feature Ticket (Complete Spec)**
```
Given: specs/tickets/feature-user-auth/spec.yaml (complete from Socrates)
When: /plan feature-user-auth
Then:
  - Loads context silently
  - Shows confirmation with technical approach
  - Generates detailed plan.md (400-800 lines)
  - Includes: implementation steps, test cases, effort estimate
  - Uses project tech stack from CLAUDE.md
  - Follows codebase patterns
```

**Scenario 2: Bug Ticket**
```
Given: specs/tickets/bug-login-timeout/spec.yaml
When: /plan bug-login-timeout
Then:
  - Uses bug plan template (not feature template)
  - Includes: root cause analysis, fix strategy, regression prevention
  - Shorter than feature plan (300-500 lines)
  - Focus on investigation → fix → validation
```

**Scenario 3: Spike Ticket**
```
Given: specs/tickets/spike-database-options/spec.yaml
When: /plan spike-database-options
Then:
  - Uses spike plan template
  - Includes: research objectives, investigation methods, evaluation criteria
  - Includes strict timebox (as specified in spec)
  - Deliverable is recommendation document, not implementation
```

**Scenario 4: Confirmation Correction**
```
Given: Spec about "/exec" command (ambiguous: CLI vs slash command)
When: /plan exec-command
Then:
  - Shows confirmation: "CLI command for execution"
When: Developer corrects: "Actually, I want a slash command"
Then:
  - Revises understanding
  - Shows updated confirmation: "Slash command for AI execution"
  - Waits for new confirmation before generating plan
```

**Scenario 5: Missing CLAUDE.md**
```
Given: Project without CLAUDE.md
When: /plan feature-user-auth
Then:
  - Shows warning about missing CLAUDE.md
  - Offers to proceed with generic plan
  - Plan uses industry best practices (not project-specific patterns)
```

**Scenario 6: Large Codebase**
```
Given: Project with 500+ files
When: /plan feature-new-capability
Then:
  - Analyzes up to 10 files (respects limit)
  - Falls back to CLAUDE.md patterns
  - Still generates valid, executable plan
  - May miss some codebase-specific patterns
```

---

## Performance & Characteristics

**Session Duration:**
- Typical session: 1-3 minutes
- Context loading: 10-30 seconds (silent)
- Confirmation review: 30-60 seconds (developer reads)
- Plan generation: 30-120 seconds (depending on complexity)

**Context Usage:**
- Loads: spec.yaml, CLAUDE.md, ticket template, up to 10 codebase files
- Analyzes: Patterns, conventions, similar features
- Generates: 200-800 line plan.md (depends on task complexity)

**Interaction Pattern:**
- Mostly autonomous (silent analysis)
- Shows confirmation (developer reviews)
- Rare questions (1-3 max, only if ambiguous)
- Final summary (shows what was created)

**Scalability:**
- Works on projects of any size
- 10-file limit prevents overwhelming analysis
- Template-driven structure scales to complex tasks
- Effort estimates adapt to task complexity

**Reliability:**
- High success rate (framework built using this workflow)
- Confirmation step catches misunderstandings (1 correction in entire framework build)
- Plans are executable (basic tasks run via /exec-auto)
- Low bug count validates quality

---

## Dependencies

### Required Dependencies

**Claude Code (AI Assistant)**
- Purpose: Planner runs as slash command within Claude Code
- Version: Any version supporting slash commands
- Integration: Command definition in `.claude/commands/plan.md`

**spec.yaml (Requirements)**
- Purpose: Input for plan generation (what to build)
- Source: Created by `cdd new`, filled by `/socrates`
- Must contain: Ticket type, acceptance criteria, scope

**CLAUDE.md (Project Context)**
- Purpose: Tech stack, patterns, conventions, standards
- Location: Project root
- Created by: `cdd init` or manually
- **Highly recommended** (plans are generic without it)

**Plan Templates**
- Purpose: Structure for different ticket types
- Location: `.cdd/templates/`
- Templates needed:
  - `feature-plan-template.md`
  - `bug-plan-template.md`
  - `spike-plan-template.md`
- Installation: Via `cdd init`

### Integration Points

**With Socrates:**
- Consumes: spec.yaml filled by Socrates
- Relationship: Socrates → requirements clarity, Planner → implementation clarity
- Handoff: Complete spec with acceptance criteria, scope, dependencies

**With Exec:**
- Produces: plan.md for execution
- Relationship: Planner → executable roadmap, Exec → implementation
- Handoff: Detailed steps, code examples, test cases, definition of done

**With Mechanical Layer:**
- Uses: File structure from `cdd new` (specs/tickets/{name}/)
- Respects: Naming conventions, directory structure
- Output location: Same directory as spec.yaml

**With File System:**
- Reads: spec.yaml, CLAUDE.md, codebase files
- Writes: plan.md (markdown file)
- Works with: Version-controlled files (git)

---

## Future Enhancements

**Improved Codebase Analysis:**
- Smarter file prioritization for large codebases
- Indexed search for relevant patterns
- Developer hints ("analyze module X")
- Increase 10-file limit intelligently

**Learning from Execution Feedback:**
- Track which plans execute successfully
- Learn from /exec corrections and adaptations
- Improve estimates based on actual completion times
- Adapt patterns based on project evolution

**Multi-Ticket Planning:**
- Generate coordinated plans for related tickets
- Identify dependencies between tickets
- Suggest implementation order
- Detect conflicts or duplicated work

**Interactive Refinement:**
- Allow plan editing before finalization
- "Revise step 3 to use X instead of Y"
- Incremental plan updates during implementation

**Template Customization:**
- Project-specific plan templates
- Domain-specific sections (e.g., security review for fintech)
- Team-specific structure preferences

---

## Related Documentation

- [Socrates - Requirements Gathering](socrates.md) - Fills spec.yaml that Planner consumes
- [Init Command](init-command.md) - Framework initialization (creates CLAUDE.md, templates)
- [New Command](new-command.md) - Ticket creation (creates spec.yaml structure)
- [CLI Reference Guide](../guides/CLI_REFERENCE.md) - Complete command reference

---

*Last updated: 2025-11-03 | Status: Production | Version: 0.1.0*

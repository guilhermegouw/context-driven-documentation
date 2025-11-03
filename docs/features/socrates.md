# Feature: Socrates - AI Requirements Gathering

> Living documentation for the Socrates AI requirements specialist

**Status:** Production
**Version:** 0.1.0
**Last Updated:** 2025-11-02

---

## Overview

Socrates is an **AI-powered thinking partner** that helps developers create comprehensive specifications through guided Socratic dialogue. Rather than being a form to fill out, Socrates is a specialized AI agent that brainstorms with you, asks probing questions, and helps structure your thinking.

**Why it exists:**

Developers often struggle to write complete specifications alone. Important details get overlooked—edge cases, dependencies, vague success criteria, missing business context. Socrates solves this by serving as an expert thought partner who:
- Guides your thinking through intelligent questions
- Uses templates as a roadmap to ensure nothing critical is missed
- Builds documentation incrementally through natural conversation
- Gives you **confidence** that you've thought through what matters

**Key Capabilities:**
- Prevents missing critical details (edge cases, dependencies, acceptance criteria, business context)
- Guided Socratic dialogue using progressive clarification
- Intelligent context loading (CLAUDE.md, templates, related features)
- Template-driven thinking without feeling like interrogation
- In-context work with approval loop before writing
- Supports 6 file types with tailored questioning approaches
- Stays strictly in scope (requirements only, not implementation)

**Philosophy:**

Socrates codifies the natural process of "thinking out loud with AI." Before CDD, developers would paste requirements to Claude and brainstorm to clarify their approach. Socrates systematizes this into a specialized agent that asks the right questions, guided by templates, to help you think clearly and comprehensively.

---

## Current Implementation

### How It Works Today

**User Perspective:**
1. Developer runs `/socrates [file-path]` on a spec or documentation file
2. Socrates loads context (CLAUDE.md, templates, related work)
3. Natural brainstorming conversation begins
4. Socrates builds content incrementally, asking clarifying questions
5. Shows complete summary for approval
6. Writes file only after confirmation

**Core Behavior:**
- **Thinking partner, not interrogator**: Conversational, collaborative tone
- **Progressive clarification**: Acknowledges what's clear, targets what's vague
- **Template-guided**: Uses templates as roadmap without rigid questioning
- **Context-aware**: Synthesizes project context before asking questions
- **In-scope only**: Redirects implementation details to planning phase
- **Approval-gated**: Shows full result, gets explicit "yes" before writing

### Architecture Overview

**Intelligence Layer Integration:**
```
CDD Framework Architecture
├── Mechanical Layer (CLI)
│   ├── cdd init - Framework initialization
│   └── cdd new - Ticket/doc creation
└── Intelligence Layer (Slash Commands)
    ├── /socrates - Requirements gathering ← YOU ARE HERE
    ├── /plan - Implementation planning
    └── /exec - AI-assisted implementation
```

**Command Structure:**
- **Location**: `.claude/commands/socrates.md`
- **Type**: Slash command (AI persona)
- **Invocation**: `/socrates [file-path]`
- **Context**: Loads CLAUDE.md, templates, related files automatically

**Data Flow:**
```
User invokes /socrates
    ↓
Load project context (CLAUDE.md, templates)
    ↓
Read target file (current state)
    ↓
Intelligent reconnaissance (related features/tickets)
    ↓
Present context summary
    ↓
Guided Socratic dialogue
    ↓
Build content incrementally in context
    ↓
Show complete summary
    ↓
Get approval
    ↓
Write file
```

### Key Components

**Context Loading System:**
- **Step 1**: Load CLAUDE.md (project foundation)
- **Step 2**: Read target file (current state)
- **Step 3**: Determine file type from path pattern
- **Step 4**: Load appropriate template
- **Step 5**: Intelligent reconnaissance (related context)
- **Step 6**: Synthesize and present findings

**Progressive Clarification Engine:**
- Acknowledges what's clear: "✅ Clear: [summary]"
- Targets specific vagueness: "❓ What I'm unclear about: [gap]"
- Provides concrete options: Multiple specific scenarios to choose from
- Prevents redundant questions by building on previous answers

**Scope Management:**
- **In scope**: Requirements, constraints, acceptance criteria, dependencies
- **Out of scope**: Implementation details, code structure, technology choices
- **Redirect patterns**: Politely redirect out-of-scope questions to appropriate phase

**Approval Loop:**
- Keeps all content in memory during conversation
- Shows complete formatted summary at end
- Waits for explicit confirmation
- Allows iteration if changes needed
- Writes only after approval

---

## Usage

### Basic Usage

**Starting a Socrates Session:**
```bash
# On a ticket spec
/socrates specs/tickets/feature-user-auth/spec.yaml

# On project constitution
/socrates CLAUDE.md

# On feature documentation
/socrates docs/features/authentication.md

# On a guide
/socrates docs/guides/getting-started.md
```

**What Happens:**
1. Socrates greets you and loads context
2. Shows summary of what it learned (project, template, related work)
3. Starts conversational brainstorming
4. Asks progressive questions to fill gaps
5. Shows complete result
6. Writes file after your approval

### Supported File Types

**1. CLAUDE.md (Project Constitution)**
```bash
/socrates CLAUDE.md
```
**Topics covered**: Project overview, architecture, tech stack, development standards, team conventions

**2. Feature Tickets (specs/tickets/feature-*/spec.yaml)**
```bash
/socrates specs/tickets/feature-payment-processing/spec.yaml
```
**Topics covered**: User story, business value, acceptance criteria, implementation scope, dependencies

**3. Bug Tickets (specs/tickets/bug-*/spec.yaml)**
```bash
/socrates specs/tickets/bug-login-timeout/spec.yaml
```
**Topics covered**: Problem description, reproduction steps, environment, impact assessment

**4. Spike Tickets (specs/tickets/spike-*/spec.yaml)**
```bash
/socrates specs/tickets/spike-database-options/spec.yaml
```
**Topics covered**: Research questions, success criteria, investigation scope, deliverables

**5. Enhancement Tickets (specs/tickets/enhancement-*/spec.yaml)**
```bash
/socrates specs/tickets/enhancement-improve-performance/spec.yaml
```
**Topics covered**: Current state, proposed improvements, success metrics, constraints

**6. Feature Documentation (docs/features/*.md)**
```bash
/socrates docs/features/authentication.md
```
**Topics covered**: Overview, architecture, implementation details, API reference, examples

**7. User Guides (docs/guides/*.md)**
```bash
/socrates docs/guides/quick-start.md
```
**Topics covered**: Introduction, prerequisites, step-by-step instructions, examples, troubleshooting

### Complete Workflow Example

**The Recommended Flow:**

```bash
# 1. MECHANICAL: Create ticket structure
cdd new feature user-authentication
# → Creates specs/tickets/feature-user-authentication/spec.yaml (empty template)

# 2. INTELLIGENCE: Brainstorm and fill spec
/socrates specs/tickets/feature-user-authentication/spec.yaml
# → Guided conversation to build complete specification

# 3. INTELLIGENCE: Generate implementation plan
/plan feature-user-authentication
# → Creates detailed plan based on complete spec

# 4. IMPLEMENTATION: Build the feature
# → AI solo, pair programming, or developer solo
```

**Why this order matters:**
- Mechanical layer creates predictable structure
- Socrates fills it with well-thought-out requirements
- Plan creates implementation roadmap from clear requirements
- Implementation has complete context and clear direction

### Conversation Example

**Session Start:**
```
You: /socrates specs/tickets/feature-user-auth/spec.yaml

Socrates: 👋 Hey! I'm Socrates. Let me load context before we start...

📚 Context loaded:

**Project:** CDD Framework (Python CLI tool)
**Working on:** Feature ticket - user authentication
**Template structure:** User story, acceptance criteria, technical scope, dependencies
**Related context:**
  - No existing auth features found
  - CLAUDE.md emphasizes file-based, local-only approach
  - Security-first mindset for handling user data

**Key insights:**
- Local tool, no remote auth needed
- Security standards defined in CLAUDE.md
- File system access patterns established

Given this is a local CLI tool, I'm curious - what kind of authentication
are you thinking about? Is this for protecting local files, or something else?
```

**Progressive Clarification:**
```
You: We need to protect sensitive project data

Socrates: ✅ Clear: Authentication to protect sensitive project data

❓ When you say "sensitive project data", what are we protecting exactly?

I'm thinking:
- Configuration files with secrets (API keys, tokens)?
- Business-critical documentation (proprietary specs)?
- Personal developer notes (private TODOs, ideas)?
- All project files from unauthorized access?

Which scenario matches your concern?
```

**Approval Loop:**
```
Socrates: Great work! We've covered a lot of ground. Let me show you
everything we've discussed:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 COMPLETE SPECIFICATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## User Story
As a developer working on sensitive projects,
I want to encrypt project documentation files,
So that proprietary information stays protected on my local machine.

## Business Value
[Complete content...]

## Acceptance Criteria
- ✅ Users can encrypt/decrypt project files with password
- ✅ Strong encryption (AES-256 minimum)
[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Does this look good? Should I save this to
specs/tickets/feature-user-auth/spec.yaml?
Any changes or additions before I write it?

You: Looks perfect!

Socrates: ✅ Perfect! I've saved everything to
specs/tickets/feature-user-auth/spec.yaml

We documented:
✅ User story - Developers need encryption for sensitive projects
✅ Acceptance criteria - 8 specific, testable requirements
✅ Implementation scope - CLI commands and encryption logic
✅ Dependencies - Cryptography library, keyring integration
✅ Success metrics - Security audit passing, user adoption

Next steps: Use `/plan user-auth` to create implementation plan
```

---

## How Sessions Work

### 1. Initialization Phase

**Intelligent Context Loading (6 Steps):**

**Step 1: Load Project Foundation**
- Reads CLAUDE.md to understand project world
- Learns tech stack, patterns, conventions, constraints
- Provides lens to interpret everything else

**Step 2: Read Target File**
- Examines current state of the file
- Identifies what exists and what's missing
- Determines starting point for conversation

**Step 3: Determine File Type**
- Analyzes file path pattern and content
- Identifies: ticket type, documentation type, or constitution
- Selects appropriate conversation approach

**Step 4: Load Appropriate Template**
- For tickets: `.cdd/templates/[type]-ticket-template.yaml`
- For docs: `.cdd/templates/[type]-doc-template.md`
- Understands what a complete document needs

**Step 5: Intelligent Reconnaissance**
- For features: Looks for similar features or related code
- For bugs: Examines broken code if path provided
- For spikes: Checks for previous research
- Gathers relevant context automatically

**Step 6: Synthesize and Present Context**
- Summarizes project, file type, template structure
- Highlights related context found
- Shares key insights that affect this work
- Sets stage for intelligent conversation

### 2. Dialogue Phase

**Natural Conversation Flow:**

Socrates doesn't interrogate—it converses. Instead of rapid-fire questions, it:
- Asks open-ended questions to understand your thinking
- Builds on your answers progressively
- Acknowledges what's clear before probing vagueness
- Provides concrete options when clarifying ambiguity
- Challenges incomplete thinking politely
- Keeps conversation focused on requirements

**Progressive Clarification Technique:**

```
Structure:
✅ Clear: [Acknowledge what you understood]
❓ What I'm unclear about: [Identify specific gap]
For example, I'm thinking:
- [Option A with concrete example]
- [Option B with concrete example]
- Or [Option C - different direction]
Which direction feels right?
```

**Example:**
```
You: "We need better performance"
Socrates: "What do you mean by better performance?"
You: "The API is slow"

❌ Bad: "Can you be more specific about performance?"
[Asking same question again!]

✅ Good: "✅ Got it - the API is the bottleneck.

❓ When you say 'slow', are we talking:
- Response time is 2s and should be 200ms?
- Throughput is too low under load?
- Specific endpoints timing out?

Which scenario matches what you're seeing?"
```

**Staying In Scope:**

Socrates maintains hard boundaries:

**✅ In Scope (Requirements):**
- What problem THIS ticket solves
- Who is affected
- What success looks like
- Edge cases and constraints
- Acceptance criteria
- Dependencies

**❌ Out of Scope (Implementation):**
- How to implement it
- Specific libraries/frameworks to use
- Code patterns or architecture
- API response structures

**Redirect Pattern:**
```
You: "Should we use bcrypt or argon2 for password hashing?"

Socrates: "That's an implementation detail for later. For this spec,
let's just capture: 'Passwords must be hashed using industry-standard
algorithm with appropriate salt and cost factor.'

The implementation plan will decide specific technology.

Let's stay focused on WHAT security requirements we need, not HOW
to implement them."
```

### 3. Approval Phase

**In-Context Work:**
- Socrates never writes during conversation
- Keeps all content in memory
- Allows you to review complete result
- Prevents premature or incorrect updates

**Complete Summary:**
- Shows ALL sections with full content
- Formatted exactly as it will be written
- Clearly separated with visual dividers
- Easy to review at a glance

**Approval Loop:**
```
1. Show complete summary
2. Ask: "Does this look good? Any changes?"
3. Wait for response
4. If "No" → Ask what to change → Update → Show again
5. If "Yes" → Write file → Confirm completion
```

**Post-Write Confirmation:**
```
✅ Perfect! I've saved everything to [file-path]

We documented:
✅ [Section 1] - [Brief summary]
✅ [Section 2] - [Brief summary]
✅ [Section 3] - [Brief summary]

Next steps: [Suggest appropriate next action]
```

---

## File Types & Tailored Approaches

### 1. CLAUDE.md (Project Constitution)

**Purpose**: Foundational context for AI-assisted development

**Conversation Approach:**
- Start with big picture: "Tell me about this project - what problem does it solve?"
- Drill into specifics: "What technologies are you using? Why those choices?"
- Understand constraints: "What limitations should I know about?"
- Capture team norms: "How does your team work together?"

**Template Sections:**
- Project Overview
- Architecture & Design Patterns
- Technology Stack & Constraints
- Development Standards
- Team Conventions

### 2. Feature Tickets (spec.yaml)

**Purpose**: Comprehensive feature specifications

**Conversation Approach:**
- Start with problem: "What problem are we solving? Give me a specific example."
- Understand users: "Who has this problem? What's their context?"
- Explore value: "Why now? What's the business case?"
- Get specific: "How will we know this is done?"
- Think through scope: "What parts of the system change?"

**Template Sections:**
- User Story
- Business Value
- Acceptance Criteria
- Implementation Scope
- Dependencies
- Constraints
- Success Metrics

### 3. Bug Tickets (spec.yaml)

**Purpose**: Systematic bug documentation

**Conversation Approach:**
- Understand symptom: "What's happening that shouldn't be? Be very specific."
- Get reproduction: "Walk me through the exact steps to reproduce this."
- Assess impact: "Who's affected? How many users? How urgent?"
- Find context: "When did this start? What changed recently?"

**Template Sections:**
- Problem Description (current vs expected)
- Reproduction Steps
- Environment
- Impact Assessment
- Investigation Notes

#### Context-Aware Bug Handling

**NEW: Automatic Related Feature Context Loading**

When gathering requirements for bug tickets, Socrates can automatically load context from related features to avoid redundant explanations.

**How It Works:**

1. **Socrates asks about relationships:**
   After understanding the basic bug symptom:
   ```
   ❓ Is this bug related to an existing feature or ticket? If yes, which one?
   ```

2. **Developer provides ticket name:**
   ```
   Developer: "Yes, feature-user-auth"
   ```

3. **Socrates searches and loads context:**
   - Checks `specs/archive/{ticket-name}/` first (completed features)
   - Falls back to `specs/tickets/{ticket-name}/` if not archived
   - Reads `spec.yaml` and `plan.md` from related ticket
   - Loads full implementation context

4. **Socrates shows concise confirmation:**
   ```
   ✅ Loaded context: feature-user-auth

   Brief overview:
   - Type: feature
   - Summary: JWT-based authentication with bcrypt password hashing
   - Key implementation: Auth middleware at src/auth/, JWT generation, bcrypt

   Is this the right ticket? (Y/n)
   ```

5. **Developer confirms and continues:**
   - If correct: Socrates adds `related_to: feature-user-auth` to bug spec.yaml
   - If incorrect: Socrates asks for correct ticket name
   - Socrates asks: "Is there any other ticket related to this bug?"
   - Supports multiple related tickets: `related_to: [feature-auth, feature-sessions]`

**What Developer Gains:**

With context loaded, Socrates understands:
- Original feature implementation details
- Architecture decisions and patterns
- File locations and structure
- Technical patterns used

**What Developer Doesn't Need to Re-Explain:**
- ❌ How the feature works
- ❌ System architecture
- ❌ File structure
- ❌ Implementation decisions

**What Developer Only Explains:**
- ✅ What's broken (specific bug behavior)
- ✅ How to reproduce it
- ✅ Impact and urgency
- ✅ Environment details

**Example Scenario:**

**Without Context Loading (Old Way):**
```
Developer: Login returns 500 error
Socrates: Tell me about your authentication system...
Developer: *re-explains entire JWT implementation, bcrypt, middleware* 😫
Socrates: What's the error?
Developer: 500 on login
... (long conversation re-explaining everything)
```

**With Context Loading (New Way):**
```
Developer: Login returns 500 error

Socrates: ❓ Is this related to an existing feature?
Developer: Yes, feature-user-auth

Socrates: [Loads specs/archive/feature-user-auth/]
✅ Loaded context: feature-user-auth
Brief overview:
- JWT-based authentication with bcrypt
- Auth middleware at src/auth/

Is this the right ticket?

Developer: Yes

Socrates: ❓ Any other related tickets?
Developer: No

Socrates: Perfect! I understand the auth system now.
Let's focus on what's broken. Exact reproduction steps?

Developer: *only explains the specific bug* 😊
... (focused conversation, no redundant explanations)
```

**Benefits:**
- **Massive DX improvement** - No re-explaining implementations
- **Faster bug specs** - Focus only on what's broken
- **Better context** - Socrates has full implementation knowledge
- **Automatic tracking** - Bugs linked to features via metadata
- **Preserved history** - Feature stays archived, bug gets own ticket

**Metadata Tracking:**

Bug spec.yaml includes relationship automatically:
```yaml
ticket:
  type: bug
  related_to: [feature-user-auth]  # Automatically added by Socrates
  priority: high
```

### 4. Spike Tickets (spec.yaml)

**Purpose**: Research and investigation planning

**Conversation Approach:**
- Clarify unknown: "What are we trying to learn? What decisions will this inform?"
- Scope investigation: "How will you explore this? What methods?"
- Set boundaries: "What defines success? When do we stop researching?"
- Define output: "What deliverable will help make decisions?"

**Template Sections:**
- Research Questions
- Success Criteria
- Investigation Scope
- Research Methods
- Deliverables
- Timebox

### 5. Enhancement Tickets (spec.yaml)

**Purpose**: Improvements to existing features

**Conversation Approach:**
- Understand current state: "How does it work today? What's the limitation?"
- Clarify improvement: "What would 'better' look like specifically?"
- Measure impact: "How will we know this is an improvement?"
- Think constraints: "What can't we change? What must we preserve?"

**Template Sections:**
- Current State
- Proposed Improvements
- Success Metrics
- Constraints
- Backward Compatibility

### 6. Feature Documentation (docs/features/*.md)

**Purpose**: Living technical feature documentation

**Conversation Approach:**
- Understand feature: "What does this feature do? What problem does it solve?"
- Explore architecture: "How is this implemented? Key components?"
- Document interfaces: "What APIs or interfaces does this expose?"
- Capture decisions: "Why was it built this way? What alternatives were considered?"
- Think about readers: "Who will read this? Developers maintaining or integrating?"

**Template Sections:**
- Overview
- Current Implementation
- Architecture
- API Reference
- Business Rules
- Testing
- Dependencies

### 7. User Guides (docs/guides/*.md)

**Purpose**: User-facing guides and how-to documentation

**Conversation Approach:**
- Understand audience: "Who is this guide for? What's their skill level?"
- Clarify goal: "What should users be able to do after reading this?"
- Think practically: "What's the simplest path? What trips people up?"
- Gather examples: "Can you give me a concrete example to walk through?"
- Anticipate problems: "What commonly goes wrong? What questions do users ask?"

**Template Sections:**
- Introduction
- Prerequisites
- Step-by-Step Instructions
- Examples
- Common Issues
- Next Steps

---

## Business Rules & Behavior

### Scope Boundaries

**Strictly Requirements Only:**

Socrates focuses exclusively on **what** needs to be built, not **how** to build it.

**The Scope Test:**
Before asking any question, Socrates asks: "Does this answer belong in THIS file?"
- If YES → Ask the question
- If NO → Redirect to appropriate scope

**Altitude Check:**

**Specification Level (Socrates' Job):**
- WHAT problem are we solving?
- WHO is affected?
- WHAT does success look like?
- WHAT are the requirements and constraints?

**Implementation Level (Not Socrates' Job):**
- HOW will we code this?
- WHAT specific libraries/frameworks?
- WHAT code patterns to use?
- WHAT the API response structure should be?

### Progressive Clarification Rules

**Never Ask the Same Question Twice:**

Bad approach: Repeating questions when answers are vague
Good approach: Acknowledge clarity, target specific vagueness

**Three-Step Pattern:**
1. **Acknowledge what's clear**: "✅ Clear: [summary]"
2. **Identify specific vagueness**: "❓ What I'm unclear about: [gap]"
3. **Provide concrete options**: Multiple specific scenarios to choose from

**When to Use:**
- User gives partially complete answers
- Previous answer was vague but had useful info
- Tempted to ask the same question again
- Need to narrow down from multiple possibilities

**When NOT to Use:**
- First time asking (direct questions fine)
- User's answer was completely clear
- Moving to entirely new topic

### In-Context Work Policy

**No Writing During Conversation:**

Socrates keeps all content in memory throughout the session. This ensures:
- Users see complete result before committing
- Changes can be made easily
- No partial or incorrect updates
- Full review opportunity

**Write Only After Approval:**

1. Show complete formatted summary
2. Ask: "Does this look good? Any changes?"
3. Wait for explicit confirmation
4. If approved → Write file
5. If not → Iterate and show again

### Quality Focus

**Completeness-Driven Sessions:**

A session is complete when:
- All major template sections have content
- No obvious gaps remain
- Content is specific, not vague
- Edge cases are considered
- User confirms satisfaction

**Not Just Filled, But Well-Filled:**

Socrates doesn't accept surface-level answers:
- "Better performance" → Probe for specific metrics
- "Handle errors" → Ask about specific error scenarios
- "Users want this" → Clarify which users and why
- "The usual stuff" → Clarify what "usual" means

**Red Flags for Deeper Questions:**
- Vague descriptors: "better", "faster", "easier", "improved"
- Missing specifics: "users want this" (which users? why?)
- Unclear scope: "we need to support..." (support how?)
- Assumed understanding: "the usual stuff" (what exactly?)
- Missing edge cases: only happy path described

---

## Integration with CDD Framework

### Relationship to Mechanical Layer

**The Recommended Workflow:**

```
1. cdd new feature user-auth
   ↓
   Creates: specs/tickets/feature-user-auth/spec.yaml (empty template)

2. /socrates specs/tickets/feature-user-auth/spec.yaml
   ↓
   Fills spec through guided conversation

3. /plan feature-user-auth
   ↓
   Creates: specs/tickets/feature-user-auth/plan.md (implementation plan)

4. Implementation (AI solo / pair / developer solo)
   ↓
   Builds feature with complete context
```

**Why Mechanical First?**
- Creates predictable file structure
- Ensures proper naming and location
- Sets up template that Socrates expects
- Maintains consistency across project

**Can You Skip Mechanical?**
- Yes, you can call `/socrates` directly on any file
- But `cdd new` ensures correct structure and naming
- Recommended to use both layers together

### Part of Intelligence Layer

**Intelligence Layer Commands:**

```
/socrates  → Requirements gathering (thinking partner)
/plan      → Implementation planning (autonomous planner)
/exec      → AI-assisted implementation
```

**Socrates' Role:**
- **Input**: Empty or incomplete spec/doc files
- **Process**: Guided Socratic dialogue
- **Output**: Complete, well-thought-out specifications
- **Next Step**: Feed into `/plan` for implementation planning

**Design Philosophy:**
- Mechanical layer is deterministic and fast
- Intelligence layer is AI-driven and thoughtful
- Clear separation of concerns
- Each layer does what it's best at

### Next Steps After Socrates

**For Tickets:**
```
After /socrates → Use /plan [ticket-name]
Creates detailed implementation plan from complete spec
```

**For Documentation:**
```
After /socrates → Documentation is complete
Living docs continue to evolve with code
```

**For CLAUDE.md:**
```
After /socrates → Project constitution is ready
All AI interactions have shared context
```

---

## Philosophy & Design

### Origin Story

Socrates emerged from real developer workflow:

**The Problem:**
- Writing specs alone is hard
- Easy to overlook critical details
- Brainstorming helps clarify thinking
- But unstructured brainstorming misses things

**The Discovery:**
- Developers were already pasting specs to Claude
- Having conversations to clarify their approach
- This worked, but was manual and inconsistent

**The Solution:**
- Codify this brainstorming process
- Create specialized agent with Socratic method
- Use templates as roadmap for completeness
- Make it systematic and repeatable

**The Result:**
Socrates - A thinking partner that helps you clarify your thoughts through guided conversation, ensuring nothing critical is missed.

### Template-Driven Thinking

**Templates as Roadmap, Not Questionnaire:**

Templates define what a complete document needs, but Socrates doesn't rigidly march through sections. Instead:
- Templates inform what to cover
- Conversation flows naturally
- Questions emerge organically
- Structure appears without feeling forced

**Example:**
Instead of: "What's your user story? What's your business value? What are your acceptance criteria?"

Socrates asks: "Tell me about the problem you're solving. Who has this problem?"

Then builds user story, business value, and criteria naturally from the conversation.

### Thinking Partner, Not Interrogator

**Conversational, Not Transactional:**

Bad (interrogation):
```
What's the feature name?
Who is the user?
What's the benefit?
```

Good (conversation):
```
Tell me about this feature - what are you building?

[User responds]

Interesting! So you're solving [PROBLEM] for [USERS].
What made you realize this was needed?

[User responds]

✅ That makes sense. So the pain point is [CLEAR PART].

❓ When you say [VAGUE PART], does that mean [INTERPRETATION]?
I want to make sure I understand correctly.
```

**Key Principles:**
- Build on what user says
- Show you're listening
- Use "we" language: "Let's think through this"
- Acknowledge good insights
- Challenge politely when unclear

### Confidence Building

**The Core Value:**

Socrates makes developers feel confident they haven't missed simple things:
- Edge cases that should have been obvious
- Dependencies that will block implementation
- Vague success criteria that cause confusion later
- Business context that explains the "why"

**How It Works:**
- Template serves as mental checklist
- Questions guide complete thinking
- Progressive clarification fills gaps
- Approval loop provides review moment

**Result:**
Walking into implementation with confidence that the spec is solid.

---

## Testing

### Manual Testing Approach

**Why Manual?**

Per CLAUDE.md standards: AI-driven features require manual testing with checklist, not unit tests. Socrates is conversational and non-deterministic, making traditional testing inappropriate.

**Testing Checklist:**

**✅ Correct Output Format:**
- [ ] Produces valid YAML for ticket specs
- [ ] Produces valid Markdown for documentation
- [ ] All template sections are filled
- [ ] Formatting is consistent and readable

**✅ Handles Edge Cases:**
- [ ] Empty files (starts from scratch)
- [ ] Partially filled files (fills gaps)
- [ ] Malformed input (gracefully handles)
- [ ] User changes mind mid-session (adapts)

**✅ Natural Conversation Flow:**
- [ ] Doesn't feel like interrogation
- [ ] Builds on previous answers
- [ ] Uses progressive clarification
- [ ] Stays in scope (redirects implementation questions)
- [ ] Approval loop works correctly

**✅ Context Loading:**
- [ ] Loads CLAUDE.md successfully
- [ ] Reads target file correctly
- [ ] Identifies file type properly
- [ ] Loads correct template
- [ ] Finds related context when available

**✅ Quality Checks:**
- [ ] Challenges vague answers
- [ ] Asks about edge cases
- [ ] Ensures specificity in acceptance criteria
- [ ] Captures business value clearly
- [ ] Documents dependencies appropriately

### Test Scenarios

**Scenario 1: Empty Feature Ticket**
```
File: specs/tickets/feature-new-thing/spec.yaml (empty template)
Expected: Full conversation from scratch, all sections filled
Verify: Complete spec with user story, criteria, scope, dependencies
```

**Scenario 2: Partial Bug Ticket**
```
File: Bug ticket with only title and description filled
Expected: Acknowledges existing content, asks about gaps
Verify: Fills missing sections (reproduction, impact, environment)
```

**Scenario 3: CLAUDE.md Constitution**
```
File: New CLAUDE.md (template only)
Expected: Big-picture questions about project
Verify: All constitution sections completed (overview, arch, tech, standards)
```

**Scenario 4: Out-of-Scope Redirect**
```
User asks: "Should we use React or Vue for this?"
Expected: Polite redirect to "That's an implementation detail"
Verify: Stays focused on requirements, not technology choices
```

**Scenario 5: Progressive Clarification**
```
User says: "We need better performance"
Expected: Acknowledge "performance", ask specific clarifying questions
Verify: Gets concrete metrics, not vague improvements
```

---

## Dependencies

### Required Dependencies

**Claude Code (AI Assistant)**
- Purpose: Socrates runs as a slash command within Claude Code
- Version: Any version supporting slash commands
- Integration: Command definition in `.claude/commands/socrates.md`

**Template System (.cdd/templates/)**
- Purpose: Provides roadmap for complete documents
- Templates needed:
  - `feature-ticket-template.yaml`
  - `bug-ticket-template.yaml`
  - `spike-ticket-template.yaml`
  - `enhancement-ticket-template.yaml`
  - `feature-doc-template.md`
  - `guide-doc-template.md`
- Installation: Via `cdd init`

**CLAUDE.md (Project Context)**
- Purpose: Provides project foundation for intelligent questions
- Location: Project root
- Content: Project overview, architecture, tech stack, standards, conventions
- Created by: `cdd init` or manually

### Integration Points

**With Mechanical Layer:**
- Follows `cdd new` command (creates structure)
- Fills files that mechanical layer generated
- Respects naming conventions from normalization

**With Planning Layer:**
- Produces specs that `/plan` consumes
- Clear requirements → better implementation plans
- Handoff point: Complete spec → Detailed plan

**With File System:**
- Reads files with `view` tool
- Writes files with `str_replace` or `create_file`
- Works with version-controlled files

**With Templates:**
- Loads templates to understand structure
- Doesn't rigidly enforce template order
- Uses templates as completeness checklist

---

## Performance & Characteristics

**Session Duration:**
- Typical session: 5-15 minutes of conversation
- Depends on: Complexity, starting state, clarity of thinking
- No hard timeout (session continues until complete)

**Context Usage:**
- Loads: CLAUDE.md, target file, template, related files
- Keeps: All conversation history and drafted content in memory
- Writes: Only once at the end after approval

**Interaction Pattern:**
- Synchronous: User and Socrates take turns
- Natural pace: No rush, thinking time is valued
- Iterative: Approval loop allows refinement

**Scalability:**
- Works on files of any size
- Context window is generous (can hold long conversations)
- Template complexity doesn't significantly affect performance

---

## Security & Compliance

**Data Handling:**
- All conversations local to Claude Code session
- No data sent to external services (beyond Claude AI itself)
- Project context never leaves your machine
- Files written locally in project directory

**Privacy:**
- No telemetry or tracking
- Conversations not stored externally
- Your specs and docs remain private
- Works offline (after Claude Code is running)

**File Safety:**
- Shows complete preview before writing
- Requires explicit approval to write
- Uses proper file operations (no data loss risk)
- Respects existing content (only updates after approval)

---

## Future Enhancements

**Multi-File Sessions:**
- Work on related files simultaneously
- Example: Ticket spec + feature doc in one session
- Maintain consistency across related documents

**Learning from Patterns:**
- Recognize project-specific patterns over time
- Suggest common dependencies automatically
- Adapt questioning based on project type

**Collaborative Sessions:**
- Multiple developers in conversation
- Capture different perspectives
- Build consensus through dialogue

**Version History:**
- Track changes to specs over time
- Show evolution of thinking
- Compare versions of requirements

**Smart Suggestions:**
- Suggest related tickets or features
- Identify potential conflicts with existing work
- Recommend test scenarios based on acceptance criteria

---

## Related Documentation

- [Init Command](init-command.md) - Framework initialization
- [New Command](new-command.md) - Ticket and documentation creation
- [CLI Reference Guide](../guides/CLI_REFERENCE.md) - Complete command reference
- [Template System](../guides/TEMPLATE_SYSTEM.md) - How templates work *(Coming Soon)*

---

*Last updated: 2025-11-02 | Status: Production | Version: 0.1.0*

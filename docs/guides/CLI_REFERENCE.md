# CLI Reference Guide

Complete reference for all CDD framework commands.

---

## Installation

```bash
pip install cdd
```

**Requirements:**
- Python 3.9 or higher
- Git installed and configured
- Project must be a git repository

---

## Commands

### `cdd init`

Initialize CDD framework structure in your project.

**Usage:**
```bash
cdd init [PATH] [OPTIONS]
```

**Arguments:**
- `PATH` - Target directory for initialization (defaults to current directory `.`)

**Options:**
- `--force` - Overwrite existing files (use with caution)
- `--minimal` - Create minimal structure (reserved for future use)

**Examples:**

```bash
# Initialize in current directory
cdd init

# Initialize in specific directory
cdd init /path/to/my-project

# Initialize and overwrite existing CLAUDE.md
cdd init --force
```

**What It Creates:**

```
my-project/
├── CLAUDE.md              # Project constitution template
├── specs/
│   └── tickets/           # For sprint work
│       └── .gitkeep
├── docs/
│   └── features/          # For living documentation
│       └── .gitkeep
├── .claude/
│   └── commands/          # Framework AI agents
│       ├── socrates.md
│       ├── plan.md
│       ├── exec.md
│       └── exec-auto.md
└── .cdd/
    └── templates/         # Internal templates
        ├── constitution-template.md
        ├── feature-ticket-template.yaml
        ├── bug-ticket-template.yaml
        ├── spike-ticket-template.yaml
        ├── feature-plan-template.md
        ├── bug-plan-template.md
        ├── spike-plan-template.md
        └── feature-doc-template.md
```

**Requirements:**
- Must be run inside a git repository
- Requires write permissions
- Cannot initialize in system directories (/, /usr, /etc, etc.)

**Behavior:**
- If run in git subdirectory → uses git root
- If files exist → skips existing (unless `--force`)
- Running multiple times is safe (idempotent)

**Next Steps After Init:**
1. Edit `CLAUDE.md` with your project details
2. Create your first ticket: `cdd new feature feature-name`
3. Use `/socrates` in Claude Code to fill out the spec
4. Generate plan: `/plan feature-name`
5. Implement: `/exec feature-name`

---

### `cdd new`

Create a new ticket with structured specification.

**Usage:**
```bash
cdd new <TYPE> <NAME>
```

**Arguments:**
- `TYPE` - Ticket type: `feature`, `bug`, or `spike`
- `NAME` - Ticket name (will be auto-normalized to lowercase-with-dashes)

**Examples:**

```bash
# Create a feature ticket
cdd new feature user-authentication

# Create a bug ticket
cdd new bug "Mobile Login Issue"

# Create a spike (research) ticket
cdd new spike oauth-provider-research
```

**Name Normalization:**

The ticket name is automatically normalized:
- `"User Authentication"` → `user-authentication`
- `"Mobile Login Issue"` → `mobile-login-issue`
- `API_Performance` → `api-performance`

**What It Creates:**

```
specs/tickets/
└── {type}-{name}/
    └── spec.yaml          # Populated template
```

**Templates by Type:**

**Feature Template:**
```yaml
ticket:
  type: "feature"
  title: "[Title]"

user_story: |
  As a [user type],
  I want [capability],
  So that [benefit].

business_value: |
  [Why this feature matters]

acceptance_criteria:
  - "[Criterion 1]"
  - "[Criterion 2]"

implementation_scope:
  frontend:
    - "[Frontend change]"
  backend:
    - "[Backend change]"

# ... more fields
```

**Bug Template:**
```yaml
ticket:
  type: "bug"
  severity: "[critical/high/medium/low]"
  title: "[Title]"

problem_description: |
  [What's broken]

steps_to_reproduce:
  - "[Step 1]"
  - "[Step 2]"

expected_behavior: "[What should happen]"
actual_behavior: "[What actually happens]"

# ... more fields
```

**Spike Template:**
```yaml
ticket:
  type: "spike"
  title: "[Title]"
  timebox: "[Time limit]"

research_questions:
  - "[Question 1]"
  - "[Question 2]"

success_criteria:
  - "[What makes this spike successful]"

# ... more fields
```

**Next Steps After Creating Ticket:**
1. Open Claude Code in your project
2. Run `/socrates` to fill out the spec through conversation
3. Generate implementation plan: `/plan {ticket-name}`
4. Start implementing: `/exec {ticket-name}`

**Error Handling:**
- If ticket folder exists → prompts to overwrite or choose different name
- If templates missing → suggests running `cdd init`
- If not in git repository → shows error

---

## Claude Code Commands

These commands are used inside Claude Code after initialization.

### `/socrates`

Interactive requirements gathering assistant.

**Purpose:** Transform scattered thoughts into comprehensive specifications through guided conversation.

**Usage:**
```
/socrates
```

**How It Works:**
1. Detects which spec file you're working on
2. Loads the appropriate template structure
3. Asks intelligent, context-aware questions
4. Structures your answers into proper YAML format
5. Saves progress iteratively
6. Ensures completeness before finishing

**Example Conversation:**
```
You: /socrates

Socrates: I'll help you create a comprehensive spec for 'feature-user-authentication'.

What problem are you trying to solve?

You: Users can't access their private data

Socrates: What kind of private data? Who are these users?

You: It's a SaaS tool. Users create private projects and tasks.

Socrates: Perfect! So you need authentication to separate user data.
What authentication method feels right for your users?

[Conversation continues until spec is complete]
```

**Learn More:** [SOCRATES_GUIDE.md](SOCRATES_GUIDE.md)

---

### `/plan`

Generate detailed implementation plan from spec.

**Purpose:** AI reads your spec and project context to create step-by-step implementation plans.

**Usage:**
```
/plan {ticket-name}
```

**Examples:**
```
/plan feature-user-authentication
/plan bug-mobile-login
/plan spike-oauth-research
```

**What It Does:**
1. Loads `specs/tickets/{ticket-name}/spec.yaml`
2. Loads `CLAUDE.md` for project context
3. Searches `docs/features/` for related documentation
4. Generates detailed implementation plan
5. Saves to `specs/tickets/{ticket-name}/plan.md`

**Plan Output Includes:**
- Executive summary
- Prerequisites and setup
- Step-by-step execution plan with time estimates
- Risk assessment and mitigation strategies
- Testing strategy
- Definition of done

**Best Practices:**
- Run after completing spec with `/socrates`
- Review and adjust plan before implementation
- Use plan as guide during `/exec`

---

### `/exec`

AI-driven code implementation from plan.

**Purpose:** Execute implementation with full project context - interactive mode.

**Usage:**
```
/exec {ticket-name}
```

**Examples:**
```
/exec feature-user-authentication
/exec bug-mobile-login
```

**What It Does:**
1. Loads spec.yaml (requirements)
2. Loads plan.md (execution strategy)
3. Loads CLAUDE.md (project context)
4. Implements code step-by-step
5. Runs formatting (Black) and linting (Ruff)
6. Warns on test failures
7. Asks for guidance when blocked

**Interactive Features:**
- Prompts when decisions need input
- Shows progress through TodoWrite
- Asks about test failures
- Can pause and resume

**Alternative:** Use `/exec-auto` for fully automatic execution (no prompts).

---

### `/exec-auto`

Fully automatic AI implementation (no user interaction).

**Purpose:** Hands-free code implementation from plan.

**Usage:**
```
/exec-auto {ticket-name}
```

**Differences from `/exec`:**
- Never prompts for input
- Continues on errors (best effort)
- Logs all issues to progress.yaml
- Attempts auto-fixes for dependencies

**Use When:**
- Plan is very detailed and unambiguous
- Prefer unattended execution
- Will review output afterward

---

## Workflow Examples

### Complete Feature Development

```bash
# 1. Create ticket
cdd new feature user-authentication

# 2. Gather requirements (in Claude Code)
/socrates

# 3. Generate plan
/plan feature-user-authentication

# 4. Implement
/exec feature-user-authentication

# 5. Living docs update automatically
# docs/features/authentication.md created
```

### Fix a Bug

```bash
# 1. Create bug ticket
cdd new bug mobile-login-issue

# 2. Document bug (in Claude Code)
/socrates

# 3. Plan the fix
/plan bug-mobile-login-issue

# 4. Implement fix
/exec bug-mobile-login-issue
```

### Research Spike

```bash
# 1. Create spike ticket
cdd new spike oauth-provider-comparison

# 2. Define research scope (in Claude Code)
/socrates

# 3. Plan research approach
/plan spike-oauth-provider-comparison

# 4. Execute research
/exec spike-oauth-provider-comparison
```

---

## Tips & Best Practices

### Before You Start

1. **Initialize Once Per Project**
   ```bash
   cd my-project
   git init  # If not already a git repo
   cdd init
   ```

2. **Fill Out CLAUDE.md**
   - Add your architecture patterns
   - Document tech stack
   - Define development standards
   - This is loaded by AI in every session

3. **Use Descriptive Ticket Names**
   ```bash
   # Good
   cdd new feature user-oauth-authentication

   # Less Clear
   cdd new feature auth
   ```

### During Development

1. **Complete Specs Before Planning**
   - Use `/socrates` to fill specs thoroughly
   - Don't skip edge cases and constraints
   - Better specs = better plans

2. **Review Plans Before Execution**
   - Plans are generated autonomously
   - Review for any project-specific adjustments
   - Refine if needed before `/exec`

3. **Keep CLAUDE.md Updated**
   - Update when architecture changes
   - Add new patterns as they emerge
   - Remove outdated information

### After Completion

1. **Update Living Docs** *(Coming Soon)*
   - `/complete` command will automate this
   - For now, manually update `docs/features/`

2. **Archive Completed Tickets** *(Coming Soon)*
   - Move from `specs/tickets/` to `specs/archive/`

---

## Troubleshooting

### `cdd init` Errors

**"Not a git repository"**
```bash
# Solution: Initialize git first
git init
cdd init
```

**"No write permission"**
```bash
# Solution: Check directory permissions
ls -la
chmod u+w .
```

**"Refusing to initialize in system directory"**
```bash
# Solution: Don't run in /, /usr, /etc, or home
cd /path/to/actual/project
cdd init
```

### `cdd new` Errors

**"Template not found"**
```bash
# Solution: Run cdd init first
cdd init
cdd new feature my-feature
```

**"Ticket already exists"**
```bash
# Options:
# 1. Choose different name
# 2. Type 'y' to overwrite
# 3. Type 'cancel' to abort
```

### Claude Code Command Errors

**"/socrates not found"**
- Solution: Ensure you're in a CDD-initialized project
- Check `.claude/commands/socrates.md` exists

**"Cannot load spec.yaml"**
- Solution: Create ticket first with `cdd new`
- Ensure you're in the correct directory

---

## Getting Help

- **GitHub Issues:** https://github.com/guilhermegouw/context-driven-documentation/issues
- **Documentation:** [docs/guides/](.)
- **Examples:** [docs/examples/](../examples/)

---

*Last Updated: 2025-11-01*

# Getting Started with CDD

Welcome to Context-Driven Documentation (CDD) - the AI-first development framework that makes human-AI collaboration feel natural, powerful, and productive.

This guide will walk you through your first end-to-end feature development workflow using CDD.

---

## What You'll Learn

By the end of this guide, you'll know how to:

1. ✅ Initialize CDD in your project
2. ✅ Create your project constitution (CLAUDE.md)
3. ✅ Build comprehensive specs through conversation with Socrates
4. ✅ Generate detailed implementation plans autonomously
5. ✅ Execute implementations with full project context
6. ✅ Keep living documentation synchronized

**Time Required:** 30-45 minutes for your first complete workflow

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** installed
- **Git** installed and configured
- **Claude Code** installed and set up
- A **git repository** for your project (existing or new)

**Quick checks:**
```bash
python --version  # Should show 3.9 or higher
git --version     # Should show git version
```

---

## Step 1: Install CDD

Install CDD using pip:

```bash
pip install cdd-claude
```

Verify installation:

```bash
cdd --version
```

You should see the CDD version number.

---

## Step 2: Initialize Your Project

Navigate to your project directory and initialize CDD:

```bash
cd /path/to/your/project
cdd init
```

**What just happened?**

CDD created a complete framework structure:

```
your-project/
├── CLAUDE.md              # Your project's constitution (start here!)
├── specs/
│   └── tickets/           # Where sprint work will live
├── docs/
│   ├── features/          # Living feature documentation
│   └── guides/            # User guides
├── .claude/
│   └── commands/          # AI agents (socrates, plan, exec, sync-docs)
└── .cdd/
    └── templates/         # Internal templates
```

**Important files created:**
- `CLAUDE.md` - Project constitution that AI reads automatically
- `.claude/commands/` - Slash commands for AI agents
- `specs/tickets/` - Where your work tickets will live
- `docs/` - Living documentation

---

## Step 3: Create Your Project Constitution

The `CLAUDE.md` file is your project's constitution - it provides foundational context that AI assistants load automatically in every session.

**Open CLAUDE.md** and you'll see a template with sections like:

- **Project Overview** - What you're building and why
- **Architecture & Design Patterns** - How your system is structured
- **Technology Stack** - Languages, frameworks, versions
- **Development Standards** - Code style, testing requirements
- **Team Conventions** - Branching, commits, workflow

### Option 1: Fill It Out Manually

Edit `CLAUDE.md` directly and fill in your project details.

### Option 2: Use Socrates (Recommended!)

Let Socrates help you complete it through conversation:

**In Claude Code:**
```
/socrates CLAUDE.md
```

**Example conversation:**
```
Socrates: I'll help you complete your project constitution.
Tell me about this project - what are you building?

You: A task management API for teams

Socrates: Task management - interesting! Who are the teams?
Are we talking about small startups or enterprise organizations?

You: Small to medium sized development teams, mostly tech companies

Socrates: Perfect! So developers are the users. What tech stack
are you using for this API?

[Conversation continues, building complete context]
```

**Why this matters:** Once `CLAUDE.md` is complete, AI assistants will understand your project fundamentals in every conversation - no more re-explaining your architecture every time!

---

## Step 4: Create Your First Feature Ticket

Let's build a real feature using CDD's full workflow.

**Create a feature ticket:**

```bash
cdd new feature user-authentication
```

**What was created:**

```
specs/tickets/feature-user-authentication/
└── spec.yaml
```

The `spec.yaml` file contains a structured template for documenting your feature requirements.

---

## Step 5: Have a Conversation with Socrates

Now comes the magic - instead of manually filling out a form, have a natural conversation with Socrates to build your specification.

**In Claude Code:**
```
/socrates feature-user-authentication
```

**What to expect:**

Socrates will guide you through understanding your feature by asking intelligent questions:

```
Socrates: I'll help you create a comprehensive spec for user-authentication.

What problem are you trying to solve?

You: Users need to log in to access their data

Socrates: What kind of data are we protecting? Why can't it be public?

You: Personal task lists and project information

Socrates: So it's a privacy concern - users shouldn't see each other's tasks.
What authentication method feels right for your users? Social login (Google, GitHub)?
Email/password? Something else?

You: Email and password, keep it simple

Socrates: Simple is good for MVP! Let's think about edge cases:
- What happens when a user forgets their password?
- Should there be rate limiting on login attempts?
- What about session management - how long should users stay logged in?

[Conversation continues, building complete requirements]
```

**At the end**, Socrates shows you a complete summary and asks for approval before saving:

```
Great! Let me show you everything we've covered:

User Story:
As a task management user,
I want to securely log in with email and password,
So that my tasks and projects remain private.

Acceptance Criteria:
- Users can create account with email and password
- Password must be at least 8 characters
- Failed login attempts are rate limited (5 attempts per 15 minutes)
- Password reset via email
- Sessions last 7 days
- Secure password hashing (bcrypt)

Does this look good? Should I save it?
```

**Type 'yes' and Socrates saves your spec!**

---

## Step 6: Generate an Implementation Plan

Now that you have a complete spec, generate a detailed implementation plan.

**In Claude Code:**
```
/plan feature-user-authentication
```

**What happens:**

1. Plan reads your `spec.yaml` (requirements)
2. Plan reads your `CLAUDE.md` (project context)
3. Plan searches `docs/features/` for related documentation
4. Plan generates a detailed, step-by-step implementation strategy

**What you get:**

A `plan.md` file in your ticket folder with:

```markdown
# Implementation Plan: User Authentication

## Executive Summary
Implementation of email/password authentication with rate limiting,
password reset, and session management.

**Estimated Effort:** 6-8 hours
**Complexity:** Medium
**Risk Level:** Low

## Prerequisites
- Database schema for users and sessions
- Email service configured (SMTP or SendGrid)
- bcrypt library installed

## Step-by-Step Execution

### Phase 1: Database Setup (1-2 hours)
1. Create users table (id, email, password_hash, created_at)
2. Create sessions table (token, user_id, expires_at)
3. Add indexes for performance

### Phase 2: Authentication Core (2-3 hours)
4. Implement password hashing with bcrypt
5. Create registration endpoint POST /api/auth/register
6. Create login endpoint POST /api/auth/login
7. Implement rate limiting (5 attempts per 15 min)

### Phase 3: Session Management (1-2 hours)
8. Generate secure session tokens
9. Implement session validation middleware
10. Create logout endpoint POST /api/auth/logout

### Phase 4: Password Reset (2-3 hours)
11. Create password reset request endpoint
12. Generate secure reset tokens
13. Send reset emails
14. Create password reset confirmation endpoint

## Risk Assessment
- **Medium Risk:** Email delivery failures
  Mitigation: Queue emails, implement retry logic

## Testing Strategy
- Unit tests for password hashing
- Integration tests for each endpoint
- Security tests for rate limiting
- End-to-end authentication flow test

## Definition of Done
✅ All acceptance criteria met
✅ Tests passing (>80% coverage)
✅ Code formatted (Black) and linted (Ruff)
✅ Security review complete
✅ Documentation updated
```

**Review the plan** - it's generated autonomously but you can refine it before implementation.

---

## Step 7: Implement with Full Context

Time to build! The `/exec` command implements your feature with complete project context.

**In Claude Code:**
```
/exec feature-user-authentication
```

**What happens:**

1. Exec loads your spec.yaml (requirements)
2. Exec loads your plan.md (execution strategy)
3. Exec loads your CLAUDE.md (project context, architecture, patterns)
4. Exec implements code step-by-step
5. Exec runs Black (formatting) and Ruff (linting) automatically
6. Exec runs tests and warns on failures
7. Exec creates `progress.yaml` to track implementation
8. When complete, exec archives the ticket to `specs/archive/`

**Interactive vs Automatic:**

- **`/exec`** - Interactive mode, asks for guidance when blocked
- **`/exec-auto`** - Fully automatic, continues on errors (best effort)

**What you'll see:**

```
📋 Implementation: feature-user-authentication

Loading context...
✅ Loaded spec.yaml (requirements)
✅ Loaded plan.md (execution strategy)
✅ Loaded CLAUDE.md (project context)

Starting implementation...

✅ [1/14] Created users table schema
✅ [2/14] Created sessions table schema
✅ [3/14] Added database indexes
✅ [4/14] Implemented password hashing
✅ [5/14] Created registration endpoint
...

Running quality checks...
✅ Black formatting passed
✅ Ruff linting passed
⚠️  Tests: 2 warnings (non-critical)

Implementation complete!
✅ Ticket archived to specs/archive/feature-user-authentication/
```

**Files created during implementation:**
- Source code files (based on plan)
- Tests (if specified in plan)
- `progress.yaml` (tracks what was created/modified)

---

## Step 8: Sync Your Living Documentation

After implementation, update your living documentation to reflect what was actually built.

**In Claude Code:**
```
/sync-docs feature-user-authentication
```

**What happens:**

1. Sync-docs loads archived ticket context (spec, plan, progress)
2. Sync-docs reads key interface files (API routes, configs, public interfaces)
3. Sync-docs proposes specific documentation updates
4. You review and approve before changes are made

**What you'll see:**

```markdown
📚 Documentation Sync Analysis

**Ticket:** feature-user-authentication (feature)
**Archived:** 2025-11-03
**Target:** docs/features/authentication.md (new file)

Smart Verification:
✅ Read src/api/auth_routes.py (4 endpoints discovered)
✅ Read config/auth_settings.py (6 config options discovered)
⏭️  Skipped src/auth/password_utils.py (internal implementation)

📝 Proposed Documentation Updates

1. ✨ Create Section: "Overview"
   - Document feature purpose and capabilities
   - Source: spec.yaml

2. ✨ Create Section: "API Reference"
   - Document 4 endpoints: register, login, logout, password-reset
   - Source: Verified code (src/api/auth_routes.py)

3. ✨ Create Section: "Configuration"
   - Document 6 config options
   - Source: Verified code (config/auth_settings.py)

Apply these updates?
  [Y] Yes, apply all
  [E] Edit proposals
  [S] Show preview
  [N] Skip for now
```

**Choose [Y]** and sync-docs creates accurate documentation based on your actual implementation!

---

## Understanding the Complete Workflow

Here's what you just did:

```
1. cdd init                        → Framework setup
2. /socrates CLAUDE.md             → Project constitution
3. cdd new feature user-auth       → Create ticket
4. /socrates feature-user-auth     → Gather requirements (conversational)
5. /plan feature-user-auth         → Generate implementation plan
6. /exec feature-user-auth         → Implement with full context
7. /sync-docs feature-user-auth    → Update living documentation
```

**Key insight:** After initial setup, every feature follows steps 3-7. The workflow becomes muscle memory.

---

## What Makes CDD Different

### Traditional Development
```
Write ticket → Re-explain project to AI → Get code → Update docs manually → Docs go stale
```
**Problems:**
- Constant context re-explanation
- Tedious ticket creation (form-filling)
- Documentation gets out of sync
- Knowledge lives in developers' heads

### With CDD
```
Conversational spec → AI reads project context → Autonomous planning → Context-aware implementation → Docs stay synchronized
```
**Benefits:**
- Context captured once, understood forever
- Natural conversation replaces form-filling
- Living documentation stays accurate
- Knowledge is shared and accessible

---

## Next Steps

Now that you've completed your first feature, here are some things to explore:

### 1. Try Different Ticket Types

**Bug ticket:**
```bash
cdd new bug mobile-login-failure
/socrates bug-mobile-login-failure
/plan bug-mobile-login-failure
/exec bug-mobile-login-failure
```

**Research spike:**
```bash
cdd new spike oauth-provider-comparison
/socrates spike-oauth-provider-comparison
/plan spike-oauth-provider-comparison
/exec spike-oauth-provider-comparison
```

**Enhancement:**
```bash
cdd new enhancement improve-auth-security
/socrates enhancement-improve-auth-security
/plan enhancement-improve-auth-security
/exec enhancement-improve-auth-security
```

### 2. Create Documentation Directly

CDD also supports creating user guides and feature docs without the ticket workflow:

```bash
# Create a getting started guide
cdd new documentation guide getting-started
/socrates docs/guides/getting-started.md

# Create feature documentation manually
cdd new documentation feature payment-processing
/socrates docs/features/payment-processing.md
```

**Use this for:**
- User-facing guides and tutorials
- Architecture documentation
- API references
- How-to guides

### 3. Explore Advanced Features

**Review existing specs:**
```
/socrates feature-existing-feature
```
Socrates focuses on gaps in existing documentation.

**Refine plans before execution:**
```
/plan feature-name
# Review plan.md, make edits
/exec feature-name  # Uses your refined plan
```

**Preview documentation updates:**
```
/sync-docs feature-name
# Choose [S] to see detailed preview before applying
```

### 4. Keep CLAUDE.md Updated

As your project evolves:
- Add new architectural patterns
- Update tech stack when dependencies change
- Document new team conventions
- Remove outdated information

**Use Socrates to refine it:**
```
/socrates CLAUDE.md
```

---

## Common Patterns

### Starting Your Day

```bash
# Create ticket for today's work
cdd new feature <feature-name>

# In Claude Code
/socrates <feature-name>
/plan <feature-name>
/exec <feature-name>
/sync-docs <feature-name>
```

### Bug Fixing Workflow

```bash
# Report bug
cdd new bug <bug-name>

# Document the bug
/socrates bug-<bug-name>

# Plan the fix
/plan bug-<bug-name>

# Implement fix
/exec bug-<bug-name>
```

### Research and Spikes

```bash
# Create spike
cdd new spike <research-topic>

# Define research scope
/socrates spike-<research-topic>

# Plan investigation
/plan spike-<research-topic>

# Execute research
/exec spike-<research-topic>
```

---

## Tips for Success

### Do's ✅

1. **Complete CLAUDE.md thoroughly** - Better context = better AI assistance
2. **Have real conversations with Socrates** - Don't rush, think deeply
3. **Review plans before /exec** - Plans are autonomous but you can refine them
4. **Keep tickets focused** - One feature per ticket, break down large work
5. **Use shorthand syntax** - `/socrates feature-name` is faster than full paths
6. **Archive completed work** - `/exec` does this automatically
7. **Update living docs** - Run `/sync-docs` after implementation

### Don'ts ❌

1. **Don't skip CLAUDE.md** - It's the foundation for all AI context
2. **Don't rush Socrates conversations** - Good specs take thoughtful dialogue
3. **Don't skip plan review** - Autonomous doesn't mean blind trust
4. **Don't create massive tickets** - Break work into focused, manageable pieces
5. **Don't let docs go stale** - Use `/sync-docs` to keep them accurate
6. **Don't re-explain project context** - That's what CLAUDE.md is for!

---

## Troubleshooting

### "Not a git repository"

**Solution:**
```bash
git init
cdd init
```

### "/socrates command not found"

**Solution:**
- Ensure you're in a CDD-initialized project
- Check `.claude/commands/socrates.md` exists
- Try running `cdd init` again

### "Ticket not found"

**Solution:**
```bash
# Create the ticket first
cdd new feature <name>

# Then use slash commands
/socrates <name>
```

### "Templates not found"

**Solution:**
```bash
# Re-initialize (safe, won't overwrite existing files)
cdd init
```

### Plans seem generic

**Solution:**
- Complete CLAUDE.md with detailed project context
- Provide thorough requirements in spec.yaml via Socrates
- Add architecture patterns to CLAUDE.md that AI can follow

### Documentation updates seem off

**Solution:**
- Review proposals before applying (choose [S] to preview)
- Use [E] to edit proposals in conversational mode
- Manually refine docs after sync if needed

---

## Getting Help

**Documentation:**
- [SOCRATES_GUIDE.md](SOCRATES_GUIDE.md) - Master conversational spec creation
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Complete command reference
- Feature docs in `docs/features/` - Deep dives on each command

**Community:**
- GitHub Issues: https://github.com/guilhermegouw/context-driven-documentation/issues
- Examples: See `docs/examples/` for sample specs and workflows

---

## Quick Reference Card

```bash
# Setup (once per project)
cdd init
/socrates CLAUDE.md

# Feature development (repeat for each feature)
cdd new feature <name>
/socrates <name>
/plan <name>
/exec <name>
/sync-docs <name>

# Bug fixing
cdd new bug <name>
/socrates bug-<name>
/plan bug-<name>
/exec bug-<name>

# Documentation creation
cdd new documentation guide <name>
/socrates docs/guides/<name>.md

# Check archived work
ls specs/archive/
```

---

## What's Next?

You now have the foundation to use CDD effectively!

**Recommended reading order:**
1. ✅ **This guide** (you are here)
2. [SOCRATES_GUIDE.md](SOCRATES_GUIDE.md) - Deep dive on conversational spec creation
3. [CLI_REFERENCE.md](CLI_REFERENCE.md) - Complete command reference
4. Feature documentation in `docs/features/` - Understand each command deeply

**Try building:**
1. A simple authentication feature (like in this guide)
2. A bug fix for an existing issue
3. A research spike to evaluate a technology
4. User-facing documentation for your project

**Remember:** CDD is about making human-AI collaboration feel natural. The more you use it, the more natural it becomes.

**Happy building! 🚀**

---

*Last Updated: 2025-11-03*

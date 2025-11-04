# Context-Driven Documentation (CDD)

[![PyPI version](https://badge.fury.io/py/cdd-claude.svg)](https://pypi.org/project/cdd-claude/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-111%20passed-brightgreen.svg)](https://github.com/guilhermegouw/context-driven-documentation)

**Transform how you build software with AI pair programming**

CDD is an AI-first development framework that makes human-AI collaboration feel natural, powerful, and productive. Create meaningful specifications through conversation, generate detailed implementation plans autonomously, and let AI write high-quality code - all while maintaining perfect context across your entire project.

---

## 🎯 **What Makes CDD Different**

Traditional development with AI requires constantly re-explaining your project. CDD eliminates this friction:

- **Create meaningful specs in a conversational way** - Socrates, your intelligent documentation assistant, asks the right questions and structures your engineering thought process
- **Break down specs into actionable plans** - AI generates detailed, step-by-step implementation plans autonomously
- **Automatically generate high-quality code from plans** - Execute implementations with full project context
- **Eliminate repeated context-sharing with AI** - Capture your project's context once, AI understands it forever
- **Documentation never goes out of date** - Living documentation that evolves with your codebase

---

## 💡 **The Core Principle**

**Context captured once. AI understands forever.**

Instead of manually managing context or repeatedly explaining your project, CDD maintains a living knowledge base that provides perfect context automatically. Your AI partner knows your architecture, patterns, and conventions - making every conversation start from shared understanding instead of zero.

---

## 🧠 **The Mental Model**

```
CLAUDE.md = "My project's constitution - always loaded"
specs/    = "Current sprint work - tickets with plans"
docs/     = "Living feature documentation - stays synchronized"
AI Agents = "Intelligent assistants that know my project"
```

**The workflow:** Conversational requirements → Autonomous planning → AI implementation → Self-maintaining docs

---

## ⚡ **Quick Start**

### Installation

```bash
pip install cdd-claude
```

### Initialize Your Project

```bash
cd my-project
cdd init
```

This creates:
- `CLAUDE.md` - Your project's constitution
- `specs/tickets/` - Where your sprint work lives
- `docs/features/` and `docs/guides/` - Living documentation that stays synchronized
- Framework AI agents for intelligent collaboration

### Your First Feature (5-Step Workflow)

```bash
# 1. Create a ticket
cdd new feature user-authentication

# 2. Open in Claude Code and have a conversation with Socrates
/socrates feature-user-authentication

# Socrates asks intelligent questions:
# - "What problem are you solving?"
# - "Who are your users?"
# - "What are the acceptance criteria?"
# Your spec.yaml gets built through natural conversation

# 3. Generate an implementation plan
/plan feature-user-authentication

# AI reads your spec, understands your project (CLAUDE.md),
# and creates a detailed step-by-step plan

# 4. Implement with full context
/exec feature-user-authentication
# (Or use /exec-auto for fully automatic, hands-free implementation)

# AI writes code following your plan, architecture, and conventions

# 5. Your living docs update automatically
# docs/features/authentication.md reflects what was built
```

**That's it.** Conversational requirements → Autonomous planning → AI implementation.

### Create Documentation (Simpler Workflow)

Documentation has a simpler workflow - no spec/plan/exec phases:

```bash
# Create a guide or feature doc
cdd new documentation guide getting-started
cdd new documentation feature authentication

# Fill it with Socrates
/socrates docs/guides/getting-started.md

# Socrates helps you build comprehensive docs through conversation
# - What is this guide about?
# - Who is the audience?
# - What examples would help?
# Your documentation gets built naturally

# Keep it updated as your code evolves - it's living documentation!
```

**Key difference:** Documentation is meant to evolve continuously with your codebase. Create it once, refine it often with Socrates.

---

## 🏗️ **How It Works**

### **Directory Structure**

When you run `cdd init`, you get a simple, git-friendly structure:

```
my-project/
├── CLAUDE.md              # Project constitution (always loaded by AI)
├── specs/
│   ├── tickets/           # Active sprint work
│   │   └── feature-auth/
│   │       ├── spec.yaml  # Requirements from conversation
│   │       ├── plan.md    # AI-generated implementation plan
│   │       └── progress.yaml  # Implementation progress (created by /exec)
│   └── archive/           # Completed tickets (auto-archived by /exec)
└── docs/
    ├── features/          # Living feature documentation
    │   └── authentication.md
    └── guides/            # User guides and how-tos
        └── getting-started.md
```

### **CLAUDE.md - Your Project's Constitution**

This file is automatically loaded in every Claude Code session, providing foundational context:

```markdown
# Project Constitution

## Architecture & Patterns
- System design and core patterns
- Data flow and component relationships

## Tech Stack & Constraints
- Languages, frameworks, and versions
- Infrastructure and deployment requirements

## Development Standards
- Code style and formatting rules
- Testing requirements and conventions
```

Once you fill this out, AI knows your project fundamentals forever.

### **Specs - Structured Tickets with Plans**

Each ticket is a folder containing:

- **spec.yaml** - Requirements gathered through conversation with Socrates
- **plan.md** - Detailed implementation plan generated by AI

**Ticket types:**
- `cdd new feature` - New functionality with user stories and acceptance criteria
- `cdd new bug` - Bug reports with reproduction steps and impact assessment
- `cdd new spike` - Research tasks with questions and success criteria
- `cdd new enhancement` - Improvements to existing features

### **Docs - Living Documentation**

Feature documentation that stays synchronized with your code:

```markdown
# Feature: User Authentication

## Current Implementation
- OAuth 2.0 with Google
- Session-based auth
- JWT tokens for API access

## Technical Details
- Endpoints: /auth/google, /auth/logout
- Database: users, sessions tables
- Security: bcrypt hashing, secure cookies
```

---

## 🤖 **Meet Socrates - Your Intelligent Documentation Assistant**

Socrates transforms scattered thoughts into comprehensive specifications through guided conversation.

**Traditional approach:**
```
What's the feature name? ___
What does it do? ___
Who are the users? ___
```
*Feels like filling out a form. No intelligence.*

**Socrates approach:**
```
You: /socrates

Socrates: I'll help you create a comprehensive spec.
What problem are you trying to solve?

You: Users can't access their personal data

Socrates: What kind of personal data? Why can't it be public?
Who are these users exactly?

You: It's a SaaS project management tool. Users create private
projects and tasks.

Socrates: Perfect! So you need authentication to separate user data.
Let's think about the authentication method - what feels right
for your users?
```

**Socrates:**
- Asks the right questions based on context
- Probes deeper when answers are vague
- Suggests edge cases you might miss
- Structures your thoughts into proper spec format
- Saves progress as you go

---

## ✨ **Current Features**

### ✅ **Conversational Specification Creation**
Create comprehensive specs through natural dialogue with Socrates. No forms, no templates - just conversation that builds understanding.

### ✅ **Autonomous Implementation Planning**
AI reads your spec, understands your project architecture, and generates detailed step-by-step implementation plans with time estimates and risk assessment.

### ✅ **Context-Aware Code Generation**
Execute implementations with full project context - architecture, patterns, conventions, and business rules all automatically available.

### ✅ **Living Documentation**
Documentation that evolves with your codebase, capturing what actually exists rather than what was planned.

### ✅ **File-Based & Git-Friendly**
Everything lives in files you can version control, review, and share. No databases, no lock-in.

---

## 📍 **Current Workflow**

```
1. cdd new feature-name         → Creates ticket structure
2. /socrates feature-name       → Conversational spec creation
3. /plan feature-name           → AI generates implementation plan
4. /exec feature-name           → AI implements with full context
   (or /exec-auto for hands-free automatic implementation)
5. /sync-docs feature-name      → Sync living documentation with implementation
```

---

## 🗺️ **Roadmap**

### Coming Soon

**Skills - Auto-Activation** 📅
- Technical knowledge that activates automatically based on conversation
- Example: Mention "OAuth" → Security patterns auto-load
- Example: Mention "slow query" → Database optimization patterns auto-load

**Agents - Domain Specialists** 📅
- Independent specialists with focused expertise
- `@business-analyst` - Validate requirements and edge cases
- `@security-auditor` - Review security implications
- `@api-architect` - Design API patterns and structure

**Auto-Documentation** 📅
- `/complete` command that analyzes implementations
- Automatically updates living docs based on actual code
- Captures institutional knowledge and lessons learned

**Team Collaboration** 📅
- Shared knowledge bases across teams
- Project templates for different domains
- Team onboarding automation

---

## 🎓 **Learn More**

- **[Getting Started Guide](docs/guides/GETTING_STARTED.md)** *(Coming Soon)*
- **[Socrates Guide](docs/guides/SOCRATES_GUIDE.md)** - Master conversational spec creation
- **[Examples](docs/examples/)** - See example specs and workflows

---

## 🤝 **Contributing**

CDD is open source and welcomes contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) *(Coming Soon)* for:

- Development setup
- Architecture overview
- Contribution guidelines
- Roadmap and priorities

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details

---

## 🌟 **Why CDD?**

**Before CDD:**
```
Every conversation with AI starts from zero
→ Constantly re-explaining architecture
→ AI makes suggestions that don't fit your patterns
→ Documentation gets stale immediately
→ Context lives in developers' heads
```

**With CDD:**
```
Context captured once, understood forever
→ AI knows your project intimately
→ Suggestions align with your architecture
→ Documentation evolves automatically
→ Knowledge is shared and accessible
```

**The result:** Development teams that think faster, build better, and maintain perfect context without cognitive overhead.

---

**Transform your development workflow. Start with `pip install cdd-claude`**

*Built for the AI-first development era. Made with ❤️ by developers who believe human-AI collaboration should feel natural.*

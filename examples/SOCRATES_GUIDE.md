# Socrates: AI Requirements Gathering Specialist

## Overview

**Socrates** is an AI-powered requirements gathering specialist who uses the Socratic method to help you create comprehensive, well-structured specifications through natural conversation.

Unlike traditional form-filling tools, Socrates is an **intelligent conversation partner** - a Claude Code sub-agent that thinks WITH you, asks probing questions, and helps you discover what you're really trying to build.

## What Makes Socrates Different

### Traditional Approach ❌
```bash
$ cdd create-spec
What's the project name? _
What's the purpose? _
Who are the users? _
What's the tech stack? _
...
```
*Feels like filling out a form. Tedious. No intelligence.*

### Socrates Approach ✅
```
You: /socrates CLAUDE.md

Socrates: Hey! I see you're working on your project constitution.
Tell me about this project - what are you building?

You: A tool that helps developers give context to AI assistants

Socrates: Ah, the context problem! That's huge. When you say "give context,"
what specific pain point are you solving? What happens when context is missing?

You: Every time I start a conversation with an AI, I have to re-explain everything

Socrates: Exactly - that's exhausting! So you're building a system to capture
context once and reference it forever.

Tell me more - what specific types of context are hardest to convey repeatedly?
Is it technical details? Project history? Team conventions?

You: Mainly technical stack and architecture decisions

Socrates: Architecture decisions - those are complex. When you say "architecture,"
are we talking about high-level patterns like microservices vs monolith? Or
more detailed like how you handle state management?

[Continues probing until complete picture emerges]

[At the end:]

Great! Let me show you everything we've covered...

[Shows complete summary]

Does this look good? Should I save it?
```
*Natural conversation. Intelligent questions. Collaborative discovery.*

## How to Use Socrates

### Starting a Conversation

Socrates works with any CDD file type. Just invoke the slash command with a file path:

```bash
# Complete your project constitution
/socrates CLAUDE.md

# Create a feature specification
/socrates specs/tickets/user-auth/spec.yaml

# Document a bug
/socrates specs/tickets/safari-login-bug/spec.yaml

# Plan a research spike
/socrates specs/tickets/performance-investigation/spec.yaml
```

### What to Expect

**1. Socrates Reads the File**
- Checks what's already documented
- Identifies gaps and missing sections
- Understands the file type and required structure

**2. Natural Conversation Begins**
- Asks thoughtful, probing questions
- Builds on your answers
- Challenges assumptions gently
- Helps you think through edge cases

**3. Probes Deeply**
- Asks 2-3 follow-up questions when answers are vague
- Doesn't accept surface-level responses
- Keeps digging until requirements are crystal clear

**4. Shows Complete Summary**
- Keeps everything in memory during conversation
- Shows you the COMPLETE result at the end
- Gets your approval before writing anything

**5. Saves Only After Approval**
- You review the full specification
- Make any final changes
- Confirm, and then Socrates saves it

## File Types Socrates Handles

### 1. CLAUDE.md (Project Constitution)

**Purpose:** Foundational context for your entire project

**What Socrates Helps With:**
- Project overview and purpose
- Technology stack and constraints
- Architecture and design patterns
- Development standards
- Team conventions

**Example Session:**
```
You: /socrates CLAUDE.md

Socrates: I see you're working on your project constitution.
Tell me about this project - what are you building?

You: An API for managing customer subscriptions

Socrates: Subscriptions - so billing, recurring payments, that whole space.
Who's using this API? Is it internal microservices or external partners?

[Conversation continues, building complete context]
```

### 2. Feature Tickets (specs/tickets/**/spec.yaml)

**Purpose:** Comprehensive feature specifications

**What Socrates Helps With:**
- User stories with clear value
- Business justification
- Acceptance criteria
- Implementation scope
- Technical considerations

**Example Session:**
```
You: /socrates specs/tickets/export-data/spec.yaml

Socrates: New feature ticket! What problem are we solving?

You: Users need to export their data to CSV

Socrates: Export functionality - makes sense. When you say "their data,"
what specific data are we talking about? All of it, or specific subsets?

You: All their transaction history

Socrates: Got it. And who are these users? Are they power users who need
this daily, or is it more of an occasional "backup my data" need?

[Continues exploring the feature deeply]
```

### 3. Bug Tickets (specs/tickets/**/spec.yaml)

**Purpose:** Systematic bug investigation and documentation

**What Socrates Helps With:**
- Clear problem description
- Reproduction steps
- Impact assessment
- Environment details

**Example Session:**
```
You: /socrates specs/tickets/login-fails-safari/spec.yaml

Socrates: Bug ticket - let's investigate this properly.
What's happening that shouldn't be?

You: Login form doesn't work in Safari

Socrates: Okay, "doesn't work" - let's get specific. What exactly happens?
Error message? Silent failure? Infinite spinner?

You: It submits but nothing happens, no error

Socrates: Silent failure - those are the worst. Can you walk me through
the exact steps to reproduce this? Starting from...?

[Methodically gathers reproduction details]
```

### 4. Spike Tickets (specs/tickets/**/spec.yaml)

**Purpose:** Research and investigation planning

**What Socrates Helps With:**
- Research questions
- Investigation methodology
- Success criteria
- Time boundaries

**Example Session:**
```
You: /socrates specs/tickets/caching-strategy/spec.yaml

Socrates: Research spike! What are we trying to learn?

You: Whether we should use Redis or Memcached for caching

Socrates: Classic choice. What's driving this decision now?
Performance issues? Scaling concerns? New feature needs?

You: We're seeing slow response times on the API

Socrates: So performance is the driver. When you say "slow,"
what are we talking about? Current vs. target response times?

[Helps scope the investigation properly]
```

## The Socratic Method

Socrates doesn't just collect information - he helps you **think through problems**:

### Exploring Problem Space
- "What pain point are you solving?"
- "Who experiences this problem?"
- "What happens if we don't solve this?"

### Probing Deeper
- "Why is that important?"
- "Can you give me an example?"
- "What about when...?"

### Uncovering Assumptions
- "When you say X, do you mean Y?"
- "Have you considered...?"
- "What if the user does Z instead?"

### Connecting to Value
- "How does this help the business?"
- "What's the measurable impact?"
- "Who benefits most from this?"

### Thinking Through Implementation
- "What parts of the system change?"
- "What are the technical risks?"
- "What dependencies exist?"

## Best Practices

### 1. Have a Conversation, Don't Recite Facts

**Bad:**
```
You: The project is called MyApp. It's written in Python.
It uses Django. The users are businesses. It does reporting.
```

**Good:**
```
You: We're building a reporting tool for businesses

Socrates: Reporting - what kind of reports are we talking about?

You: Financial reports mostly - P&L, balance sheets, cash flow

Socrates: So accounting-focused. Are these businesses using
external accounting software, or is this standalone?

You: They're using QuickBooks and Xero, we need to integrate

[Natural back-and-forth reveals details]
```

### 2. Think Out Loud

Socrates asks good questions when you share your thinking:

```
You: I'm not sure if we should build this as a real-time feature
or batch process it overnight

Socrates: Good question! Let's think through both. What drives
that decision? User expectations? System load? Data freshness needs?
```

### 3. Ask Questions Back

Socrates is here to help you think:

```
You: Should we support OAuth or just email/password?

Socrates: Great question to consider! What's your user base like?
Are they technical users who'd expect social login? Enterprise
users who need SSO? Let's think about their workflow...
```

### 4. Build Incrementally

Don't try to complete everything in one session:

```
You: Let's focus on the user story today, I'll come back
for acceptance criteria later

Socrates: Perfect! Let's nail down the user story first.
You can always run /socrates again to add more...
```

## Tips for Great Sessions

✅ **Start with the problem** - Not the solution
✅ **Be specific** - Give examples, not abstractions
✅ **Expect follow-up questions** - Socrates will probe when answers are vague
✅ **Share context** - Mention constraints, history, concerns
✅ **Challenge yourself** - If Socrates asks "why?", dig deep
✅ **Review the summary** - Read the complete spec before approving

❌ **Don't rush** - Good specs take thoughtful conversation
❌ **Don't give vague answers** - Socrates will ask 2-3 follow-ups
❌ **Don't just list facts** - Engage in actual dialogue
❌ **Don't skip the review** - Always check the final summary before saving

## Advanced Usage

### Refining Existing Specs

Already have content? Socrates focuses on gaps:

```
You: /socrates specs/tickets/existing-feature/spec.yaml

Socrates: I can see you've already documented the user story
and acceptance criteria. Nice work!

I notice the implementation scope is vague though. Let's drill
into that - what parts of the system actually change here?
```

### Multiple File Types

Use Socrates across different files to build complete context:

```
# First, establish project context
/socrates CLAUDE.md

# Then create feature specs
/socrates specs/tickets/feature-a/spec.yaml

# Document bugs as they arise
/socrates specs/tickets/bug-123/spec.yaml

# Plan research spikes
/socrates specs/tickets/spike-performance/spec.yaml
```

### Building on Previous Sessions

Socrates reads what's already there:

```
# Session 1: Basic structure
/socrates specs/tickets/auth/spec.yaml
[Create user story and acceptance criteria]

# Session 2: Technical details
/socrates specs/tickets/auth/spec.yaml
[Add implementation scope and technical considerations]

# Session 3: Final refinement
/socrates specs/tickets/auth/spec.yaml
[Review and polish everything]
```

## What Makes Socrates Special

### 1. **AI Intelligence**
Not scripted questions - genuine AI conversation that adapts to your answers

### 2. **Socratic Method**
Asks questions that make you think deeper, not just collect surface info

### 3. **Context Awareness**
Reads templates, existing files, and your project structure

### 4. **Smart Approval Flow**
Shows complete summary before saving - you review and approve first

### 5. **Natural Language**
Conversational, warm, collaborative - not robotic or interrogative

### 6. **Extensible**
Built on Claude Code slash commands - easy to create more AI personas

## Troubleshooting

**Q: Socrates isn't asking questions, just saying "got it"**
A: You might have given very complete information. Try being more vague initially to trigger questions.

**Q: The conversation ended too quickly**
A: Run `/socrates [file]` again - it'll pick up where it left off and probe gaps.

**Q: Socrates is asking about things I already documented**
A: Make sure the file is saved. Socrates reads the current file state each time.

**Q: I want to undo something Socrates wrote**
A: Just edit the file directly or use git to revert. Files are yours to control.

**Q: Can I use Socrates on non-CDD files?**
A: Currently it's optimized for CLAUDE.md and spec.yaml files. More file types coming!

## Next Steps

Now that you understand Socrates:

1. **Try it on CLAUDE.md** - Build your project constitution
2. **Create a feature spec** - Practice the conversation flow
3. **Document a real bug** - See how Socrates helps investigate
4. **Compare before/after** - Notice how much better specs are with conversation

---

**Remember: Socrates is a thought partner, not a form to fill out.**

Have real conversations. Think deeply. Build better specifications. 🧠

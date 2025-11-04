# Feature: Sync-Docs Command

> Living documentation synchronization from archived implementations

**Status:** Production
**Version:** 0.1.0
**Last Updated:** 2025-11-03

---

## Overview

The `/sync-docs` command is an intelligent documentation analyst that keeps feature documentation in sync with implementations through smart analysis and human approval. After implementing a feature with `/exec`, sync-docs analyzes what was built, verifies actual code, and proposes targeted documentation updates.

**Why it exists:**

Traditional documentation goes stale because updating docs is a manual, tedious process requiring developers to remember what changed and manually synchronize documentation. Sync-docs solves this by automatically analyzing archived ticket implementations, reading key interface files, and proposing specific documentation updates - all while requiring human approval before making changes.

**Key Capabilities:**
- Loads complete context from archived tickets (spec, plan, progress)
- Smart code verification - reads API routes, configs, public interfaces
- Proposes specific, targeted documentation updates (not vague rewrites)
- Human approval workflow before applying changes
- Conversational refinement of proposals
- Handles discrepancies between planned and actual implementation

**Philosophy:**

Documentation should reflect what was actually built, not what was planned. Sync-docs bridges the gap between implementation reality and documentation by verifying code, comparing to plans, and proposing accurate updates that keep living docs synchronized with actual implementations.

---

## Current Implementation

### How It Works Today

**User Perspective:**
1. Complete implementation with `/exec feature-name` (ticket gets archived)
2. Run `/sync-docs feature-name` to analyze the implementation
3. Review AI-proposed documentation updates
4. Choose to apply, edit, preview, or skip
5. Documentation automatically updated to reflect actual implementation

**Core Behavior:**
- **Automatic Context Loading**: Reads spec.yaml, plan.md, and progress.yaml from archived tickets
- **Smart Verification**: Selectively reads public interface files (APIs, configs) while skipping internal implementation
- **Targeted Proposals**: Proposes specific section updates with reasoning, not wholesale rewrites
- **Human-in-the-Loop**: Always requires approval before making changes
- **Conversational Refinement**: Can discuss and refine proposals through Socratic dialogue

### Architecture Overview

**CDD Framework Integration:**
```
User implements feature → /exec archives ticket → /sync-docs analyzes
                                                          ↓
                                    Loads archived context (spec/plan/progress)
                                                          ↓
                                    Verifies implementation (reads key files)
                                                          ↓
                                    Proposes updates → User approves → Docs updated
```

**Component Structure:**
- **Path Resolution**: Handles both shorthand (`feature-name`) and full paths (`specs/archive/feature-name/`)
- **Context Loader**: Reads spec.yaml, plan.md, progress.yaml from archived tickets
- **Smart Verifier**: Filters files by interface patterns, reads only public APIs and configs
- **Proposal Generator**: Compares plan vs code vs current docs, identifies gaps
- **Content Generator**: Creates accurate documentation from verified implementation details
- **Interactive Handler**: Manages user choices (apply/edit/preview/skip)

**Data Flow:**
```
Archived Ticket → Load Context → Verify Code → Generate Proposals
                                                       ↓
User Choice → [Y] Apply → Generate Content → Write Documentation
              [E] Edit → Socratic Dialogue → Apply Refined
              [S] Preview → Show Content → Re-prompt
              [N] Skip → Exit
```

### Key Components

**Path Resolution:**
- Accepts shorthand ticket names (`feature-auth`) or full paths (`specs/archive/feature-auth/`)
- Automatically resolves shorthand to `specs/archive/{ticket-name}/`
- Validates archived ticket exists before proceeding

**Smart Verification:**
- Reads files matching interface patterns (routes, api, config, __init__, settings)
- Skips internal implementation (utils, helpers, models, tests, migrations)
- Extracts API endpoints, configuration options, public classes
- Shows what was read vs what was skipped with reasoning

**Proposal System:**
- Compares three sources: plan (intended), code (actual), docs (current)
- Identifies gaps, staleness, and discrepancies
- Proposes specific actions: Create, Update, Add to, Verify
- Includes reasoning and source attribution for each proposal

**Human Approval Workflow:**
- [Y] Apply all - Generate and write all proposed updates
- [E] Edit - Enter conversational mode to refine proposals
- [S] Show preview - Display detailed content before applying
- [N] Skip - Exit without making changes

---

## Usage

### Basic Usage

**Sync documentation after implementing a feature:**
```bash
# In Claude Code
/sync-docs feature-user-auth
```

Sync-docs will:
1. Load archived ticket context
2. Verify implementation by reading key files
3. Propose documentation updates
4. Wait for your approval

**Using full path:**
```bash
/sync-docs specs/archive/feature-user-auth/
```

### Advanced Usage

**Preview content before applying:**
```bash
/sync-docs feature-payment-processing
# Review proposals
# Choose [S] to see detailed content preview
# Then [Y] to apply or [E] to refine
```

**Refine proposals through conversation:**
```bash
/sync-docs feature-api-endpoints
# Choose [E] for conversational editing
# Discuss each section with sync-docs
# Refine content, add examples, adjust tone
# Apply refined documentation
```

### Configuration

Sync-docs uses file pattern matching to determine which files to read for verification:

**Interface Patterns (Always Read):**
- API routes: `*routes.py`, `*api.py`, `*endpoints.py`, `*views.py`
- Public interfaces: `__init__.py`, `main.py`, `app.py`
- Configuration: `config*.py`, `settings*.py`, `*.yaml`, `*.json`, `*.toml`

**Skip Patterns (Never Read):**
- Tests: `tests/`, `*_test.py`, `test_*.py`
- Utilities: `utils/`, `helpers/`
- Models: `models.py`
- Migrations: `migrations/`

These patterns are built into sync-docs and ensure efficient, focused verification.

---

## Workflow Integration

### Position in CDD Workflow

**The Feature Implementation Flow:**

```
1. cdd new feature name           → Create ticket
2. /socrates feature-name         → Gather requirements
3. /plan feature-name             → Generate implementation plan
4. /exec feature-name             → Implement and archive
5. /sync-docs feature-name        → Update living documentation ⬅ YOU ARE HERE
```

**Workflow Integration:**
- Runs after `/exec` completes and archives the ticket
- Reads archived ticket context (preserves all implementation details)
- Updates `docs/features/` living documentation
- Completes the full cycle from requirements to documented feature

### Related Commands

**`/exec`:**
- Implements features and archives tickets to `specs/archive/`
- Creates `progress.yaml` with files created/modified
- Sync-docs reads this context to understand what was built

**`/socrates`:**
- Can help refine documentation in conversational mode
- Sync-docs uses similar Socratic approach when editing proposals

**`cdd new documentation`:**
- Creates documentation files manually
- Sync-docs updates documentation created by `/exec` implementations

---

## Command Syntax

### Invocation

```bash
/sync-docs <ticket-name>
/sync-docs <full-path>
```

### Arguments

**`<ticket-name>` (shorthand):**
- Ticket name without path (e.g., `feature-user-auth`)
- Automatically resolves to `specs/archive/{ticket-name}/`
- Recommended for convenience

**`<full-path>` (explicit):**
- Full path to archived ticket directory
- Must contain `/` or end with `/` to be recognized as path
- Example: `specs/archive/feature-user-auth/`

### Examples

```bash
# Shorthand (recommended)
/sync-docs feature-authentication
/sync-docs bug-login-500
/sync-docs enhancement-cache-optimization

# Full path
/sync-docs specs/archive/feature-authentication/
/sync-docs specs/archive/bug-login-500/
```

---

## Smart Verification Details

### What Gets Read

**API Endpoints and Routes:**
```python
# Files matching: *routes.py, *api.py, *endpoints.py, *views.py
src/api/auth_routes.py          ✅ Read
src/api/payment_endpoints.py    ✅ Read
```

**Public Interfaces:**
```python
# Files: __init__.py, main.py, app.py
src/auth/__init__.py            ✅ Read
src/main.py                     ✅ Read
```

**Configuration:**
```python
# Files: config*.py, settings*.py, *.yaml, *.json, *.toml
config/auth_settings.py         ✅ Read
config.yaml                     ✅ Read
```

### What Gets Skipped

**Internal Implementation:**
```python
src/auth/jwt_handler.py         ⏭️  Skipped (internal implementation)
src/auth/password_utils.py      ⏭️  Skipped (utility)
src/models/user.py               ⏭️  Skipped (model - not API model)
```

**Tests:**
```python
tests/test_auth.py               ⏭️  Skipped (test file)
tests/auth/test_login.py         ⏭️  Skipped (test file)
```

**Verification Output Example:**
```markdown
**Smart Verification:**
✅ Read src/api/auth_routes.py (3 endpoints discovered)
✅ Read config/auth_settings.py (5 config options discovered)
✅ Read src/auth/__init__.py (2 public classes)
⏭️  Skipped src/auth/jwt_handler.py (internal implementation)
⏭️  Skipped src/auth/password.py (internal implementation)
⏭️  Skipped tests/test_auth.py (test file)

**Discovered:**
- Endpoints: POST /api/auth/login, POST /api/auth/refresh, POST /api/auth/logout
- Config: JWT_SECRET_KEY, JWT_EXPIRY, REFRESH_TOKEN_EXPIRY, SESSION_STORE, MAX_REFRESH_COUNT
- Public API: AuthMiddleware, TokenManager
```

---

## Proposal System

### Proposal Actions

**✨ Create:**
- New section needed (for new docs or missing sections)
- Example: "Create Section: API Reference"

**📝 Update:**
- Existing section has outdated content
- Example: "Update Section: Configuration (3 new options added)"

**➕ Add to:**
- Append to existing section without replacing
- Example: "Add to Section: Examples (2 new use cases)"

**⚠️  Verify:**
- Discrepancy found between plan and code
- Example: "Verify Section: Authentication Method (implementation differs from plan)"

### Proposal Format

Each proposal includes:
- **Action and Section**: What will be done and where
- **Reason**: Why this update is needed
- **Key Content**: High-level what will be added
- **Source**: Where information came from (spec, plan, code)

**Example:**
```markdown
1. ✨ Create Section: "API Reference"
   - No API documentation exists, but 3 endpoints discovered in code
   - Document POST /login, POST /refresh, POST /logout with request/response formats
   - Source: Verified code (src/api/auth_routes.py)

2. 📝 Update Section: "Configuration"
   - Current docs list 3 options, verified code has 5 options
   - Add JWT_EXPIRY and MAX_REFRESH_COUNT documentation
   - Source: Verified code (config/auth_settings.py)
```

---

## Special Cases

### Bug and Spike Tickets

**Bug tickets:**
```markdown
ℹ️  This is a bug ticket.

Bug fixes typically don't need new feature documentation.
They update existing features.

Related feature: feature-user-authentication

Did you mean to sync the related feature documentation?
Run: /sync-docs feature-user-authentication
```

**Spike tickets:**
```markdown
ℹ️  This is a spike ticket.

Spike tickets are research/investigation.
They don't result in user-facing features to document.

The deliverables from this spike should inform future feature work.
```

### Discrepancies Between Plan and Code

When verification finds code differs from plan:

```markdown
⚠️  Discrepancy Detected

**Proposal 3: Verify Section "Authentication Method"**

Plan specified: JWT tokens stored in httpOnly cookies
Code implements: JWT tokens in Authorization header (Bearer)

This is a significant difference that affects how users integrate.

Should documentation reflect:
  [A] What was built (Authorization header) - Recommended
  [B] What was planned (httpOnly cookies)
  [C] Note both with explanation of why it changed
```

### Documentation Already Up-to-Date

If no updates needed:

```markdown
✅ Documentation Already in Sync

**Verification:**
- All sections present and current
- API documentation matches verified code
- Configuration matches verified settings
- Examples align with acceptance criteria

No updates needed! 📚

The living documentation is already accurate.
```

---

## Content Generation

### What Gets Documented

**✅ Include:**
- Public APIs and interfaces (endpoints, methods, classes)
- Configuration options (environment variables, settings, defaults)
- Usage examples (based on acceptance criteria)
- Architecture and design patterns (from plan)
- Dependencies and integrations
- Testing approaches

**❌ Exclude:**
- Internal implementation details (belongs in code comments)
- Code-level minutiae (obvious from reading code)
- Implementation history (use git for this)
- Speculation about future changes

### Documentation Structure

**Standard sections generated:**
1. **Overview**: What the feature does and why it exists (from spec)
2. **Current Implementation**: How it works today (from plan)
3. **API Reference**: Endpoints discovered from verified code
4. **Configuration**: Config options discovered from verified code
5. **Usage Examples**: Based on acceptance criteria
6. **Architecture**: From plan implementation approach
7. **Dependencies**: From spec and plan
8. **Testing**: From acceptance criteria

### Tone and Style

- **Clear and concise**: Get to the point quickly
- **Practical**: Focus on what developers need to know
- **Accurate**: Use verified code details
- **Structured**: Consistent formatting and organization
- **Example-driven**: Show don't tell

---

## Examples

### Example 1: Sync Documentation After Implementation

**Goal:** Update documentation after implementing user authentication feature

**Setup:**
```bash
# Feature already implemented and archived via /exec
# specs/archive/feature-user-authentication/ exists with spec/plan/progress
```

**Execution:**
```bash
/sync-docs feature-user-authentication
```

**Expected Result:**
```markdown
📚 Documentation Sync Analysis

**Ticket:** feature-user-authentication (feature)
**Archived:** 2025-11-02
**Target:** docs/features/authentication.md (new file)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Smart Verification Results:**
✅ Read 3 interface files
⏭️  Skipped 12 internal files

Discovered:
- 3 API endpoints (login, refresh, logout)
- 5 configuration options
- 2 public classes (AuthMiddleware, TokenManager)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Proposed Documentation Updates

1. ✨ Create Section: "Overview"
   - Document feature purpose and capabilities
   - Source: spec.yaml user story and business value

2. ✨ Create Section: "API Reference"
   - Document 3 authenticated endpoints with request/response
   - Source: Verified code (src/api/auth_routes.py)

3. ✨ Create Section: "Configuration"
   - Document 5 config options with defaults
   - Source: Verified code (config/auth_settings.py)

4. ✨ Create Section: "Usage Examples"
   - Login flow, token refresh, logout examples
   - Source: Acceptance criteria from spec.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Summary:** 4 sections to create

Apply these updates?
  [Y] Yes, apply all proposals
  [E] Edit proposals (Socratic conversation mode)
  [S] Show detailed content preview
  [N] Skip for now
```

### Example 2: Update Existing Documentation

**Goal:** Update existing docs after adding new configuration options

**Execution:**
```bash
/sync-docs enhancement-auth-config-options
```

**Expected Result:**
```markdown
📚 Documentation Sync Analysis

**Ticket:** enhancement-auth-config-options (enhancement)
**Target:** docs/features/authentication.md (exists)
**Current docs:** Last updated 2025-10-15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Proposed Documentation Updates

1. 📝 Update Section: "Configuration"
   - Current docs list 5 options, verified code has 8 options
   - Add SESSION_TIMEOUT, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW
   - Source: Verified code (config/auth_settings.py)

2. ➕ Add to Section: "Examples"
   - Add rate limiting configuration example
   - Source: Acceptance criteria

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Summary:** 2 sections to update

Apply these updates?
  [Y] Yes, apply all proposals
  [E] Edit proposals
  [S] Show preview
  [N] Skip for now
```

---

## Error Handling

### Ticket Not Found

```markdown
❌ Archived ticket not found: feature-user-auth

This ticket doesn't appear to be archived yet.

Check:
- Is the ticket in specs/tickets/ (still active)?
- Has implementation completed and been archived?
- Is the ticket name spelled correctly?

Run /exec feature-user-auth first to implement and archive the ticket.
```

### Missing Context Files

**If spec.yaml missing:**
```markdown
⚠️  Warning: spec.yaml not found in archived ticket
Continuing with available context from plan.md and progress.yaml
```

**If progress.yaml missing:**
```markdown
ℹ️  No progress.yaml found
Using file structure from plan.md as fallback
```

### No Interface Files to Verify

```markdown
ℹ️  No public interface files found for verification.

This ticket contains only internal implementation changes.

Documentation will be based on spec.yaml and plan.md.
Consider if user-facing documentation is needed.

Continue with documentation sync based on plan? (Y/n)
```

---

## Performance & Characteristics

**Session Duration:**
- Context loading: ~2-5 seconds
- Smart verification: ~3-10 seconds (depends on file count)
- Proposal generation: ~5-15 seconds
- Content generation (when applying): ~10-30 seconds per section

**File Reading:**
- Selectively reads only interface files (typically 3-8 files)
- Skips internal implementation (typically 80-90% of files)
- Efficient and fast compared to reading all files

**Context Usage:**
- Reads archived ticket context (spec, plan, progress)
- Reads selected interface files
- Moderate context usage (~10K-30K tokens depending on codebase size)

**Accuracy:**
- High accuracy due to code verification
- Documents what was actually built, not what was planned
- Human approval ensures quality before applying

---

## Limitations

**Current Limitations:**
1. **Pattern-based filtering**: Uses file patterns to identify interfaces - may miss unconventional file structures
2. **No multi-language support yet**: File patterns optimized for Python projects
3. **No diagram generation**: Cannot generate architecture diagrams automatically
4. **No automatic detection of stale docs**: Only syncs when explicitly invoked

**Known Issues:**
- May propose updates for internal refactors that don't affect public API
- Cannot detect when documentation should be removed (only adds/updates)

**Workarounds:**
- Review proposals before applying to filter out unnecessary updates
- Manually remove obsolete documentation sections

---

## Related Documentation

- [/exec Command](exec-command.md) - Implements features and creates context for sync-docs
- [/socrates Command](socrates.md) - Conversational spec creation
- [/plan Command](plan-command.md) - Implementation planning
- [CLI Reference](../guides/CLI_REFERENCE.md) - All CDD CLI commands

---

## Troubleshooting

### Common Issues

**Issue: Sync-docs proposes updates that aren't needed**

**Symptoms:**
- Proposals include internal implementation details
- Documentation suggestions for private functions

**Cause:**
- File pattern matching may include files that shouldn't be documented

**Solution:**
Review proposals and choose [E] to edit, then skip unnecessary sections. Pattern filtering will improve in future versions.

**Issue: Discrepancy warnings for intentional changes**

**Symptoms:**
- Sync-docs reports discrepancy between plan and code
- Implementation intentionally differs from plan

**Cause:**
- Implementation evolved during development (normal)

**Solution:**
Choose option [A] to document what was actually built. This is the recommended approach - documentation should reflect reality.

---

### FAQ

**Q: When should I run /sync-docs?**

A: Run it after `/exec` completes and archives your ticket. This ensures the implementation is done and all context is available.

**Q: Can I skip sync-docs and write documentation manually?**

A: Yes! Sync-docs is optional. You can manually create and update documentation using `/socrates` or by editing files directly.

**Q: What if I don't want all the proposed updates?**

A: Choose [E] to enter conversational mode, where you can refine, skip, or modify specific proposals before applying.

**Q: Does sync-docs overwrite my documentation automatically?**

A: No. Sync-docs always requires human approval (Y/E/S/N choice) before making any changes.

**Q: Can I sync documentation for bugs or spikes?**

A: Bug fixes typically update existing feature docs, not create new ones. Sync-docs will suggest syncing the related feature instead. Spikes don't create user-facing features, so documentation sync isn't applicable.

---

*Documentation generated using CDD Framework v0.1.0 - Last verified: 2025-11-03*

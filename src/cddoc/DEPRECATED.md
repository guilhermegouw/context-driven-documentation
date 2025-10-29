# Deprecated Code

## socrates.py and handlers/

These files were part of an initial CLI-based implementation of Socrates that used scripted prompts.

**Why Deprecated:**
The original vision for Socrates was an AI-powered conversational assistant, not a CLI questionnaire. The CLI approach didn't match the intended user experience.

**Current Implementation:**
Socrates is now implemented as a Claude Code slash command at `.claude/commands/socrates.md`.

**Files:**
- `socrates.py` - CLI entry point (deprecated)
- `handlers/` - File handlers for scripted prompts (deprecated)
  - `base_handler.py`
  - `ticket_handler.py`
  - `constitution_handler.py`

**Keeping for Reference:**
These files demonstrate:
- Handler pattern architecture
- Rich terminal UI formatting
- YAML file operations
- Template-based file generation

They may be useful for future CLI features that need similar functionality.

---
*To use Socrates, run `/socrates [file_path]` in Claude Code instead of `cdd socrates`*

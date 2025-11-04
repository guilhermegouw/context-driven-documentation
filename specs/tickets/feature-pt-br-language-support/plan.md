# Implementation Plan: PT-BR Language Support for CDD Framework

**Generated:** 2025-11-04
**Spec:** `specs/tickets/feature-pt-br-language-support/spec.yaml`
**Ticket Type:** Feature
**Estimated Effort:** 72-96 hours (9-12 days)

---

## Executive Summary

This feature enables Brazilian software engineers to use CDD Framework with complete Portuguese (PT-BR) language support. The implementation adds a two-language system (English + PT-BR) with interactive language selection during initialization, translated CLI output, Portuguese templates, and language-aware slash commands.

**Core Strategy:** Language is selected once during `cdd init` and stored in `.cdd/config.yaml`. CLI commands detect this config and output Portuguese messages. Templates are copied in the selected language only. Slash commands use prompt engineering to respond in the user's writing language while generating content using PT-BR templates.

**Key Deliverables:**
- Config system with singleton pattern for language detection
- Translation module with English and Portuguese strings
- 10+ template files fully translated to Portuguese
- Updated `cdd init` with bilingual language selection
- All CLI commands outputting translated messages
- 5 slash commands with language matching instructions
- README.pt-BR.md with complete documentation translation
- Comprehensive test suite (unit + manual testing checklist)

---

## Technical Decisions

### Decision 1: Config System - Singleton Pattern
**Choice:** Implement Config class as singleton loading `.cdd/config.yaml` once per CLI execution
**Rationale:**
- Prevents repeated file I/O operations
- Provides consistent language detection across all commands
- Simple to use from any module: `Config.get_language()`
- Thread-safe for CLI execution (single-threaded)

**Alternatives Considered:**
- Environment variable: Rejected - not project-specific, requires manual setup
- Pass language as parameter: Rejected - too invasive, requires changing all function signatures
- Re-read config.yaml each time: Rejected - inefficient, unnecessary I/O

**Implementation:**
```python
# src/cddoc/config.py
class Config:
    _instance = None
    _language = None

    @classmethod
    def get_language(cls) -> str:
        if cls._language is None:
            cls._language = cls._load_language()
        return cls._language
```

### Decision 2: Template Strategy - Copy Only Selected Language
**Choice:** During init, copy only the selected language's templates to `.cdd/templates/` (flat structure)
**Rationale:**
- Prevents AI context pollution - Claude won't see mixed-language templates
- Simpler for handlers - no language detection needed when loading templates
- Aligns with immutable language decision
- Reduces disk space (marginal but cleaner)

**Alternatives Considered:**
- Copy both languages: Rejected - risks context pollution, unnecessary complexity
- Symlink templates: Rejected - Windows compatibility issues
- Keep language subfolders in project: Rejected - requires handlers to detect language

### Decision 3: Slash Command Language Matching - Prompt Engineering
**Choice:** Add explicit language matching instructions at the top of each slash command file
**Rationale:**
- Leverages Claude's natural language understanding
- No code changes needed in Python - pure prompt engineering
- Allows flexibility - users can write in their preferred language
- Aligned with spec requirement for natural conversation flow

**Risk:** Claude may "leak" to Portuguese when reading PT-BR context files
**Mitigation:** Strong, explicit instructions; extensive manual testing
**Fallback:** If inconsistent, can force language in v2 or defer feature

**Instruction Format:**
```markdown
# LANGUAGE MATCHING RULE

CRITICAL: Always respond in the same language the user writes to you.

- If user writes in English → Respond in English
- If user writes in Portuguese → Respond in Portuguese

The language of project files (CLAUDE.md, templates, spec.yaml) does NOT determine
your conversation language. Only the user's messages determine conversation language.
```

### Decision 4: Translation System - Simple Python Modules
**Choice:** Use Python classes in `translations/en.py` and `translations/pt_br.py` with simple attribute access
**Rationale:**
- No additional dependencies (no i18n libraries)
- Type-safe with IDE autocomplete
- Fast (in-memory, no file I/O)
- Easy to maintain and extend
- Follows "simple over clever" philosophy from CLAUDE.md

**Alternatives Considered:**
- JSON/YAML files: Rejected - requires file I/O, no type safety
- gettext: Rejected - overkill for 2 languages, adds dependency
- Dict-based: Rejected - no type safety, harder to maintain

### Decision 5: Backward Compatibility - Default to English with Warning
**Choice:** Projects without `.cdd/config.yaml` default to English and show informative warning
**Rationale:**
- No breaking changes - existing projects continue working
- Educates users about new feature
- Simple fallback logic
- Allows gradual adoption

**Warning Message:**
```
⚠️  Language config not found - using English by default.
Run 'cdd init' to configure language preference.
```

### Decision 6: UTF-8 Encoding - Explicit Everywhere
**Choice:** Explicitly specify UTF-8 encoding for all file operations involving translations or templates
**Rationale:**
- Portuguese requires special characters (ç, ã, õ, á, é, etc.)
- Ensures cross-platform compatibility (Windows, Linux, macOS)
- Prevents encoding errors

**Implementation:**
```python
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

---

## File Structure

### New Files to Create

1. **`src/cddoc/config.py`**
   - Purpose: Singleton config manager for language detection
   - Key components: `Config` class with `get_language()` classmethod
   - Responsibilities: Load `.cdd/config.yaml`, cache language, provide fallback

2. **`src/cddoc/translations/__init__.py`**
   - Purpose: Translation system entry point
   - Key components: `get_translations(language)` function
   - Responsibilities: Load appropriate translation module based on language

3. **`src/cddoc/translations/en.py`**
   - Purpose: English translation strings
   - Key components: `Messages` class with all CLI strings as attributes
   - Responsibilities: Provide all English messages

4. **`src/cddoc/translations/pt_br.py`**
   - Purpose: Portuguese translation strings
   - Key components: `Messages` class with all CLI strings as attributes
   - Responsibilities: Provide all Portuguese messages

5. **`src/cddoc/templates/pt-br/constitution-template.md`**
   - Purpose: Portuguese version of CLAUDE.md template
   - Fully translated with English commands + Portuguese comments

6. **`src/cddoc/templates/pt-br/feature-ticket-template.yaml`**
   - Purpose: Portuguese version of feature ticket template
   - All fields and instructions in Portuguese

7. **`src/cddoc/templates/pt-br/bug-ticket-template.yaml`**
   - Purpose: Portuguese version of bug ticket template

8. **`src/cddoc/templates/pt-br/spike-ticket-template.yaml`**
   - Purpose: Portuguese version of spike ticket template

9. **`src/cddoc/templates/pt-br/enhancement-ticket-template.yaml`**
   - Purpose: Portuguese version of enhancement ticket template

10. **`src/cddoc/templates/pt-br/feature-plan-template.md`**
    - Purpose: Portuguese version of feature plan template

11. **`src/cddoc/templates/pt-br/bug-plan-template.md`**
    - Purpose: Portuguese version of bug plan template

12. **`src/cddoc/templates/pt-br/spike-plan-template.md`**
    - Purpose: Portuguese version of spike plan template

13. **`src/cddoc/templates/pt-br/guide-doc-template.md`**
    - Purpose: Portuguese version of guide documentation template

14. **`src/cddoc/templates/pt-br/feature-doc-template.md`**
    - Purpose: Portuguese version of feature documentation template

15. **`README.pt-BR.md`**
    - Purpose: Complete Portuguese translation of README.md
    - Cross-linked with English README

16. **`tests/test_config.py`**
    - Purpose: Unit tests for Config singleton
    - Tests: language loading, caching, fallback behavior

17. **`tests/test_translations.py`**
    - Purpose: Unit tests for translation system
    - Tests: get_translations(), message access, language switching

### Existing Files to Modify

1. **`src/cddoc/cli.py`**
   - Changes:
     - Import Config and get_translations
     - Refactor all console.print(), Panel(), Table() to use translations
     - Update help text to be translatable
   - Locations: All command functions (init, new)

2. **`src/cddoc/init.py`**
   - Changes:
     - Add language selection prompt (bilingual)
     - Create `.cdd/config.yaml` with selected language
     - Update `install_templates()` to copy only selected language
     - Refactor console output to use translations
   - Locations: `initialize_project()`, `install_templates()`, new function `prompt_language_selection()`

3. **`src/cddoc/new_ticket.py`**
   - Changes:
     - Import Config and get_translations
     - Refactor all console output to use translations
   - Locations: `create_new_ticket()`, error handling sections

4. **`.claude/commands/socrates.md`**
   - Changes: Add language matching instructions at top
   - Location: Before "# Socrates: Requirements Gathering Specialist"

5. **`.claude/commands/plan.md`**
   - Changes: Add language matching instructions at top
   - Location: Before "# Planner: Software Architect"

6. **`.claude/commands/exec.md`**
   - Changes: Add language matching instructions at top
   - Location: Before main command description

7. **`.claude/commands/exec-auto.md`**
   - Changes: Add language matching instructions at top
   - Location: Before main command description

8. **`.claude/commands/sync-docs.md`**
   - Changes: Add language matching instructions at top
   - Location: Before main command description

9. **`README.md`**
   - Changes: Add cross-reference link to README.pt-BR.md
   - Location: Top of file, after title

### Files to Reference for Patterns

1. **`src/cddoc/cli.py`**
   - Pattern: Click decorators, Rich Panel/Table usage
   - Reason: All CLI output follows this pattern

2. **`src/cddoc/init.py`**
   - Pattern: Path validation, error handling with three-part messages
   - Reason: Error handling philosophy reference

3. **`.cdd/templates/feature-ticket-template.yaml`**
   - Pattern: Template structure with comments
   - Reason: Guide for creating PT-BR versions

---

## Data Models & API Contracts

### Config File Schema

**File:** `.cdd/config.yaml`

```yaml
# CDD Framework Configuration
# Generated during: cdd init

# Language preference (immutable after init)
# Supported values: en, pt-br
language: pt-br

# Version of config schema (for future migrations)
version: 1
```

### Config Singleton Class

**File:** `src/cddoc/config.py`

```python
"""Configuration management for CDD Framework."""

from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Singleton configuration manager.

    Loads .cdd/config.yaml once per execution and caches values.
    """

    _instance: Optional['Config'] = None
    _language: Optional[str] = None
    _loaded: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_language(cls) -> str:
        """Get configured language.

        Returns:
            Language code ('en' or 'pt-br'). Defaults to 'en' if config not found.
        """
        if not cls._loaded:
            cls._language = cls._load_language()
            cls._loaded = True
        return cls._language or 'en'

    @classmethod
    def _load_language(cls) -> str:
        """Load language from .cdd/config.yaml.

        Returns:
            Language code or None if config not found.
        """
        config_path = Path('.cdd/config.yaml')

        if not config_path.exists():
            return None  # Will trigger warning in CLI

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('language', 'en')
        except Exception:
            # If config is malformed, default to English
            return 'en'

    @classmethod
    def reset(cls):
        """Reset singleton state (for testing only)."""
        cls._loaded = False
        cls._language = None
```

### Translation System Structure

**File:** `src/cddoc/translations/__init__.py`

```python
"""Translation system for CDD Framework."""

from typing import Any


def get_translations(language: str) -> Any:
    """Get translation messages for specified language.

    Args:
        language: Language code ('en' or 'pt-br')

    Returns:
        Messages class with translated strings
    """
    if language == 'pt-br':
        from .pt_br import Messages
    else:
        from .en import Messages

    return Messages()
```

**File:** `src/cddoc/translations/en.py`

```python
"""English translation strings."""


class Messages:
    """English messages for CLI output."""

    # Init command
    init_title = "🚀 Initializing Context-Driven Documentation"
    init_success = "✅ CDD Framework initialized successfully"
    init_language_prompt = "Choose language / Escolha o idioma:"
    init_language_english = "[1] English"
    init_language_portuguese = "[2] Português (PT-BR)"
    init_language_invalid = "Invalid selection. Please choose 1 or 2."

    # Config warning
    config_not_found_warning = (
        "⚠️  Language config not found - using English by default.\n"
        "Run 'cdd init' to configure language preference."
    )

    # New command
    new_ticket_created = "✅ Ticket created: {path}"
    new_ticket_error = "❌ Error creating ticket: {error}"

    # Error messages
    error_not_git = "Not a git repository"
    error_not_git_context = "CDD requires git for version control of documentation."
    error_not_git_action = "Run: git init"

    error_no_permission = "No write permission"
    error_no_permission_context = "Cannot create files in {path}"
    error_no_permission_action = "Check directory permissions"

    # Rich UI
    panel_initialization_summary = "Initialization Summary"
    table_component = "Component"
    table_status = "Status"
    status_created = "Created"
    status_exists = "Already exists"

    next_steps_title = "📚 Next Steps"
    next_step_1 = "1. Edit CLAUDE.md with your project details"
    next_step_2 = "2. Create your first ticket: cdd new feature <name>"
    next_step_3 = "3. Run /socrates to fill specifications"
```

**File:** `src/cddoc/translations/pt_br.py`

```python
"""Portuguese (PT-BR) translation strings."""


class Messages:
    """Portuguese messages for CLI output."""

    # Init command
    init_title = "🚀 Inicializando Context-Driven Documentation"
    init_success = "✅ Framework CDD inicializado com sucesso"
    init_language_prompt = "Choose language / Escolha o idioma:"
    init_language_english = "[1] English"
    init_language_portuguese = "[2] Português (PT-BR)"
    init_language_invalid = "Seleção inválida. Por favor escolha 1 ou 2."

    # Config warning
    config_not_found_warning = (
        "⚠️  Configuração de idioma não encontrada - usando inglês por padrão.\n"
        "Execute 'cdd init' para configurar preferência de idioma."
    )

    # New command
    new_ticket_created = "✅ Ticket criado: {path}"
    new_ticket_error = "❌ Erro ao criar ticket: {error}"

    # Error messages
    error_not_git = "Não é um repositório git"
    error_not_git_context = "CDD requer git para controle de versão da documentação."
    error_not_git_action = "Execute: git init"

    error_no_permission = "Sem permissão de escrita"
    error_no_permission_context = "Não é possível criar arquivos em {path}"
    error_no_permission_action = "Verifique as permissões do diretório"

    # Rich UI
    panel_initialization_summary = "Resumo da Inicialização"
    table_component = "Componente"
    table_status = "Status"
    status_created = "Criado"
    status_exists = "Já existe"

    next_steps_title = "📚 Próximos Passos"
    next_step_1 = "1. Edite CLAUDE.md com os detalhes do seu projeto"
    next_step_2 = "2. Crie seu primeiro ticket: cdd new feature <nome>"
    next_step_3 = "3. Execute /socrates para preencher especificações"
```

### Slash Command Language Matching Instruction

**Added to top of all 5 slash command files:**

```markdown
---

## LANGUAGE MATCHING RULE

**CRITICAL:** Always respond in the same language the user writes to you.

**Behavior:**
- If user writes in English → Respond in English
- If user writes in Portuguese (PT-BR) → Respond in Portuguese

**Important:** The language of project files (CLAUDE.md, templates, spec.yaml) does NOT determine your conversation language. Only the user's messages determine your response language.

**When generating file content:** Use the template language based on `.cdd/config.yaml` configuration. For example, if the project has `language: pt-br` in config, generated specs and plans will use Portuguese templates, but your conversational messages still match the user's language.

**Example:**
```
User writes: "Tell me about this feature" (English)
You respond: "Great! Let me understand..." (English)
Generated spec.yaml: Uses PT-BR template (Portuguese field names)

User writes: "Me fala sobre essa feature" (Portuguese)
You respond: "Ótimo! Deixa eu entender..." (Portuguese)
Generated spec.yaml: Uses PT-BR template (Portuguese field names)
```

---
```

---

## Implementation Steps

Execute these steps in order. Each step has a clear outcome.

### Step 1: Create Config System
**Outcome:** Config singleton loads `.cdd/config.yaml` and provides language detection

**Details:**
1. Create `src/cddoc/config.py` with Config class
2. Implement singleton pattern with classmethod `get_language()`
3. Load `.cdd/config.yaml` once and cache result
4. Return 'en' as default if config not found (None triggers warning in CLI)
5. Handle malformed YAML gracefully (default to 'en')

**Code Example:**
```python
# src/cddoc/config.py
"""Configuration management for CDD Framework."""

from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Singleton configuration manager."""

    _instance: Optional['Config'] = None
    _language: Optional[str] = None
    _loaded: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_language(cls) -> str:
        """Get configured language.

        Returns:
            Language code ('en' or 'pt-br'). Defaults to 'en' if config not found.
            Returns None if config file doesn't exist (triggers warning in CLI).
        """
        if not cls._loaded:
            cls._language = cls._load_language()
            cls._loaded = True
        return cls._language or 'en'

    @classmethod
    def _load_language(cls) -> Optional[str]:
        """Load language from .cdd/config.yaml.

        Returns:
            Language code, None if config not found, 'en' if malformed.
        """
        config_path = Path('.cdd/config.yaml')

        if not config_path.exists():
            return None  # Signals config not found (show warning)

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('language', 'en')
        except Exception:
            # Malformed YAML - default to English silently
            return 'en'

    @classmethod
    def reset(cls):
        """Reset singleton state (for testing only)."""
        cls._loaded = False
        cls._language = None
```

**Validation:**
- Import Config in Python REPL
- Call `Config.get_language()` without config → returns 'en'
- Create `.cdd/config.yaml` with `language: pt-br` → returns 'pt-br'
- Call multiple times → returns same cached value (singleton works)

---

### Step 2: Create Translation System
**Outcome:** Translation modules provide all CLI strings in English and Portuguese

**Details:**
1. Create `src/cddoc/translations/` directory
2. Create `__init__.py` with `get_translations(language)` function
3. Create `en.py` with Messages class containing all English strings
4. Create `pt_br.py` with Messages class containing all Portuguese strings
5. Audit ALL console output in existing codebase to extract strings

**Audit Process for Existing Strings:**
- Read `src/cddoc/cli.py` - extract all strings from console.print, Panel, Table
- Read `src/cddoc/init.py` - extract all console output strings
- Read `src/cddoc/new_ticket.py` - extract all console output strings
- Categorize by command (init, new, errors, Rich UI)

**Code Example:**
```python
# src/cddoc/translations/__init__.py
"""Translation system for CDD Framework."""

from typing import Any


def get_translations(language: str) -> Any:
    """Get translation messages for specified language.

    Args:
        language: Language code ('en' or 'pt-br')

    Returns:
        Messages class instance with translated strings
    """
    if language == 'pt-br':
        from .pt_br import Messages
    else:
        from .en import Messages

    return Messages()
```

**Validation:**
- Run `get_translations('en')` → returns Messages with English strings
- Run `get_translations('pt-br')` → returns Messages with Portuguese strings
- Access message attributes → no AttributeError

---

### Step 3: Translate All Templates (10 Files)
**Outcome:** Portuguese versions of all templates exist in `src/cddoc/templates/pt-br/`

**Details:**
1. Create `src/cddoc/templates/pt-br/` directory
2. Copy each template from `src/cddoc/templates/` (or `.cdd/templates/`)
3. Translate all field names, instructions, comments to Portuguese
4. Keep command examples in English, add Portuguese comments
5. Ensure UTF-8 encoding for all files

**Templates to Translate:**
1. constitution-template.md → Complete translation, English commands with PT-BR comments
2. feature-ticket-template.yaml → All fields in Portuguese
3. bug-ticket-template.yaml → All fields in Portuguese
4. spike-ticket-template.yaml → All fields in Portuguese
5. enhancement-ticket-template.yaml → All fields in Portuguese
6. feature-plan-template.md → All sections in Portuguese
7. bug-plan-template.md → All sections in Portuguese
8. spike-plan-template.md → All sections in Portuguese
9. guide-doc-template.md → All sections in Portuguese
10. feature-doc-template.md → All sections in Portuguese

**Translation Guidelines:**
- Field names: Direct translation (e.g., "title" → "titulo")
- Instructions: Full translation maintaining meaning
- Code examples: Keep code in English, translate comments
- Command examples: Keep commands English, add explanatory comments in Portuguese

**Example Translation (feature-ticket-template.yaml):**
```yaml
# Template de Ticket: Feature
# Este template mostra a estrutura que o Socrates usa para especificações de features

titulo: "[Título descritivo da feature]"

historia_usuario: |
  Como um [tipo de usuário],
  Eu quero [capacidade ou feature],
  Para que [benefício ou valor].

valor_negocio: |
  [Por que esta feature importa para o negócio]

  Impacto no Negócio: [Impacto mensurável - receita, usuários, eficiência, etc.]

criterios_aceitacao:
  - [Critério específico e testável 1]
  - [Critério específico e testável 2]
  - [Critério específico e testável 3]
  # Adicione quantos forem necessários para definir "pronto"
```

**Validation:**
- All 10 files exist in `src/cddoc/templates/pt-br/`
- Files are valid YAML/Markdown (no syntax errors)
- UTF-8 characters display correctly (ç, ã, õ, á, etc.)
- Structure matches English templates (same sections)

---

### Step 4: Update `cdd init` Command - Add Language Selection
**Outcome:** `cdd init` prompts for language choice and creates `.cdd/config.yaml`

**Details:**
1. Add `prompt_language_selection()` function to `init.py`
2. Function displays bilingual prompt using Rich
3. Force user to choose (no default)
4. Validate input (1 or 2 only)
5. Return language code ('en' or 'pt-br')
6. Create `.cdd/config.yaml` with selected language
7. Update `install_templates()` to copy only selected language templates

**Code Example:**
```python
# Add to src/cddoc/init.py

def prompt_language_selection() -> str:
    """Prompt user to select language (bilingual prompt).

    Returns:
        Language code: 'en' or 'pt-br'
    """
    console.print()
    console.print("[bold]Choose language / Escolha o idioma:[/bold]")
    console.print("  [1] English")
    console.print("  [2] Português (PT-BR)")
    console.print()

    while True:
        choice = console.input("Enter choice / Digite sua escolha [1 or 2]: ").strip()

        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'pt-br'
        else:
            console.print(
                "[red]Invalid selection / Seleção inválida. Please choose 1 or 2.[/red]"
            )


def create_config_file(target_path: Path, language: str):
    """Create .cdd/config.yaml with language preference.

    Args:
        target_path: Project root path
        language: Language code ('en' or 'pt-br')
    """
    config_dir = target_path / '.cdd'
    config_file = config_dir / 'config.yaml'

    config_content = f"""# CDD Framework Configuration
# Generated by: cdd init

# Language preference (immutable after init)
# Supported values: en, pt-br
language: {language}

# Config schema version (for future migrations)
version: 1
"""

    config_file.write_text(config_content, encoding='utf-8')


def install_templates(target_path: Path, language: str) -> List[str]:
    """Install templates in selected language.

    Args:
        target_path: Project root path
        language: Language code ('en' or 'pt-br')

    Returns:
        List of installed template filenames
    """
    # Get source templates directory from package
    package_dir = Path(__file__).parent
    source_templates = package_dir / 'templates' / language

    if not source_templates.exists():
        raise InitializationError(
            f"Templates not found for language: {language}"
        )

    # Target: .cdd/templates/ (flat structure, no language subfolder)
    target_templates = target_path / '.cdd' / 'templates'
    target_templates.mkdir(parents=True, exist_ok=True)

    installed = []

    # Copy all template files
    for template_file in source_templates.glob('*'):
        if template_file.is_file():
            target_file = target_templates / template_file.name
            shutil.copy2(template_file, target_file)
            installed.append(template_file.name)

    return installed


# Update initialize_project() to use language selection
def initialize_project(
    path: str, force: bool = False, minimal: bool = False
) -> dict:
    """Initialize CDD structure in a project.

    Args:
        path: Target directory path
        force: Overwrite existing files if True
        minimal: Skip templates if True

    Returns:
        Dictionary with initialization results
    """
    # ... existing validation code ...

    # NEW: Prompt for language selection
    language = prompt_language_selection()

    # NEW: Create config file
    create_config_file(target_path, language)

    # ... existing directory creation ...

    # UPDATED: Install templates in selected language
    if not minimal:
        installed_templates = install_templates(target_path, language)

    # ... rest of function ...
```

**Validation:**
- Run `cdd init` → see bilingual prompt
- Choose 1 → `.cdd/config.yaml` has `language: en`
- Choose 2 → `.cdd/config.yaml` has `language: pt-br`
- Only selected language templates copied to `.cdd/templates/`
- Invalid input → shows error, prompts again

---

### Step 5: Refactor CLI Commands to Use Translations
**Outcome:** All CLI output uses translation system based on config language

**Details:**
1. Import Config and get_translations at top of each file
2. Load language once at start of each command function
3. Replace all hardcoded strings with translation attributes
4. Show warning if config not found (backward compatibility)
5. Update Rich Panel, Table, console.print calls

**Files to Update:**
- `src/cddoc/cli.py` - init and new commands
- `src/cddoc/init.py` - all console output
- `src/cddoc/new_ticket.py` - all console output

**Code Example:**
```python
# src/cddoc/cli.py

from .config import Config
from .translations import get_translations

@main.command()
@click.argument("path", default=".")
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--minimal", is_flag=True, help="Create only essential structure")
def init(path, force, minimal):
    """Initialize CDD structure in a project."""
    # Load language and translations
    language = Config.get_language()
    t = get_translations(language)

    # Show warning if config not found (backward compatibility)
    if Config._language is None:
        console.print(f"[yellow]{t.config_not_found_warning}[/yellow]")
        console.print()

    console.print(
        Panel.fit(
            t.init_title,
            border_style="blue",
        )
    )

    try:
        result = initialize_project(path, force=force, minimal=minimal)

        console.print()
        _display_results(result, t)

        console.print()
        _display_next_steps(result["path"], t)

        sys.exit(0)

    except InitializationError as e:
        console.print(f"\n[red]❌ {t.error_title}:[/red] {e}")
        sys.exit(1)


def _display_results(result: dict, t):
    """Display initialization results.

    Args:
        result: Initialization results dictionary
        t: Translation messages
    """
    table = Table(title=t.panel_initialization_summary, show_header=True)
    table.add_column(t.table_component, style="cyan", width=40)
    table.add_column(t.table_status, style="green", width=20)

    # Add rows with translated status
    for item in result.get("created_dirs", []):
        table.add_row(item, t.status_created)

    # ... rest of function ...

    console.print(table)


def _display_next_steps(path: Path, t):
    """Display next steps.

    Args:
        path: Project path
        t: Translation messages
    """
    console.print(Panel.fit(
        f"[bold]{t.next_steps_title}[/bold]\n\n"
        f"{t.next_step_1}\n"
        f"{t.next_step_2}\n"
        f"{t.next_step_3}",
        border_style="blue"
    ))
```

**Translation Keys to Add (Complete List After Audit):**

After auditing all existing CLI output, the complete translation classes will include approximately 30-40 message keys covering:
- Init command: title, success, prompts, component names
- New command: success messages, error messages
- Error handling: all error types with three-part messages
- Rich UI: panel titles, table headers, status messages
- Help text: command descriptions (may need separate handling with Click)

**Validation:**
- Run `cdd init` with EN config → all messages in English
- Run `cdd init` with PT-BR config → all messages in Portuguese
- Run `cdd new feature test` → messages in configured language
- Error messages follow three-part pattern in correct language

---

### Step 6: Update Slash Commands with Language Matching
**Outcome:** All 5 slash commands respond in user's writing language

**Details:**
1. Add language matching instructions to top of each slash command file
2. Instructions are identical across all 5 files
3. Place before main command description
4. Use strong, explicit language about behavior

**Files to Update:**
- `.claude/commands/socrates.md`
- `.claude/commands/plan.md`
- `.claude/commands/exec.md`
- `.claude/commands/exec-auto.md`
- `.claude/commands/sync-docs.md`

**Code Example:**
```markdown
<!-- Add to top of each slash command file, after header comments -->

---

## LANGUAGE MATCHING RULE

**CRITICAL:** Always respond in the same language the user writes to you.

**Behavior:**
- If user writes in English → Respond in English
- If user writes in Portuguese (PT-BR) → Respond in Portuguese

**Important:** The language of project files (CLAUDE.md, templates, spec.yaml) does NOT determine your conversation language. Only the user's messages determine your response language.

**When generating file content:** Use the template language based on `.cdd/config.yaml` configuration. For example, if the project has `language: pt-br` in config, generated specs and plans will use Portuguese templates, but your conversational messages still match the user's language.

**Example:**
```
User writes: "Tell me about this feature" (English)
You respond: "Great! Let me understand..." (English)
Generated spec.yaml: Uses PT-BR template (Portuguese field names)

User writes: "Me fala sobre essa feature" (Portuguese)
You respond: "Ótimo! Deixa eu entender..." (Portuguese)
Generated spec.yaml: Uses PT-BR template (Portuguese field names)
```

---

<!-- Resume original command content below -->

# Socrates: Requirements Gathering Specialist
...
```

**Validation:**
- Manual testing required (see Testing Strategy section)
- User writes English → Claude responds English
- User writes Portuguese → Claude responds Portuguese
- Generated files use template language regardless of conversation language

---

### Step 7: Create README.pt-BR.md
**Outcome:** Complete Portuguese translation of README.md with cross-links

**Details:**
1. Copy README.md to README.pt-BR.md
2. Translate all sections completely
3. Translate command examples → keep commands in English, add Portuguese comments
4. Add cross-reference link to README.md at top
5. Add cross-reference link from README.md to README.pt-BR.md at top

**Code Example:**
```markdown
<!-- Add to top of README.md -->
# Context-Driven Documentation (CDD Framework)

> 🌐 **Português:** [Leia em Português (PT-BR)](README.pt-BR.md)

...rest of README...
```

```markdown
<!-- README.pt-BR.md -->
# Context-Driven Documentation (Framework CDD)

> 🌐 **English:** [Read in English](README.md)

## Visão Geral

O Framework CDD é um sistema completo de inteligência de engenharia que torna a colaboração humano-IA natural, poderosa e produtiva.

### Instalação

```bash
# Instalar via pip
pip install cdd-claude

# Inicializar em seu projeto
cdd init

# Criar seu primeiro ticket
cdd new feature autenticacao-usuario
```

...continue translating all sections...
```

**Validation:**
- README.pt-BR.md exists at project root
- All sections translated
- Links work (README.md ↔ README.pt-BR.md)
- Command examples clear (English commands + PT-BR explanations)
- Markdown renders correctly on GitHub

---

### Step 8: Create Comprehensive Test Suite
**Outcome:** Unit tests for deterministic features, manual testing checklist for AI features

**Details:**
1. Create `tests/test_config.py` - Config singleton tests
2. Create `tests/test_translations.py` - Translation system tests
3. Update `tests/test_init.py` - Add language selection tests
4. Create manual testing checklist document

**Unit Test Examples:**

```python
# tests/test_config.py
"""Unit tests for Config singleton."""

import pytest
from pathlib import Path
from cddoc.config import Config


def test_config_singleton():
    """Config should be a singleton."""
    config1 = Config()
    config2 = Config()
    assert config1 is config2


def test_config_get_language_no_config(tmp_path, monkeypatch):
    """Should return 'en' when no config file exists."""
    monkeypatch.chdir(tmp_path)
    Config.reset()  # Reset singleton for test

    language = Config.get_language()
    assert language == 'en'


def test_config_get_language_pt_br(tmp_path, monkeypatch):
    """Should return 'pt-br' when config specifies it."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    # Create config file
    config_dir = tmp_path / '.cdd'
    config_dir.mkdir()
    config_file = config_dir / 'config.yaml'
    config_file.write_text('language: pt-br\nversion: 1\n')

    language = Config.get_language()
    assert language == 'pt-br'


def test_config_get_language_malformed(tmp_path, monkeypatch):
    """Should default to 'en' when config is malformed."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    # Create malformed config file
    config_dir = tmp_path / '.cdd'
    config_dir.mkdir()
    config_file = config_dir / 'config.yaml'
    config_file.write_text('invalid: yaml: content: [[[')

    language = Config.get_language()
    assert language == 'en'


def test_config_caching(tmp_path, monkeypatch):
    """Should cache language value after first load."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    config_dir = tmp_path / '.cdd'
    config_dir.mkdir()
    config_file = config_dir / 'config.yaml'
    config_file.write_text('language: pt-br\nversion: 1\n')

    # First call loads
    lang1 = Config.get_language()

    # Delete config file
    config_file.unlink()

    # Second call should return cached value
    lang2 = Config.get_language()

    assert lang1 == lang2 == 'pt-br'
```

```python
# tests/test_translations.py
"""Unit tests for translation system."""

import pytest
from cddoc.translations import get_translations


def test_get_translations_english():
    """Should return English messages."""
    t = get_translations('en')
    assert hasattr(t, 'init_title')
    assert 'Initializing' in t.init_title


def test_get_translations_portuguese():
    """Should return Portuguese messages."""
    t = get_translations('pt-br')
    assert hasattr(t, 'init_title')
    assert 'Inicializando' in t.init_title


def test_translations_have_same_attributes():
    """English and Portuguese should have same attributes."""
    en = get_translations('en')
    pt = get_translations('pt-br')

    en_attrs = set(attr for attr in dir(en) if not attr.startswith('_'))
    pt_attrs = set(attr for attr in dir(pt) if not attr.startswith('_'))

    assert en_attrs == pt_attrs, "Missing translations detected"


def test_translations_format_strings():
    """Format strings should work correctly."""
    t = get_translations('en')

    # Test format string
    message = t.new_ticket_created.format(path='/path/to/ticket')
    assert '/path/to/ticket' in message
```

```python
# Add to tests/test_init.py
"""Additional tests for language selection in init."""

def test_init_creates_config_file(tmp_path):
    """Init should create .cdd/config.yaml."""
    # Mock language selection to return 'pt-br'
    # ... test implementation ...

    config_file = tmp_path / '.cdd' / 'config.yaml'
    assert config_file.exists()

    content = config_file.read_text()
    assert 'language: pt-br' in content


def test_init_installs_correct_language_templates(tmp_path):
    """Init should install only selected language templates."""
    # Mock language selection to return 'pt-br'
    # ... test implementation ...

    templates_dir = tmp_path / '.cdd' / 'templates'

    # Should have Portuguese templates
    assert (templates_dir / 'feature-ticket-template.yaml').exists()

    # Check content is in Portuguese
    content = (templates_dir / 'feature-ticket-template.yaml').read_text()
    assert 'titulo:' in content  # Portuguese field name
    assert 'title:' not in content  # English field name should not exist
```

**Manual Testing Checklist:**

Create `TESTING_CHECKLIST.md` in ticket directory:

```markdown
# Manual Testing Checklist: PT-BR Language Support

## Language Matching (Slash Commands)

### Test Scenario 1: English User, PT-BR Project
- [ ] Create project with `language: pt-br` in config
- [ ] Run `/socrates feature-test`
- [ ] Write all messages in English
- [ ] **Expected:** Claude responds in English
- [ ] **Expected:** Generated spec.yaml has Portuguese field names

### Test Scenario 2: Portuguese User, PT-BR Project
- [ ] Same project setup
- [ ] Run `/socrates feature-test`
- [ ] Write all messages in Portuguese
- [ ] **Expected:** Claude responds in Portuguese
- [ ] **Expected:** Generated spec.yaml has Portuguese field names

### Test Scenario 3: Language Switching Mid-Conversation
- [ ] Start conversation in English
- [ ] Switch to Portuguese mid-conversation
- [ ] **Expected:** Claude follows the switch
- [ ] Continue in Portuguese
- [ ] **Expected:** Claude stays in Portuguese

### Test Scenario 4: All Slash Commands
Repeat above tests for:
- [ ] `/socrates`
- [ ] `/plan`
- [ ] `/exec`
- [ ] `/exec-auto`
- [ ] `/sync-docs`

## CLI Output Translation

### Test Scenario 5: Init Command (EN)
- [ ] Delete `.cdd/config.yaml`
- [ ] Run `cdd init`
- [ ] Select English
- [ ] **Expected:** All messages in English after selection

### Test Scenario 6: Init Command (PT-BR)
- [ ] Delete `.cdd/config.yaml`
- [ ] Run `cdd init`
- [ ] Select Portuguese
- [ ] **Expected:** All messages in Portuguese after selection

### Test Scenario 7: New Command (PT-BR)
- [ ] Project with `language: pt-br`
- [ ] Run `cdd new feature test-feature`
- [ ] **Expected:** Success message in Portuguese
- [ ] **Expected:** Error messages (if any) in Portuguese

### Test Scenario 8: Backward Compatibility
- [ ] Project without `.cdd/config.yaml`
- [ ] Run `cdd new feature test`
- [ ] **Expected:** Warning message about missing config
- [ ] **Expected:** Commands work in English
- [ ] **Expected:** No crashes or errors

## UTF-8 Encoding

### Test Scenario 9: Special Characters
- [ ] Create Portuguese spec with special characters (ç, ã, õ, á, é, ê, etc.)
- [ ] Save and reopen file
- [ ] **Expected:** Characters display correctly
- [ ] **Expected:** No encoding errors

### Test Scenario 10: Cross-Platform
- [ ] Test on Linux
- [ ] Test on macOS (if available)
- [ ] Test on Windows (if available)
- [ ] **Expected:** Consistent UTF-8 handling across platforms

## Template Translation Quality

### Test Scenario 11: Template Content
- [ ] Generate ticket with PT-BR template
- [ ] Check all field names are Portuguese
- [ ] Check all instructions are Portuguese
- [ ] **Expected:** No English text except command examples
- [ ] **Expected:** Command examples have Portuguese comments

### Test Scenario 12: CLAUDE.md Translation
- [ ] Run `cdd init` with PT-BR
- [ ] Open generated CLAUDE.md
- [ ] Check all sections translated
- [ ] **Expected:** Commands in English with PT-BR explanatory comments

## Rich UI Display

### Test Scenario 13: Panels and Tables (PT-BR)
- [ ] Run `cdd init` with PT-BR
- [ ] Check initialization summary table
- [ ] **Expected:** Column headers in Portuguese
- [ ] **Expected:** Status messages in Portuguese
- [ ] **Expected:** Next steps panel in Portuguese

## Demo Workflow

### Test Scenario 14: Complete Workflow (PT-BR)
- [ ] `cdd init` → Select PT-BR
- [ ] `cdd new feature demo` → Check Portuguese output
- [ ] `/socrates feature-demo` → Write in English, check English responses
- [ ] Check generated spec.yaml → Portuguese field names
- [ ] `/plan feature-demo` → Write in English, check English responses
- [ ] Check generated plan.md → Portuguese section headers
- [ ] **Expected:** Seamless workflow, no language inconsistencies

---

## Success Criteria

**Pass Conditions:**
- ✅ Language matching works in 90%+ of test cases
- ✅ All CLI output correctly translated
- ✅ UTF-8 characters display correctly on all platforms
- ✅ No crashes or encoding errors
- ✅ Templates generate valid YAML/Markdown
- ✅ Backward compatibility maintained
- ✅ Demo workflow completes successfully in both languages

**Known Limitations:**
- Language matching is best-effort (prompt engineering, not guaranteed)
- Some context pollution may occur in edge cases
- Document any issues for future iteration
```

**Validation:**
- All unit tests pass: `pytest tests/`
- Test coverage ≥80% for new code: `pytest --cov=src/cddoc --cov-report=term`
- Manual checklist completed with documented results
- No P0/P1 bugs found during manual testing

---

## Test Cases

### Unit Tests

**Test 1: `test_config_singleton`**
```python
def test_config_singleton():
    """Config should be a singleton - same instance returned."""
    config1 = Config()
    config2 = Config()
    assert config1 is config2
```

**Test 2: `test_config_get_language_default`**
```python
def test_config_get_language_default(tmp_path, monkeypatch):
    """Should return 'en' when no config exists."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    language = Config.get_language()
    assert language == 'en'
```

**Test 3: `test_config_get_language_pt_br`**
```python
def test_config_get_language_pt_br(tmp_path, monkeypatch):
    """Should return 'pt-br' when config specifies it."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    config_dir = tmp_path / '.cdd'
    config_dir.mkdir()
    (config_dir / 'config.yaml').write_text('language: pt-br\n')

    language = Config.get_language()
    assert language == 'pt-br'
```

**Test 4: `test_config_caching`**
```python
def test_config_caching(tmp_path, monkeypatch):
    """Should cache language after first load."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    config_dir = tmp_path / '.cdd'
    config_dir.mkdir()
    config_file = config_dir / 'config.yaml'
    config_file.write_text('language: pt-br\n')

    lang1 = Config.get_language()
    config_file.unlink()  # Delete config
    lang2 = Config.get_language()  # Should still return cached value

    assert lang1 == lang2 == 'pt-br'
```

**Test 5: `test_get_translations_english`**
```python
def test_get_translations_english():
    """Should return English Messages instance."""
    t = get_translations('en')
    assert hasattr(t, 'init_title')
    assert 'Initializing' in t.init_title
```

**Test 6: `test_get_translations_portuguese`**
```python
def test_get_translations_portuguese():
    """Should return Portuguese Messages instance."""
    t = get_translations('pt-br')
    assert hasattr(t, 'init_title')
    assert 'Inicializando' in t.init_title
```

**Test 7: `test_translations_parity`**
```python
def test_translations_parity():
    """English and Portuguese should have same attributes."""
    en = get_translations('en')
    pt = get_translations('pt-br')

    en_attrs = {a for a in dir(en) if not a.startswith('_')}
    pt_attrs = {a for a in dir(pt) if not a.startswith('_')}

    assert en_attrs == pt_attrs
```

**Test 8: `test_init_creates_config`**
```python
def test_init_creates_config(tmp_path, monkeypatch):
    """Init should create .cdd/config.yaml with selected language."""
    # Test implementation with mocked language selection
    pass
```

**Test 9: `test_init_installs_correct_templates`**
```python
def test_init_installs_correct_templates(tmp_path, monkeypatch):
    """Init should install only selected language templates."""
    # Test implementation verifying PT-BR templates copied
    pass
```

**Test 10: `test_cli_uses_translations`**
```python
def test_cli_uses_translations(tmp_path, monkeypatch):
    """CLI commands should use translation system."""
    # Test implementation checking CLI output
    pass
```

### Expected Test Coverage
- Config singleton: 100% coverage
- Translation system: 100% coverage
- Template installation: 90% coverage (excluding error paths)
- CLI command updates: 80% coverage (some Rich UI hard to test)
- Overall new code: ≥80% coverage

---

## Error Handling

### Error Scenario 1: Missing Config File (Backward Compatibility)
**Trigger:** User runs commands in project without `.cdd/config.yaml`
**Error Message:**
```
⚠️  Language config not found - using English by default.
Run 'cdd init' to configure language preference.
```
**HTTP Status:** N/A (CLI)
**Recovery:** Commands execute normally in English
**User Impact:** Warning displayed once per command execution, no functionality loss

### Error Scenario 2: Malformed Config File
**Trigger:** `.cdd/config.yaml` exists but contains invalid YAML
**Error Message:** Silent fallback to English (no error shown)
**Recovery:** Commands execute normally in English
**User Impact:** No error shown, graceful degradation to English

### Error Scenario 3: Templates Not Found for Language
**Trigger:** `cdd init` attempts to install templates but `src/cddoc/templates/{language}/` doesn't exist
**Error Message:**
```
❌ Error: Templates not found for language: {language}
This is likely a package installation issue.
Try reinstalling: pip install --upgrade --force-reinstall cdd-claude
```
**Recovery:** Initialization fails, no partial state created
**User Impact:** Cannot initialize with selected language

### Error Scenario 4: UTF-8 Encoding Error
**Trigger:** File system doesn't support UTF-8 or file opened without encoding specification
**Error Message:**
```
❌ Error: Failed to read template file
Character encoding issue detected.
Ensure your system supports UTF-8 encoding.
```
**Recovery:** Operation fails, no partial changes
**User Impact:** Cannot create tickets/templates with that language

### Error Scenario 5: Invalid Language Code in Config
**Trigger:** User manually edits config.yaml and sets unsupported language (e.g., `language: fr`)
**Error Message:** Silent fallback to English
**Recovery:** Commands execute in English
**User Impact:** No error, unexpected language (English instead of intended)

### Logging Requirements
- **Info level:** Language loaded from config, template installation progress
- **Warning level:** Missing config file, fallback to English
- **Error level:** Template installation failures, file I/O errors, encoding errors

---

## Integration Points

### Integration 1: Click CLI Framework
**Connection Point:** All CLI commands via decorators
**Data Flow:** Config.get_language() → get_translations() → CLI output
**Dependencies:** Click 8.1.7+, Rich 13.x+
**Error Handling:** If translation fails, fall back to English silently

### Integration 2: Rich Terminal UI
**Connection Point:** Panel, Table, console.print calls
**Data Flow:** Translation messages → Rich formatting → terminal output
**Dependencies:** Rich library with UTF-8 support
**Error Handling:** If Rich fails to render UTF-8, display warning

### Integration 3: Template System
**Connection Point:** `install_templates()` in init.py
**Data Flow:** Language selection → Copy templates/{language}/* → .cdd/templates/
**Dependencies:** File system with UTF-8 support, shutil for file operations
**Error Handling:** If template copy fails, abort initialization

### Integration 4: Slash Commands (AI Layer)
**Connection Point:** Slash command files read by Claude
**Data Flow:** User message language → Claude response language; Config language → template selection
**Dependencies:** Claude Code, .cdd/config.yaml exists
**Error Handling:** If config not found, slash commands detect and warn user

### Integration 5: YAML Configuration
**Connection Point:** Config.get_language() reads .cdd/config.yaml
**Data Flow:** YAML file → PyYAML parser → Config singleton → CLI commands
**Dependencies:** PyYAML library
**Error Handling:** Malformed YAML → silent fallback to English

---

## Dependencies

### New Dependencies to Install
**None** - All dependencies already exist in project:
- PyYAML (existing) - For config.yaml parsing
- Rich (existing) - For terminal UI
- Click (existing) - For CLI framework
- Python 3.9+ (existing) - For type hints and pathlib

### Existing Dependencies to Leverage
- **PyYAML**: Parse `.cdd/config.yaml` for language detection
- **Rich**: Display translated messages in panels, tables, formatted output
- **Click**: CLI command framework, help text translation (may need custom handling)
- **pathlib**: Cross-platform path handling for template installation
- **shutil**: File copying operations for template installation

### Version Constraints
- Python: 3.9+ (existing requirement)
- PyYAML: 6.0+ (existing)
- Rich: 13.0+ (existing)
- Click: 8.1+ (existing)

No version changes needed - all dependencies compatible.

---

## Effort Estimation

| Activity                                  | Estimated Time | Assumptions                                                                 |
|-------------------------------------------|----------------|-----------------------------------------------------------------------------|
| **1. Config System**                      | 6-8 hours      | Simple singleton, YAML parsing straightforward                              |
| - Design and implement Config class       | 3 hours        | ~100 LOC, singleton pattern                                                 |
| - Unit tests for Config                   | 2 hours        | 5-6 test cases                                                              |
| - Integration with CLI commands           | 1-2 hours      | Import and use in 3 files                                                   |
| - Documentation                           | 0.5 hour       | Docstrings                                                                  |
|                                           |                |                                                                             |
| **2. Translation System**                 | 10-12 hours    | Need to audit all existing output, create 2 message classes                 |
| - Audit existing CLI output               | 3-4 hours      | Read cli.py, init.py, new_ticket.py, extract ~30-40 strings                 |
| - Create translations/__init__.py         | 1 hour         | ~50 LOC, simple import logic                                                |
| - Create translations/en.py               | 2 hours        | ~200-300 LOC, organize by category                                          |
| - Create translations/pt_br.py            | 3-4 hours      | Translation work, ~200-300 LOC                                              |
| - Unit tests                              | 1-2 hours      | 3-4 test cases                                                              |
| - Documentation                           | 0.5 hour       | Docstrings                                                                  |
|                                           |                |                                                                             |
| **3. Template Translation**               | 8-16 hours     | 10 files, varying complexity, Portuguese translation required               |
| - constitution-template.md                | 2-3 hours      | Large file, ~400 lines, careful translation                                 |
| - 4 ticket templates (YAML)               | 2-3 hours      | ~100 lines each, field names + instructions                                 |
| - 3 plan templates (Markdown)             | 2-4 hours      | ~300 lines each, section headers + instructions                             |
| - 2 doc templates (Markdown)              | 1-2 hours      | ~200 lines each                                                             |
| - Review and validation                   | 1-2 hours      | Check consistency, test rendering                                           |
|                                           |                |                                                                             |
| **4. Update cdd init**                    | 8 hours        | Language selection UI, config creation, template logic                      |
| - prompt_language_selection()             | 2 hours        | ~50 LOC, Rich UI for bilingual prompt                                       |
| - create_config_file()                    | 1 hour         | ~30 LOC, simple YAML generation                                             |
| - Update install_templates()              | 2 hours        | ~50 LOC, language-aware template copying                                    |
| - Refactor init output to use translations| 2 hours        | Update all console.print, Panel, Table calls                                |
| - Unit tests                              | 1 hour         | 2-3 new test cases                                                          |
|                                           |                |                                                                             |
| **5. Update CLI Commands**                | 8 hours        | Refactor cli.py, init.py, new_ticket.py                                    |
| - Import Config and translations          | 0.5 hour       | Add imports to 3 files                                                      |
| - Refactor cli.py                         | 3 hours        | Replace all hardcoded strings, ~20 locations                                |
| - Refactor init.py console output         | 1.5 hours      | ~10 locations                                                               |
| - Refactor new_ticket.py console output   | 1.5 hours      | ~10 locations                                                               |
| - Add backward compatibility warning      | 0.5 hour       | Check if config exists, show warning                                        |
| - Update tests                            | 1 hour         | Fix tests affected by refactoring                                           |
|                                           |                |                                                                             |
| **6. Update Slash Commands**              | 8-16 hours     | Add language matching to 5 files, includes manual testing risk             |
| - Add instructions to 5 slash commands    | 2 hours        | Copy/paste same instructions                                                |
| - Update template loading logic           | 1 hour         | Add language detection from config.yaml                                     |
| - Manual testing (CRITICAL)               | 5-12 hours     | Test all 14 scenarios in checklist, iterate if issues found                 |
| - Document findings                       | 0.5 hour       | Note any edge cases or limitations                                          |
|                                           |                |                                                                             |
| **7. README.pt-BR.md**                    | 4 hours        | Complete translation of README                                              |
| - Translate content                       | 3 hours        | ~500-600 lines, technical content                                           |
| - Add cross-links                         | 0.5 hour       | Links between READMEs                                                       |
| - Review and validation                   | 0.5 hour       | Check links, formatting, consistency                                        |
|                                           |                |                                                                             |
| **8. Manual Testing**                     | 16-24 hours    | Complete checklist, iterate on issues                                       |
| - Language matching tests (Scenarios 1-4) | 6-8 hours      | Most critical, requires multiple iterations likely                          |
| - CLI output tests (Scenarios 5-8)        | 3-4 hours      | Straightforward, less iteration needed                                      |
| - UTF-8 encoding tests (Scenarios 9-10)   | 2-3 hours      | Cross-platform testing                                                      |
| - Template quality tests (Scenarios 11-12)| 2-3 hours      | Verify translations, consistency                                            |
| - Rich UI tests (Scenario 13)             | 1-2 hours      | Visual verification                                                         |
| - Complete workflow test (Scenario 14)    | 2-3 hours      | End-to-end demo preparation                                                 |
| - Documentation of issues                 | 1 hour         | Write up any limitations or edge cases                                      |
|                                           |                |                                                                             |
| **Total Estimate**                        | **72-96 hours**| **9-12 days** (assuming 8-hour days)                                        |

### Key Assumptions
1. Portuguese translations done by someone fluent (not machine translated)
2. Existing test infrastructure works (pytest, fixtures, etc.)
3. No major refactoring needed beyond translation integration
4. Language matching prompt engineering works reasonably well (90%+ success rate)
5. UTF-8 encoding supported on target platforms without issues
6. Template structure remains unchanged during translation

### Risks to Estimate

**High Risk:**
- **Language matching iteration** (+8-16 hours): If prompt engineering doesn't work consistently, may need multiple iterations or alternative approach
  - Mitigation: Budget extra time for manual testing and iteration

**Medium Risk:**
- **Template translation quality** (+4-8 hours): If translations need multiple review passes or corrections
  - Mitigation: Get translations reviewed by native speaker early

- **CLI output audit incomplete** (+2-4 hours): May find additional output points not initially identified
  - Mitigation: Systematic audit with grep/search tools

**Low Risk:**
- **UTF-8 encoding issues on Windows** (+2-4 hours): Windows console encoding can be problematic
  - Mitigation: Explicit UTF-8 encoding in all file operations

- **Rich UI rendering with Portuguese** (+1-2 hours): Table/panel layouts may need adjustment
  - Mitigation: Test early, adjust column widths if needed

### Confidence Level
**Medium confidence (±30%)** due to:
- ✅ Well-defined requirements and architecture
- ✅ Familiar technology stack
- ✅ Clear implementation steps
- ⚠️  Language matching is AI-driven (unpredictable)
- ⚠️  Translation quality depends on external input
- ⚠️  Manual testing time can vary significantly

**Adjusted Estimate with Risk Buffer:** 80-112 hours (10-14 days)

---

## Definition of Done

- ✅ Config system implemented and tested (unit tests passing)
- ✅ Translation system implemented with English and Portuguese messages
- ✅ All 10 template files translated and validated
- ✅ `cdd init` prompts for language and creates config file
- ✅ All CLI commands output translated messages based on config
- ✅ All 5 slash commands have language matching instructions
- ✅ README.pt-BR.md created with cross-links
- ✅ All unit tests pass (≥80% coverage for new code)
- ✅ Manual testing checklist completed with documented results
- ✅ Language matching works in 90%+ of test scenarios
- ✅ UTF-8 characters display correctly on all tested platforms
- ✅ Backward compatibility verified (old projects work without issues)
- ✅ Code formatted with Black (no formatting errors)
- ✅ Code passes Ruff linting (no lint errors)
- ✅ Demo workflow completes successfully in both English and Portuguese
- ✅ No P0 or P1 bugs found during testing
- ✅ Documentation updated (docstrings, README cross-links)

---

*Generated by CDD Framework /plan command - Planner persona*
*Spec: `specs/tickets/feature-pt-br-language-support/spec.yaml`*

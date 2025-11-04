"""English translation strings."""


class Messages:
    """English messages for CLI output."""

    # Init command
    init_title = "🚀 [bold]Initializing Context-Driven Documentation[/bold]"
    init_success = "✅ CDD Framework initialized successfully"
    init_git_root_detected = (
        "ℹ️  Detected git repository. Using git root: {git_root}"
    )
    init_partial_exists = (
        "⚠️  CDD structure partially exists. Creating missing items only."
    )

    # Config
    config_not_found_warning = (
        "⚠️  Language config not found - using English by default.\n"
        "Run 'cdd init' to configure language preference."
    )

    # Language selection
    language_prompt = "Choose language / Escolha o idioma:"
    language_english = "[1] English"
    language_portuguese = "[2] Português (PT-BR)"
    language_invalid = (
        "Invalid selection / Seleção inválida. Please choose 1 or 2."
    )
    language_input_prompt = "Enter choice / Digite sua escolha [1 or 2]"

    # Initialization summary
    init_summary_title = "Initialization Summary"
    init_table_component = "Component"
    init_table_status = "Status"
    init_status_created = "✅ Created"
    init_status_installed = "✅ Installed"
    init_status_exists = "⚠️  Already exists"
    init_all_exists = "ℹ️  All directories and files already exist"

    # Next steps
    next_steps_title = "✅ CDD Framework Initialized"
    next_steps_content = """[bold]Your CDD Framework is Ready![/bold]

📁 Structure Created:
   • [cyan]CLAUDE.md[/cyan] - Project constitution (edit this first!)
   • [cyan]specs/tickets/[/cyan] - Active sprint work
   • [cyan]specs/archive/[/cyan] - Completed tickets (auto-archived by /exec)
   • [cyan]docs/features/[/cyan] - Living documentation
   • [cyan].claude/commands/[/cyan] - AI agents (socrates, plan, exec)
   • [cyan].cdd/templates/[/cyan] - Internal templates

🤖 [bold]Meet Socrates - Think Better, Document Faster[/bold]

Stop writing specs alone. Socrates is your thinking partner:
   ✓ Brainstorm through conversation, not forms
   ✓ Uncover edge cases before they become bugs
   ✓ Structure scattered thoughts into clear requirements
   ✓ Stay focused on what matters

Walk in with an idea. Walk out with a complete spec.

🚀 [bold]Quick Start Workflow:[/bold]

1. [yellow]Edit CLAUDE.md[/yellow] - Capture your project's context once, AI understands it forever
   Tip: Brainstorm with [green]/socrates CLAUDE.md[/green] to build it together

2. [yellow]Create a ticket:[/yellow] [green]cdd new feature user-auth[/green]
   Generates a ticket in specs/tickets/

3. [yellow]Gather requirements:[/yellow] [green]/socrates feature-user-auth[/green]
   Brainstorm with Socrates - uncover edge cases, clarify scope, build complete specs

4. [yellow]Generate plan:[/yellow] [green]/plan feature-user-auth[/green]
   Clear spec → Detailed plan → Confident implementation

5. [yellow]Implement:[/yellow] [green]/exec feature-user-auth[/green]
   Clear spec + Detailed plan = AI builds exactly what you need (not what it guesses)

📚 [bold]Learn More:[/bold]
   [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    # Ticket creation
    ticket_creating_feature = "🎫 [bold]Creating Feature Ticket[/bold]"
    ticket_creating_bug = "🎫 [bold]Creating Bug Ticket[/bold]"
    ticket_creating_spike = "🎫 [bold]Creating Spike Ticket[/bold]"
    ticket_creating_enhancement = "🎫 [bold]Creating Enhancement Ticket[/bold]"
    ticket_created_title = "🎉 Ticket Created Successfully!"
    ticket_overwritten = "Overwritten"
    ticket_created = "Created"
    ticket_exists_warning = "⚠️  Ticket already exists: {ticket_path}"
    ticket_overwrite_prompt = "Ticket already exists. Overwrite? [y/N]"
    ticket_rename_tip = "💡 Tip: Type 'cancel' or press Ctrl+C to abort"
    ticket_rename_prompt = (
        "Enter a different name for the {ticket_type} ticket"
    )
    ticket_invalid_name_error = (
        "❌ Invalid name - must contain alphanumeric characters"
    )
    ticket_cancelled = "Ticket creation cancelled by user"

    # Ticket success table
    ticket_table_title_created = "{status} Successfully"
    ticket_table_field = "Field"
    ticket_table_value = "Value"
    ticket_table_type = "Type"
    ticket_table_normalized_name = "Normalized Name"
    ticket_table_location = "Location"
    ticket_table_spec_file = "Spec File"

    # Ticket next steps
    ticket_next_steps = """[bold]Next Steps:[/bold]

1. 📝 Fill out your ticket specification:
   - In Claude Code, run: [cyan]/socrates {spec_path}[/cyan]
   - Have a natural conversation with Socrates AI
   - Your specification will be built through dialogue

2. 🎯 Generate implementation plan:
   - In Claude Code, run: [cyan]/plan {spec_path}[/cyan]
   - Planner will analyze your spec and create a detailed plan
   - Review the generated plan: [cyan]{plan_path}[/cyan]

3. 🚀 Start implementation:
   - Use the plan.md as your implementation guide
   - Claude will have full context from spec + plan
   - Build with confidence!

4. 📚 Learn more:
   - Visit [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    # Documentation creation
    doc_creating_guide = "📚 [bold]Creating Guide Documentation[/bold]"
    doc_creating_feature = "📚 [bold]Creating Feature Documentation[/bold]"
    doc_created_title = "🎉 Documentation File Created!"
    doc_exists_warning = "⚠️  Documentation already exists: {file_path}"
    doc_table_type = "Type"
    doc_table_file_name = "File Name"
    doc_table_location = "Location"
    doc_type_guide = "Guide Documentation"
    doc_type_feature = "Feature Documentation"

    # Documentation next steps
    doc_next_steps = """[bold]Next Steps:[/bold]

1. 📝 Fill out your documentation with Socrates:
   - In Claude Code, run: [cyan]/socrates {file_path}[/cyan]
   - Have a natural conversation to build comprehensive docs
   - Socrates will help you think through the structure

2. 📚 Documentation is now part of your living docs:
   - Guide docs: Help users understand and use features
   - Feature docs: Technical reference for implementation details
   - Keep it updated as the code evolves

3. 🔗 Link related documentation:
   - Cross-reference other guides and features
   - Build a knowledge network

4. 🎯 Remember the CDD philosophy:
   - Context captured once, understood forever
   - Living documentation that evolves with your code
   - AI assistants have full context automatically

[bold]Pro tip:[/bold] Use Socrates to brainstorm! Start the conversation even if you're not
sure what to write - Socrates will ask the right questions.
"""

    # Error messages
    error_title = "Error"
    error_unexpected = "Unexpected error"
    error_not_git = (
        "Not a git repository\n"
        "CDD requires git for version control of documentation.\n"
        "Run: git init"
    )
    error_git_not_found = (
        "Git not found\n"
        "CDD requires git to be installed.\n"
        "Install git: https://git-scm.com/downloads"
    )
    error_template_not_found = (
        "Template not found: {template_name}\n"
        "Templates are required for ticket creation.\n"
        "Run: cdd init"
    )
    error_doc_template_not_found = (
        "Template not found: {template_name}\n"
        "Documentation templates are required.\n"
        "Run: cdd init"
    )
    error_invalid_ticket_name = (
        "Invalid ticket name\n"
        "Name must contain at least one alphanumeric character.\n"
        "Example: cdd new feature user-authentication"
    )
    error_invalid_doc_name = (
        "Invalid documentation name\n"
        "Name must contain at least one alphanumeric character.\n"
        "Example: cdd new documentation guide getting-started"
    )
    error_dangerous_path = "Refusing to initialize in system directory: {path}"
    error_no_write_permission = "No write permission for directory: {path}"
    error_failed_to_create = "Failed to create ticket: {error}"
    error_failed_to_create_doc = "Failed to create documentation: {error}"

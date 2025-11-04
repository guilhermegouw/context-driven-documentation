"""Portuguese (PT-BR) translation strings."""


class Messages:
    """Portuguese messages for CLI output."""

    # Init command
    init_title = "🚀 [bold]Inicializando Context-Driven Documentation[/bold]"
    init_success = "✅ Framework CDD inicializado com sucesso"
    init_git_root_detected = (
        "ℹ️  Repositório git detectado. Usando raiz do git: {git_root}"
    )
    init_partial_exists = "⚠️  Estrutura CDD parcialmente existente. Criando apenas itens faltantes."

    # Config
    config_not_found_warning = (
        "⚠️  Configuração de idioma não encontrada - usando inglês por padrão.\n"
        "Execute 'cdd init' para configurar preferência de idioma."
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
    init_summary_title = "Resumo da Inicialização"
    init_table_component = "Componente"
    init_table_status = "Status"
    init_status_created = "✅ Criado"
    init_status_installed = "✅ Instalado"
    init_status_exists = "⚠️  Já existe"
    init_all_exists = "ℹ️  Todos os diretórios e arquivos já existem"

    # Next steps
    next_steps_title = "✅ Framework CDD Inicializado"
    next_steps_content = """[bold]Seu Framework CDD Está Pronto![/bold]

📁 Estrutura Criada:
   • [cyan]CLAUDE.md[/cyan] - Constituição do projeto (edite isto primeiro!)
   • [cyan]specs/tickets/[/cyan] - Trabalho ativo da sprint
   • [cyan]specs/archive/[/cyan] - Tickets concluídos (arquivados automaticamente pelo /exec)
   • [cyan]docs/features/[/cyan] - Documentação viva
   • [cyan].claude/commands/[/cyan] - Agentes de IA (socrates, plan, exec)
   • [cyan].cdd/templates/[/cyan] - Templates internos

🤖 [bold]Conheça o Socrates - Pense Melhor, Documente Mais Rápido[/bold]

Pare de escrever especificações sozinho. Socrates é seu parceiro de pensamento:
   ✓ Faça brainstorming através de conversas, não formulários
   ✓ Descubra casos extremos antes que se tornem bugs
   ✓ Estruture pensamentos dispersos em requisitos claros
   ✓ Mantenha o foco no que importa

Entre com uma ideia. Saia com uma especificação completa.

🚀 [bold]Fluxo de Início Rápido:[/bold]

1. [yellow]Edite CLAUDE.md[/yellow] - Capture o contexto do seu projeto uma vez, a IA o entende para sempre
   Dica: Faça brainstorming com [green]/socrates CLAUDE.md[/green] para construí-lo juntos

2. [yellow]Crie um ticket:[/yellow] [green]cdd new feature autenticacao-usuario[/green]
   Gera um ticket em specs/tickets/

3. [yellow]Reúna requisitos:[/yellow] [green]/socrates feature-autenticacao-usuario[/green]
   Brainstorming com Socrates - descubra casos extremos, esclareça escopo, construa specs completas

4. [yellow]Gere um plano:[/yellow] [green]/plan feature-autenticacao-usuario[/green]
   Spec clara → Plano detalhado → Implementação confiante

5. [yellow]Implemente:[/yellow] [green]/exec feature-autenticacao-usuario[/green]
   Spec clara + Plano detalhado = IA constrói exatamente o que você precisa (não o que ela supõe)

📚 [bold]Saiba Mais:[/bold]
   [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    # Ticket creation
    ticket_creating_feature = "🎫 [bold]Criando Ticket de Feature[/bold]"
    ticket_creating_bug = "🎫 [bold]Criando Ticket de Bug[/bold]"
    ticket_creating_spike = "🎫 [bold]Criando Ticket de Spike[/bold]"
    ticket_creating_enhancement = "🎫 [bold]Criando Ticket de Melhoria[/bold]"
    ticket_created_title = "🎉 Ticket Criado com Sucesso!"
    ticket_overwritten = "Sobrescrito"
    ticket_created = "Criado"
    ticket_exists_warning = "⚠️  Ticket já existe: {ticket_path}"
    ticket_overwrite_prompt = "Ticket já existe. Sobrescrever? [y/N]"
    ticket_rename_tip = (
        "💡 Dica: Digite 'cancel' ou pressione Ctrl+C para cancelar"
    )
    ticket_rename_prompt = (
        "Digite um nome diferente para o ticket de {ticket_type}"
    )
    ticket_invalid_name_error = (
        "❌ Nome inválido - deve conter caracteres alfanuméricos"
    )
    ticket_cancelled = "Criação de ticket cancelada pelo usuário"

    # Ticket success table
    ticket_table_title_created = "{status} com Sucesso"
    ticket_table_field = "Campo"
    ticket_table_value = "Valor"
    ticket_table_type = "Tipo"
    ticket_table_normalized_name = "Nome Normalizado"
    ticket_table_location = "Localização"
    ticket_table_spec_file = "Arquivo de Spec"

    # Ticket next steps
    ticket_next_steps = """[bold]Próximos Passos:[/bold]

1. 📝 Preencha a especificação do seu ticket:
   - No Claude Code, execute: [cyan]/socrates {spec_path}[/cyan]
   - Tenha uma conversa natural com a IA Socrates
   - Sua especificação será construída através de diálogo

2. 🎯 Gere o plano de implementação:
   - No Claude Code, execute: [cyan]/plan {spec_path}[/cyan]
   - O Planner analisará sua spec e criará um plano detalhado
   - Revise o plano gerado: [cyan]{plan_path}[/cyan]

3. 🚀 Inicie a implementação:
   - Use o plan.md como seu guia de implementação
   - Claude terá contexto completo da spec + plano
   - Construa com confiança!

4. 📚 Saiba mais:
   - Visite [link]https://github.com/guilhermegouw/context-driven-documentation[/link]
"""

    # Documentation creation
    doc_creating_guide = "📚 [bold]Criando Documentação de Guia[/bold]"
    doc_creating_feature = "📚 [bold]Criando Documentação de Feature[/bold]"
    doc_created_title = "🎉 Arquivo de Documentação Criado!"
    doc_exists_warning = "⚠️  Documentação já existe: {file_path}"
    doc_table_type = "Tipo"
    doc_table_file_name = "Nome do Arquivo"
    doc_table_location = "Localização"
    doc_type_guide = "Documentação de Guia"
    doc_type_feature = "Documentação de Feature"

    # Documentation next steps
    doc_next_steps = """[bold]Próximos Passos:[/bold]

1. 📝 Preencha sua documentação com Socrates:
   - No Claude Code, execute: [cyan]/socrates {file_path}[/cyan]
   - Tenha uma conversa natural para construir documentação abrangente
   - Socrates ajudará você a pensar na estrutura

2. 📚 A documentação agora faz parte dos seus docs vivos:
   - Docs de guia: Ajudam usuários a entender e usar features
   - Docs de feature: Referência técnica para detalhes de implementação
   - Mantenha atualizados conforme o código evolui

3. 🔗 Faça links entre documentações relacionadas:
   - Crie referências cruzadas entre outros guias e features
   - Construa uma rede de conhecimento

4. 🎯 Lembre-se da filosofia CDD:
   - Contexto capturado uma vez, entendido para sempre
   - Documentação viva que evolui com seu código
   - Assistentes de IA têm contexto completo automaticamente

[bold]Dica profissional:[/bold] Use Socrates para brainstorming! Inicie a conversa mesmo se você não
tiver certeza do que escrever - Socrates fará as perguntas certas.
"""

    # Error messages
    error_title = "Erro"
    error_unexpected = "Erro inesperado"
    error_not_git = (
        "Não é um repositório git\n"
        "CDD requer git para controle de versão da documentação.\n"
        "Execute: git init"
    )
    error_git_not_found = (
        "Git não encontrado\n"
        "CDD requer que o git esteja instalado.\n"
        "Instale o git: https://git-scm.com/downloads"
    )
    error_template_not_found = (
        "Template não encontrado: {template_name}\n"
        "Templates são necessários para criação de tickets.\n"
        "Execute: cdd init"
    )
    error_doc_template_not_found = (
        "Template não encontrado: {template_name}\n"
        "Templates de documentação são necessários.\n"
        "Execute: cdd init"
    )
    error_invalid_ticket_name = (
        "Nome de ticket inválido\n"
        "Nome deve conter pelo menos um caractere alfanumérico.\n"
        "Exemplo: cdd new feature autenticacao-usuario"
    )
    error_invalid_doc_name = (
        "Nome de documentação inválido\n"
        "Nome deve conter pelo menos um caractere alfanumérico.\n"
        "Exemplo: cdd new documentation guide primeiros-passos"
    )
    error_dangerous_path = (
        "Recusando inicializar em diretório do sistema: {path}"
    )
    error_no_write_permission = (
        "Sem permissão de escrita para o diretório: {path}"
    )
    error_failed_to_create = "Falha ao criar ticket: {error}"
    error_failed_to_create_doc = "Falha ao criar documentação: {error}"

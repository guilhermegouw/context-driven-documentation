# Context-Driven Documentation (CDD)

> 🌐 **English:** [Read in English](README.md)

[![PyPI version](https://badge.fury.io/py/cdd-claude.svg)](https://pypi.org/project/cdd-claude/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-111%20passed-brightgreen.svg)](https://github.com/guilhermegouw/context-driven-documentation)

**Transforme como você constrói software com programação em par com IA**

CDD é um framework de desenvolvimento AI-first que torna a colaboração humano-IA natural, poderosa e produtiva. Crie especificações significativas através de conversas, gere planos de implementação detalhados autonomamente, e deixe a IA escrever código de alta qualidade - tudo mantendo contexto perfeito em todo o seu projeto.

---

## 🎯 **O que Torna o CDD Diferente**

Desenvolvimento tradicional com IA requer constantemente re-explicar seu projeto. CDD elimina esse atrito:

- **Crie especificações significativas de forma conversacional** - Socrates, seu assistente inteligente de documentação, faz as perguntas certas e estrutura seu processo de pensamento em engenharia
- **Transforme specs em planos acionáveis** - IA gera planos de implementação detalhados, passo a passo, autonomamente
- **Gere código de alta qualidade automaticamente a partir de planos** - Execute implementações com contexto completo do projeto
- **Elimine o compartilhamento repetido de contexto com IA** - Capture o contexto do seu projeto uma vez, a IA entende para sempre
- **Documentação nunca fica desatualizada** - Documentação viva que evolui com sua base de código

---

## 💡 **O Princípio Central**

**Contexto capturado uma vez. IA entende para sempre.**

Em vez de gerenciar manualmente o contexto ou repetidamente explicar seu projeto, CDD mantém uma base de conhecimento viva que fornece contexto perfeito automaticamente. Seu parceiro de IA conhece sua arquitetura, padrões e convenções - fazendo cada conversa começar do entendimento compartilhado em vez do zero.

---

## 🧠 **O Modelo Mental**

```
CLAUDE.md = "A constituição do meu projeto - sempre carregada"
specs/    = "Trabalho do sprint atual - tickets com planos"
docs/     = "Documentação viva de features - mantida sincronizada"
AI Agents = "Assistentes inteligentes que conhecem meu projeto"
```

**O fluxo de trabalho:** Requisitos conversacionais → Planejamento autônomo → Implementação com IA → Docs auto-mantidas

---

## ⚡ **Início Rápido**

### Instalação

```bash
pip install cdd-claude
```

### Inicialize Seu Projeto

```bash
cd meu-projeto
cdd init
```

Isso cria:
- `CLAUDE.md` - A constituição do seu projeto
- `specs/tickets/` - Onde seu trabalho de sprint vive
- `docs/features/` e `docs/guides/` - Documentação viva que permanece sincronizada
- Agentes de IA do framework para colaboração inteligente

### Sua Primeira Feature (Fluxo de 5 Passos)

```bash
# 1. Crie um ticket
cdd new feature autenticacao-usuario

# 2. Abra no Claude Code e converse com Socrates
/socrates feature-autenticacao-usuario

# Socrates faz perguntas inteligentes:
# - "Que problema você está resolvendo?"
# - "Quem são seus usuários?"
# - "Quais são os critérios de aceitação?"
# Seu spec.yaml é construído através de conversação natural

# 3. Gere um plano de implementação
/plan feature-autenticacao-usuario

# A IA lê sua spec, entende seu projeto (CLAUDE.md),
# e cria um plano detalhado passo a passo

# 4. Implemente com contexto completo
/exec feature-autenticacao-usuario
# (Ou use /exec-auto para implementação totalmente automática, sem intervenção)

# A IA escreve código seguindo seu plano, arquitetura e convenções

# 5. Seus docs vivos atualizam automaticamente
# docs/features/autenticacao.md reflete o que foi construído
```

**É isso.** Requisitos conversacionais → Planejamento autônomo → Implementação com IA.

### Crie Documentação (Fluxo Mais Simples)

Documentação tem um fluxo mais simples - sem fases spec/plan/exec:

```bash
# Crie um guia ou doc de feature
cdd new documentation guide primeiros-passos
cdd new documentation feature autenticacao

# Preencha com Socrates
/socrates docs/guides/primeiros-passos.md

# Socrates ajuda você a construir docs abrangentes através de conversação
# - Sobre o que é este guia?
# - Quem é o público?
# - Que exemplos ajudariam?
# Sua documentação é construída naturalmente

# Mantenha atualizada conforme seu código evolui - é documentação viva!
```

**Diferença chave:** Documentação é feita para evoluir continuamente com sua base de código. Crie uma vez, refine frequentemente com Socrates.

---

## 🏗️ **Como Funciona**

### **Estrutura de Diretórios**

Quando você executa `cdd init`, obtém uma estrutura simples e git-friendly:

```
meu-projeto/
├── CLAUDE.md              # Constituição do projeto (sempre carregada pela IA)
├── specs/
│   ├── tickets/           # Trabalho ativo de sprint
│   │   └── feature-auth/
│   │       ├── spec.yaml  # Requisitos da conversação
│   │       ├── plan.md    # Plano de implementação gerado pela IA
│   │       └── progress.yaml  # Progresso da implementação (criado pelo /exec)
│   └── archive/           # Tickets completos (auto-arquivados pelo /exec)
└── docs/
    ├── features/          # Documentação viva de features
    │   └── autenticacao.md
    └── guides/            # Guias de usuário e how-tos
        └── primeiros-passos.md
```

### **CLAUDE.md - A Constituição do Seu Projeto**

Este arquivo é carregado automaticamente em cada sessão do Claude Code, fornecendo contexto fundamental:

```markdown
# Constituição do Projeto

## Arquitetura & Padrões
- Design do sistema e padrões centrais
- Fluxo de dados e relacionamento entre componentes

## Stack Técnica & Restrições
- Linguagens, frameworks e versões
- Requisitos de infraestrutura e deployment

## Padrões de Desenvolvimento
- Regras de estilo e formatação de código
- Requisitos e convenções de testes
```

Uma vez que você preencha isso, a IA conhece os fundamentos do seu projeto para sempre.

### **Specs - Tickets Estruturados com Planos**

Cada ticket é uma pasta contendo:

- **spec.yaml** - Requisitos coletados através de conversação com Socrates
- **plan.md** - Plano de implementação detalhado gerado pela IA

**Tipos de ticket:**
- `cdd new feature` - Nova funcionalidade com user stories e critérios de aceitação
- `cdd new bug` - Relatórios de bug com passos de reprodução e avaliação de impacto
- `cdd new spike` - Tarefas de pesquisa com perguntas e critérios de sucesso
- `cdd new enhancement` - Melhorias em features existentes

### **Docs - Documentação Viva**

Documentação de features que permanece sincronizada com seu código:

```markdown
# Feature: Autenticação de Usuário

## Implementação Atual
- OAuth 2.0 com Google
- Autenticação baseada em sessão
- Tokens JWT para acesso à API

## Detalhes Técnicos
- Endpoints: /auth/google, /auth/logout
- Banco de dados: tabelas users, sessions
- Segurança: hash bcrypt, cookies seguros
```

---

## 🤖 **Conheça Socrates - Seu Assistente Inteligente de Documentação**

Socrates transforma pensamentos dispersos em especificações abrangentes através de conversação guiada.

**Abordagem tradicional:**
```
Qual o nome da feature? ___
O que ela faz? ___
Quem são os usuários? ___
```
*Parece preencher um formulário. Sem inteligência.*

**Abordagem Socrates:**
```
Você: /socrates

Socrates: Vou ajudá-lo a criar uma spec abrangente.
Que problema você está tentando resolver?

Você: Usuários não podem acessar seus dados pessoais

Socrates: Que tipo de dados pessoais? Por que não podem ser públicos?
Quem são exatamente esses usuários?

Você: É uma ferramenta SaaS de gerenciamento de projetos. Usuários criam
projetos e tarefas privadas.

Socrates: Perfeito! Então você precisa de autenticação para separar dados
de usuários. Vamos pensar sobre o método de autenticação - o que faz
sentido para seus usuários?
```

**Socrates:**
- Faz as perguntas certas baseadas no contexto
- Aprofunda quando respostas são vagas
- Sugere casos extremos que você pode ter perdido
- Estrutura seus pensamentos em formato de spec apropriado
- Salva progresso conforme você avança

---

## ✨ **Features Atuais**

### ✅ **Criação de Especificações Conversacional**
Crie specs abrangentes através de diálogo natural com Socrates. Sem formulários, sem templates - apenas conversação que constrói entendimento.

### ✅ **Planejamento de Implementação Autônomo**
IA lê sua spec, entende a arquitetura do seu projeto, e gera planos de implementação detalhados passo a passo com estimativas de tempo e avaliação de risco.

### ✅ **Geração de Código com Contexto**
Execute implementações com contexto completo do projeto - arquitetura, padrões, convenções e regras de negócio, tudo automaticamente disponível.

### ✅ **Documentação Viva**
Documentação que evolui com sua base de código, capturando o que realmente existe em vez do que foi planejado.

### ✅ **Baseado em Arquivos & Git-Friendly**
Tudo vive em arquivos que você pode versionar, revisar e compartilhar. Sem bancos de dados, sem vendor lock-in.

---

## 📍 **Fluxo de Trabalho Atual**

```
1. cdd new nome-feature         → Cria estrutura de ticket
2. /socrates nome-feature       → Criação de spec conversacional
3. /plan nome-feature           → IA gera plano de implementação
4. /exec nome-feature           → IA implementa com contexto completo
   (ou /exec-auto para implementação automática sem intervenção)
5. /sync-docs nome-feature      → Sincroniza documentação viva com implementação
```

---

## 🗺️ **Roadmap**

### Em Breve

**Skills - Auto-Ativação** 📅
- Conhecimento técnico que ativa automaticamente baseado na conversação
- Exemplo: Mencione "OAuth" → Padrões de segurança carregam automaticamente
- Exemplo: Mencione "query lenta" → Padrões de otimização de banco carregam automaticamente

**Agents - Especialistas de Domínio** 📅
- Especialistas independentes com expertise focada
- `@business-analyst` - Valida requisitos e casos extremos
- `@security-auditor` - Revisa implicações de segurança
- `@api-architect` - Projeta padrões e estrutura de API

**Auto-Documentação** 📅
- Comando `/complete` que analisa implementações
- Atualiza automaticamente docs vivos baseado no código real
- Captura conhecimento institucional e lições aprendidas

**Colaboração em Equipe** 📅
- Bases de conhecimento compartilhadas entre equipes
- Templates de projeto para diferentes domínios
- Automação de onboarding de equipes

---

## 🎓 **Aprenda Mais**

- **[Guia de Primeiros Passos](docs/guides/GETTING_STARTED.md)** *(Em Breve)*
- **[Guia do Socrates](docs/guides/SOCRATES_GUIDE.md)** - Domine a criação de specs conversacional
- **[Exemplos](docs/examples/)** - Veja exemplos de specs e fluxos de trabalho

---

## 🤝 **Contribuindo**

CDD é código aberto e recebe contribuições! Veja [CONTRIBUTING.md](CONTRIBUTING.md) *(Em Breve)* para:

- Configuração de desenvolvimento
- Visão geral da arquitetura
- Diretrizes de contribuição
- Roadmap e prioridades

---

## 📄 **Licença**

Licença MIT - veja [LICENSE](LICENSE) para detalhes

---

## 🌟 **Por que CDD?**

**Antes do CDD:**
```
Cada conversa com IA começa do zero
→ Constantemente re-explicando arquitetura
→ IA faz sugestões que não se encaixam em seus padrões
→ Documentação fica obsoleta imediatamente
→ Contexto vive nas cabeças dos desenvolvedores
```

**Com CDD:**
```
Contexto capturado uma vez, entendido para sempre
→ IA conhece seu projeto intimamente
→ Sugestões se alinham com sua arquitetura
→ Documentação evolui automaticamente
→ Conhecimento é compartilhado e acessível
```

**O resultado:** Times de desenvolvimento que pensam mais rápido, constroem melhor, e mantêm contexto perfeito sem sobrecarga cognitiva.

---

**Transforme seu fluxo de trabalho de desenvolvimento. Comece com `pip install cdd-claude`**

*Construído para a era do desenvolvimento AI-first. Feito com ❤️ por desenvolvedores que acreditam que a colaboração humano-IA deve ser natural.*

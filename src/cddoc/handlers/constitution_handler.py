"""Handler for CLAUDE.md project constitution files."""

from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()


class ConstitutionHandler:
    """Handle conversation and updates for CLAUDE.md files."""

    def read_current_content(self, path: Path) -> Dict[str, Any]:
        """Read existing markdown content and parse sections."""

        if path.exists():
            content = path.read_text()
            sections = self.parse_markdown_sections(content)
        else:
            content = ""
            sections = {}

        return {
            "raw_content": content,
            "sections": sections,
            "path": path,
            "is_new": not path.exists() or len(content.strip()) < 100,
        }

    def parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections."""

        sections = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(
                        current_content
                    ).strip()

                # Start new section
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def start_conversation(
        self, file_data: Dict, path: Path
    ) -> Dict[str, Any]:
        """Guide conversation for project constitution."""

        sections = file_data["sections"]
        is_new = file_data["is_new"]
        updates = []

        console.print("🏛️ I see you're working on your project constitution.")

        if is_new:
            console.print(
                "This is the foundation of your entire CDD setup. Let's build it together.\n"
            )
        else:
            console.print(
                "Let's review and improve your existing constitution.\n"
            )

        # 1. Project Overview
        if (
            not sections.get("Project Overview")
            or len(sections.get("Project Overview", "")) < 50
        ):
            console.print("Let's start with the fundamentals of your project:")

            project_name = Prompt.ask("What's your project name?")
            project_purpose = Prompt.ask(
                "In one sentence, what does this project do?"
            )
            target_users = Prompt.ask("Who are your primary users?")
            business_domain = Prompt.ask(
                "What business domain or industry is this for?"
            )

            overview = f"""**Project:** {project_name}

**Purpose:** {project_purpose}

**Target Users:** {target_users}

**Business Domain:** {business_domain}

**Core Value Proposition:** What unique value does this project provide?
(You can update this section later with more details)"""

            sections["Project Overview"] = overview
            updates.append(
                {
                    "section": "Project Overview",
                    "action": "Added",
                    "preview": f"{project_name} - {project_purpose}",
                }
            )
            console.print("\n✅ [green]Updated Project Overview[/green]")

        # 2. Technology Stack
        if (
            not sections.get("Technology Stack & Constraints")
            or len(sections.get("Technology Stack & Constraints", "")) < 50
        ):
            console.print("\nLet's document your technology choices:")

            primary_language = Prompt.ask(
                "What's your primary programming language?"
            )
            framework = Prompt.ask(
                "What framework or major libraries do you use?",
                default="None",
            )
            database = Prompt.ask("What database technology?", default="None")
            deployment = Prompt.ask(
                "How do you deploy? (cloud, on-premise, etc.)",
                default="Cloud",
            )

            tech_stack = f"""**Primary Language:** {primary_language}
**Framework:** {framework}
**Database:** {database}
**Deployment:** {deployment}

**Key Dependencies:**
- [List major dependencies as you add them]

**Version Constraints:**
- [Document version requirements]

**Performance Requirements:**
- [Response time, throughput, etc.]

**Security Requirements:**
- [Authentication, authorization, compliance needs]"""

            sections["Technology Stack & Constraints"] = tech_stack
            updates.append(
                {
                    "section": "Technology Stack & Constraints",
                    "action": "Added",
                    "preview": f"{primary_language}, {framework}, {database}",
                }
            )
            console.print(
                "\n✅ [green]Updated Technology Stack & Constraints[/green]"
            )

        # 3. Architecture & Design Patterns
        if (
            not sections.get("Architecture & Design Patterns")
            or len(sections.get("Architecture & Design Patterns", "")) < 50
        ):
            if Confirm.ask(
                "\nWould you like to document your architecture and design patterns?"
            ):
                console.print(
                    "[dim]Describe your system architecture...[/dim]"
                )

                architecture_type = Prompt.ask(
                    "What's your overall architecture? (e.g., monolith, microservices, serverless)"
                )
                design_patterns = Prompt.ask(
                    "What design patterns do you use? (e.g., MVC, Repository, Factory)",
                    default="To be documented",
                )
                code_organization = Prompt.ask(
                    "How is your code organized? (e.g., by feature, by layer)",
                    default="To be documented",
                )

                architecture = f"""**Architecture Type:** {architecture_type}

**Design Patterns:**
{design_patterns}

**Code Organization:**
{code_organization}

**Key Architectural Decisions:**
- [Document important architectural choices and their rationale]

**Integration Points:**
- [External services, APIs, third-party integrations]"""

                sections["Architecture & Design Patterns"] = architecture
                updates.append(
                    {
                        "section": "Architecture & Design Patterns",
                        "action": "Added",
                        "preview": architecture_type,
                    }
                )
                console.print(
                    "\n✅ [green]Updated Architecture & Design Patterns[/green]"
                )

        # 4. Development Standards
        if (
            not sections.get("Development Standards")
            or len(sections.get("Development Standards", "")) < 50
        ):
            if Confirm.ask(
                "\nWould you like to document your development standards?"
            ):
                console.print(
                    "[dim]Define code quality and testing standards...[/dim]"
                )

                code_style = Prompt.ask(
                    "What code style/linting tools do you use?",
                    default="To be defined",
                )
                testing_approach = Prompt.ask(
                    "What's your testing strategy? (e.g., unit, integration, e2e)",
                    default="To be defined",
                )
                review_process = Prompt.ask(
                    "What's your code review process?",
                    default="Pull request review required",
                )

                standards = f"""**Code Style:**
{code_style}

**Testing Standards:**
{testing_approach}

**Code Review Process:**
{review_process}

**Definition of Done:**
- Code written and tested
- Tests passing
- Code reviewed and approved
- Documentation updated
- [Add more criteria as needed]

**Quality Gates:**
- [Automated checks, coverage requirements, etc.]"""

                sections["Development Standards"] = standards
                updates.append(
                    {
                        "section": "Development Standards",
                        "action": "Added",
                        "preview": f"Style: {code_style}, Testing: {testing_approach}",
                    }
                )
                console.print(
                    "\n✅ [green]Updated Development Standards[/green]"
                )

        # 5. Team Conventions
        if (
            not sections.get("Team Conventions")
            or len(sections.get("Team Conventions", "")) < 50
        ):
            if Confirm.ask("\nWould you like to document team conventions?"):
                console.print(
                    "[dim]Establish naming and workflow conventions...[/dim]"
                )

                naming = Prompt.ask(
                    "What naming conventions do you follow?",
                    default="To be documented",
                )
                branching = Prompt.ask(
                    "What's your branching strategy?",
                    default="feature branches",
                )
                commit_style = Prompt.ask(
                    "What commit message format do you use?",
                    default="Conventional commits",
                )

                conventions = f"""**Naming Conventions:**
{naming}

**Branching Strategy:**
{branching}

**Commit Message Format:**
{commit_style}

**Workflow:**
- [Define your development workflow]

**Communication:**
- [How does the team communicate and collaborate?]"""

                sections["Team Conventions"] = conventions
                updates.append(
                    {
                        "section": "Team Conventions",
                        "action": "Added",
                        "preview": f"Branching: {branching}, Commits: {commit_style}",
                    }
                )
                console.print("\n✅ [green]Updated Team Conventions[/green]")

        return {"sections": sections, "updates": updates}

    def update_file(
        self, path: Path, conversation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update CLAUDE.md with conversation results."""

        sections = conversation_data["sections"]

        # Rebuild markdown content
        content_parts = ["# Project Constitution\n"]
        content_parts.append(
            "> This file serves as the foundational context for all AI-assisted development in this project.\n"
        )
        content_parts.append(
            "> Complete this constitution to enable powerful, context-aware AI collaboration.\n"
        )

        section_order = [
            "Project Overview",
            "Architecture & Design Patterns",
            "Technology Stack & Constraints",
            "Development Standards",
            "Team Conventions",
        ]

        for section_name in section_order:
            if section_name in sections:
                content_parts.append(f"## {section_name}\n")
                content_parts.append(f"{sections[section_name]}\n\n")

        content_parts.append("---\n")
        content_parts.append(
            "*Generated by CDD Framework v0.1.0 - Learn more: https://github.com/guilhermegouw/context-driven-documentation*\n"
        )

        new_content = "\n".join(content_parts)
        path.write_text(new_content)

        return {
            "updates": conversation_data["updates"],
            "file_path": str(path),
            "next_steps": [
                f"Review your completed constitution: {path}",
                'Create your first ticket: cdd new feature "your-feature"',
                "Use Socrates to develop ticket specs: cdd socrates specs/tickets/[ticket]/spec.yaml",
                "Start development with full context",
            ],
        }

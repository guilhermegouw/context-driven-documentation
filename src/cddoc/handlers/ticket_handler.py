"""Handler for ticket specification files (feature/bug/spike)."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()


class TicketSpecHandler:
    """Handle conversation and updates for ticket specification files."""

    def read_current_content(self, path: Path) -> Dict[str, Any]:
        """Read existing YAML content or create empty structure."""

        if path.exists():
            with open(path, "r") as f:
                content = yaml.safe_load(f) or {}
        else:
            # Create parent directory if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            content = {}

        # Determine ticket type from path or content
        ticket_type = self.detect_ticket_type(path, content)

        return {
            "content": content,
            "ticket_type": ticket_type,
            "path": path,
            "is_new": not path.exists() or not content,
        }

    def detect_ticket_type(self, path: Path, content: Dict) -> str:
        """Detect if this is feature/bug/spike ticket."""

        # Check existing content first
        if content.get("ticket", {}).get("type"):
            return content["ticket"]["type"]

        # Infer from path name
        path_str = str(path).lower()
        if "feature" in path_str or "feat" in path_str:
            return "feature"
        elif "bug" in path_str or "fix" in path_str:
            return "bug"
        elif "spike" in path_str or "research" in path_str:
            return "spike"
        else:
            # Ask user
            return Prompt.ask(
                "What type of ticket is this?",
                choices=["feature", "bug", "spike"],
                default="feature",
            )

    def start_conversation(
        self, file_data: Dict, path: Path
    ) -> Dict[str, Any]:
        """Run guided conversation based on ticket type."""

        ticket_type = file_data["ticket_type"]
        content = file_data["content"]
        is_new = file_data["is_new"]

        console.print(
            f"\n🎯 I see you're working on a [bold]{ticket_type}[/bold] ticket."
        )

        if is_new:
            console.print(
                "This looks like a new ticket. Let's build the specification through conversation.\n"
            )
        else:
            console.print(
                "I can see some existing content. Let's refine and complete it.\n"
            )

        # Route to appropriate conversation flow
        if ticket_type == "feature":
            return self.feature_conversation(content, path)
        elif ticket_type == "bug":
            return self.bug_conversation(content, path)
        elif ticket_type == "spike":
            return self.spike_conversation(content, path)

        return {"content": content, "updates": [], "ticket_type": ticket_type}

    def feature_conversation(
        self, content: Dict, path: Path
    ) -> Dict[str, Any]:
        """Guide conversation for feature tickets."""

        updates = []

        # 1. Title
        if not content.get("title"):
            console.print("Let's start with a descriptive title:")
            title = Prompt.ask("What's a concise title for this feature?")
            content["title"] = title
            updates.append(
                {"section": "title", "action": "Added", "preview": title}
            )
            console.print("\n✅ [green]Updated title[/green]")

        # 2. Problem Discovery - User Story
        if not content.get("user_story"):
            console.print("\nNow let's define the user story:")
            console.print(
                "[dim]We'll use the format: As a [user], I want [capability], So that [benefit][/dim]\n"
            )

            user_type = Prompt.ask("Who is the user? (role/persona)")
            capability = Prompt.ask("What capability or action do they need?")
            benefit = Prompt.ask("What value or benefit will this provide?")

            # Generate user story
            user_story = (
                f"As a {user_type},\nI want {capability},\nSo that {benefit}."
            )

            content["user_story"] = user_story
            updates.append(
                {
                    "section": "user_story",
                    "action": "Added",
                    "preview": user_story,
                }
            )

            console.print("\n✅ [green]Updated user story[/green]")

        # 3. Business Value
        if not content.get("business_value"):
            console.print("\nLet's establish the business context:")
            business_why = Prompt.ask(
                "Why is this important for the business?"
            )
            business_impact = Prompt.ask(
                "What measurable impact will this have?"
            )

            business_value = (
                f"{business_why}\n\nBusiness Impact: {business_impact}"
            )
            content["business_value"] = business_value
            updates.append(
                {
                    "section": "business_value",
                    "action": "Added",
                    "preview": business_value[:100],
                }
            )
            console.print("\n✅ [green]Updated business value[/green]")

        # 4. Acceptance Criteria
        if not content.get("acceptance_criteria"):
            console.print("\nNow let's define success criteria:")
            console.print(
                "[dim]I'll help you create specific, testable acceptance criteria.[/dim]\n"
            )

            criteria = []
            while True:
                criterion = Prompt.ask(
                    f"Acceptance criterion #{len(criteria) + 1} (or 'done' to finish)",
                    default="done" if len(criteria) >= 3 else "",
                )

                if criterion.lower() == "done":
                    if len(criteria) == 0:
                        console.print(
                            "[yellow]Please add at least one criterion[/yellow]"
                        )
                        continue
                    break

                criteria.append(criterion)
                console.print(f"  ✅ Added: {criterion}")

            content["acceptance_criteria"] = criteria
            updates.append(
                {
                    "section": "acceptance_criteria",
                    "action": "Added",
                    "preview": f"{len(criteria)} criteria defined",
                }
            )
            console.print(
                f"\n✅ [green]Added {len(criteria)} acceptance criteria[/green]"
            )

        # 5. Implementation Scope
        if not content.get("implementation_scope"):
            console.print("\nLet's think about the implementation:")

            scope = {}

            if Confirm.ask("Does this involve frontend changes?"):
                frontend = Prompt.ask(
                    "What frontend components or changes are needed?"
                )
                scope["frontend"] = [frontend]

            if Confirm.ask("Does this involve backend changes?"):
                backend = Prompt.ask(
                    "What backend services or APIs are needed?"
                )
                scope["backend"] = [backend]

            if Confirm.ask("Does this involve database changes?"):
                database = Prompt.ask("What database changes are required?")
                scope["database"] = [database]

            content["implementation_scope"] = scope
            updates.append(
                {
                    "section": "implementation_scope",
                    "action": "Added",
                    "preview": f"Frontend: {bool(scope.get('frontend'))}, Backend: {bool(scope.get('backend'))}",
                }
            )
            console.print("\n✅ [green]Updated implementation scope[/green]")

        # 6. Technical Considerations
        if Confirm.ask(
            "\nWould you like to document any technical considerations or constraints?"
        ):
            considerations = Prompt.ask(
                "What technical aspects should the team be aware of?"
            )
            content["technical_considerations"] = considerations
            updates.append(
                {
                    "section": "technical_considerations",
                    "action": "Added",
                    "preview": considerations[:100],
                }
            )
            console.print("\n✅ [green]Added technical considerations[/green]")

        return {
            "content": content,
            "updates": updates,
            "ticket_type": "feature",
        }

    def bug_conversation(self, content: Dict, path: Path) -> Dict[str, Any]:
        """Guide conversation for bug tickets."""

        updates = []

        # 1. Title
        if not content.get("title"):
            console.print("Let's document this bug:")
            title = Prompt.ask("What's a concise title for this bug?")
            content["title"] = title
            updates.append(
                {"section": "title", "action": "Added", "preview": title}
            )
            console.print("\n✅ [green]Updated title[/green]")

        # 2. Problem Description
        if not content.get("problem_description"):
            console.print("\nDescribe the problem:")
            problem = Prompt.ask("What is the current buggy behavior?")
            expected = Prompt.ask("What should be happening instead?")

            problem_description = f"**Current Behavior:**\n{problem}\n\n**Expected Behavior:**\n{expected}"
            content["problem_description"] = problem_description
            updates.append(
                {
                    "section": "problem_description",
                    "action": "Added",
                    "preview": problem[:100],
                }
            )
            console.print("\n✅ [green]Updated problem description[/green]")

        # 3. Reproduction Steps
        if not content.get("reproduction_steps"):
            console.print("\nLet's document how to reproduce this bug:")
            console.print(
                "[dim]Enter steps one at a time (type 'done' when finished)[/dim]\n"
            )

            steps = []
            step_num = 1
            while True:
                step = Prompt.ask(
                    f"Step {step_num}",
                    default="done" if len(steps) >= 2 else "",
                )

                if step.lower() == "done":
                    if len(steps) == 0:
                        console.print(
                            "[yellow]Please add at least one step[/yellow]"
                        )
                        continue
                    break

                steps.append(step)
                console.print(f"  ✅ Added step {step_num}")
                step_num += 1

            content["reproduction_steps"] = steps
            updates.append(
                {
                    "section": "reproduction_steps",
                    "action": "Added",
                    "preview": f"{len(steps)} steps documented",
                }
            )
            console.print(
                f"\n✅ [green]Added {len(steps)} reproduction steps[/green]"
            )

        # 4. Impact Assessment
        if not content.get("impact_assessment"):
            console.print("\nLet's assess the impact:")
            severity = Prompt.ask(
                "What's the severity?",
                choices=["critical", "high", "medium", "low"],
                default="medium",
            )
            affected_users = Prompt.ask(
                "Who is affected? (e.g., all users, admins only, etc.)"
            )
            workaround = Prompt.ask(
                "Is there a workaround?", default="None known"
            )

            impact = {
                "severity": severity,
                "affected_users": affected_users,
                "workaround": workaround,
            }
            content["impact_assessment"] = impact
            updates.append(
                {
                    "section": "impact_assessment",
                    "action": "Added",
                    "preview": f"Severity: {severity}, Affects: {affected_users}",
                }
            )
            console.print("\n✅ [green]Updated impact assessment[/green]")

        return {"content": content, "updates": updates, "ticket_type": "bug"}

    def spike_conversation(self, content: Dict, path: Path) -> Dict[str, Any]:
        """Guide conversation for spike tickets."""

        updates = []

        # 1. Title
        if not content.get("title"):
            console.print("Let's define this research spike:")
            title = Prompt.ask("What's a concise title for this spike?")
            content["title"] = title
            updates.append(
                {"section": "title", "action": "Added", "preview": title}
            )
            console.print("\n✅ [green]Updated title[/green]")

        # 2. Research Questions
        if not content.get("research_questions"):
            console.print("\nWhat questions are we trying to answer?")
            console.print(
                "[dim]Enter questions one at a time (type 'done' when finished)[/dim]\n"
            )

            questions = []
            while True:
                question = Prompt.ask(
                    f"Research question #{len(questions) + 1}",
                    default="done" if len(questions) >= 2 else "",
                )

                if question.lower() == "done":
                    if len(questions) == 0:
                        console.print(
                            "[yellow]Please add at least one question[/yellow]"
                        )
                        continue
                    break

                questions.append(question)
                console.print(f"  ✅ Added: {question}")

            content["research_questions"] = questions
            updates.append(
                {
                    "section": "research_questions",
                    "action": "Added",
                    "preview": f"{len(questions)} questions defined",
                }
            )
            console.print(
                f"\n✅ [green]Added {len(questions)} research questions[/green]"
            )

        # 3. Investigation Approach
        if not content.get("investigation_approach"):
            console.print("\nHow will you investigate?")
            approach = Prompt.ask("Describe your investigation methodology")
            content["investigation_approach"] = approach
            updates.append(
                {
                    "section": "investigation_approach",
                    "action": "Added",
                    "preview": approach[:100],
                }
            )
            console.print("\n✅ [green]Updated investigation approach[/green]")

        # 4. Success Criteria
        if not content.get("success_criteria"):
            console.print("\nWhat defines success for this spike?")
            success = Prompt.ask(
                "How will you know this research is complete?"
            )
            content["success_criteria"] = success
            updates.append(
                {
                    "section": "success_criteria",
                    "action": "Added",
                    "preview": success[:100],
                }
            )
            console.print("\n✅ [green]Updated success criteria[/green]")

        # 5. Time Box
        if Confirm.ask("\nWould you like to set a time box for this spike?"):
            timebox = Prompt.ask(
                "How long should this investigation take? (e.g., 4 hours, 2 days)"
            )
            content["timebox"] = timebox
            updates.append(
                {
                    "section": "timebox",
                    "action": "Added",
                    "preview": timebox,
                }
            )
            console.print("\n✅ [green]Added timebox[/green]")

        return {"content": content, "updates": updates, "ticket_type": "spike"}

    def update_file(
        self, path: Path, conversation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update YAML file with conversation results."""

        content = conversation_data["content"]

        # Add metadata
        if "ticket" not in content:
            content["ticket"] = {}

        content["ticket"]["type"] = conversation_data["ticket_type"]

        # Add timestamps
        if not content["ticket"].get("created"):
            content["ticket"]["created"] = datetime.now().strftime("%Y-%m-%d")
        content["ticket"]["updated"] = datetime.now().strftime("%Y-%m-%d")

        # Write updated YAML
        with open(path, "w") as f:
            yaml.dump(
                content,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

        # Determine next steps based on ticket type
        ticket_type = conversation_data["ticket_type"]
        next_steps = [
            f"Review the completed spec: {path}",
        ]

        if ticket_type == "feature":
            next_steps.append("Consider refining with domain experts")
            next_steps.append(
                f"Start development: cdd plan {path.parent.name}"
            )
        elif ticket_type == "bug":
            next_steps.append(
                "Begin investigation with the reproduction steps"
            )
            next_steps.append("Consider adding diagnostic logging")
        elif ticket_type == "spike":
            next_steps.append(
                "Begin research following the investigation approach"
            )
            next_steps.append("Document findings as you discover them")

        return {
            "updates": conversation_data["updates"],
            "file_path": str(path),
            "next_steps": next_steps,
        }

"""Progress tracking handler for CDD implementation execution."""

from datetime import UTC, datetime
from pathlib import Path
from typing import List, Literal, Optional, TypedDict

import yaml


class FileTouched(TypedDict):
    path: str
    operation: Literal["created", "modified", "deleted"]


class Step(TypedDict):
    step_id: int
    description: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    started_at: Optional[str]
    completed_at: Optional[str]
    files_touched: List[FileTouched]


class AcceptanceCriterion(TypedDict):
    criterion: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    validated_at: Optional[str]


class Issue(TypedDict):
    timestamp: str
    type: Literal[
        "test_failure", "linting_error", "runtime_error", "missing_dependency"
    ]
    description: str
    resolution: Optional[str]
    resolved_at: Optional[str]


class ProgressData(TypedDict):
    plan_path: str
    spec_path: str
    started_at: str
    updated_at: str
    status: Literal["in_progress", "completed", "blocked"]
    steps: List[Step]
    acceptance_criteria: List[AcceptanceCriterion]
    files_modified: List[str]
    files_created: List[str]
    issues: List[Issue]


class ProgressHandlerError(Exception):
    """Base exception for progress handler errors."""

    pass


class ProgressHandler:
    """Handler for reading and writing progress.yaml files."""

    @staticmethod
    def read_progress(progress_path: Path) -> ProgressData:
        """Read and parse progress.yaml file.

        Args:
            progress_path: Path to progress.yaml file

        Returns:
            Parsed progress data

        Raises:
            ProgressHandlerError: If file doesn't exist or is malformed
        """
        if not progress_path.exists():
            raise ProgressHandlerError(
                f"Progress file not found: {progress_path}"
            )

        try:
            with open(progress_path, "r") as f:
                data = yaml.safe_load(f)

            # Validate required fields
            required_fields = [
                "plan_path",
                "spec_path",
                "started_at",
                "updated_at",
                "status",
                "steps",
                "acceptance_criteria",
            ]
            for field in required_fields:
                if field not in data:
                    raise ProgressHandlerError(
                        f"Missing required field: {field}"
                    )

            return data
        except yaml.YAMLError as e:
            raise ProgressHandlerError(f"Invalid YAML format: {e}")

    @staticmethod
    def write_progress(progress_path: Path, data: ProgressData) -> None:
        """Write progress data to progress.yaml file.

        Args:
            progress_path: Path where progress.yaml will be written
            data: Progress data to write
        """
        # Update timestamp
        data["updated_at"] = (
            datetime.now(UTC).isoformat().replace("+00:00", "Z")
        )

        # Ensure parent directory exists
        progress_path.parent.mkdir(parents=True, exist_ok=True)

        with open(progress_path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def initialize_progress(plan_path: Path, spec_path: Path) -> ProgressData:
        """Create initial progress structure from plan and spec paths.

        Args:
            plan_path: Path to plan.md file
            spec_path: Path to spec.yaml file

        Returns:
            Initial progress data structure
        """
        now = datetime.now(UTC).isoformat().replace("+00:00", "Z")

        return {
            "plan_path": str(plan_path),
            "spec_path": str(spec_path),
            "started_at": now,
            "updated_at": now,
            "status": "in_progress",
            "steps": [],
            "acceptance_criteria": [],
            "files_modified": [],
            "files_created": [],
            "issues": [],
        }

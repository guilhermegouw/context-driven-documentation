"""Spec handler for managing spec.yaml ticket status."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import yaml


class SpecHandlerError(Exception):
    """Base exception for spec handler errors."""

    pass


TicketStatus = Literal[
    "draft", "defined", "planned", "in_progress", "completed", "archived"
]


class SpecHandler:
    """Handler for reading and updating spec.yaml files."""

    @staticmethod
    def read_spec(spec_path: Path) -> dict:
        """Read and parse spec.yaml file.

        Args:
            spec_path: Path to spec.yaml file

        Returns:
            Parsed spec data

        Raises:
            SpecHandlerError: If file doesn't exist or is malformed
        """
        if not spec_path.exists():
            raise SpecHandlerError(f"Spec file not found: {spec_path}")

        try:
            with open(spec_path, "r") as f:
                data = yaml.safe_load(f)

            if not isinstance(data, dict):
                raise SpecHandlerError("Spec file must contain a dictionary")

            return data
        except yaml.YAMLError as e:
            raise SpecHandlerError(f"Invalid YAML format: {e}")

    @staticmethod
    def write_spec(spec_path: Path, data: dict) -> None:
        """Write spec data to spec.yaml file.

        Args:
            spec_path: Path where spec.yaml will be written
            data: Spec data to write
        """
        # Ensure parent directory exists
        spec_path.parent.mkdir(parents=True, exist_ok=True)

        with open(spec_path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def update_status(
        spec_path: Path,
        new_status: TicketStatus,
        add_timestamp: bool = True,
    ) -> None:
        """Update the ticket status in spec.yaml.

        Args:
            spec_path: Path to spec.yaml file
            new_status: New status to set
            add_timestamp: Whether to add a timestamp for the status change

        Raises:
            SpecHandlerError: If spec file doesn't exist or has no ticket section
        """
        data = SpecHandler.read_spec(spec_path)

        # Ensure ticket section exists
        if "ticket" not in data:
            raise SpecHandlerError("Spec file missing 'ticket' section")

        # Update status
        data["ticket"]["status"] = new_status

        # Update the 'updated' timestamp if it exists
        now = datetime.now(UTC).strftime("%Y-%m-%d")
        if "updated" in data["ticket"]:
            data["ticket"]["updated"] = now

        # Add specific timestamps based on status
        if add_timestamp:
            if new_status == "in_progress":
                data["ticket"]["implementation_started"] = now
            elif new_status == "completed":
                data["ticket"]["implementation_completed"] = now
            elif new_status == "archived":
                data["ticket"]["archived_at"] = now

        # Write back
        SpecHandler.write_spec(spec_path, data)

    @staticmethod
    def get_status(spec_path: Path) -> TicketStatus | None:
        """Get the current ticket status from spec.yaml.

        Args:
            spec_path: Path to spec.yaml file

        Returns:
            Current status or None if not set

        Raises:
            SpecHandlerError: If spec file doesn't exist
        """
        data = SpecHandler.read_spec(spec_path)

        if "ticket" not in data:
            return None

        return data["ticket"].get("status")

"""Base handler class for file-specific conversation and update logic."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class FileHandler(ABC):
    """Base class for file-specific conversation and update logic."""

    @abstractmethod
    def read_current_content(self, path: Path) -> Dict[str, Any]:
        """Read and parse existing content.

        Args:
            path: Path to file

        Returns:
            Dictionary containing parsed content and metadata
        """
        pass

    @abstractmethod
    def start_conversation(
        self, file_data: Dict[str, Any], path: Path
    ) -> Dict[str, Any]:
        """Run guided conversation for this file type.

        Args:
            file_data: Parsed file data from read_current_content
            path: Path to file

        Returns:
            Dictionary containing conversation results and updates
        """
        pass

    @abstractmethod
    def update_file(
        self, path: Path, conversation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update file with conversation results.

        Args:
            path: Path to file to update
            conversation_data: Data from conversation to apply

        Returns:
            Dictionary containing update results and next steps
        """
        pass

"""This houses the interface for the file manager."""

import logging
from abc import ABC, abstractmethod
from typing import Any


class IFileManager(ABC):
    """This is the interface for the file manager."""

    def __init__(self, name: str, file_path: str) -> None:
        """
        Initialize the file manager.

        Args:
            name: The __name__ of the file manager which inherits this class.
        """
        self.log = logging.getLogger(name)
        self.file = file_path
        super().__init__()

    @abstractmethod
    def on_ready(self) -> None:
        """Call when the client is ready."""
        pass

    @abstractmethod
    def read(self) -> list[dict[str, Any]] | dict[str, Any]:
        """Read the file."""
        pass

    @abstractmethod
    def write(self, data: list[dict[str, Any]] | dict[str, Any]) -> None:
        """Write to the file."""
        pass

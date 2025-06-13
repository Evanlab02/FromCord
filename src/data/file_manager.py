"""This houses the interface for the file manager."""

from json import dump, load
from typing import Any

from src.data.interfaces import IFileManager


class FileManager(IFileManager):
    """This is the file manager."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize the file manager.

        Args:
            name: The __name__ of the file manager which inherits this class.
        """
        name = __name__
        super().__init__(name=name, file_path=file_path)

    def on_ready(self) -> None:
        """Call when the client is ready."""
        self.log.info(f"File manager created for file: {self.file}")

    def read(self) -> list[dict[str, Any]] | dict[str, Any]:
        """Read the file."""
        with open(self.file, "r") as file:
            return load(file)  # type: ignore

    def write(self, data: list[dict[str, Any]] | dict[str, Any]) -> None:
        """Write to the file."""
        with open(self.file, "w") as file:
            dump(data, file, indent=4)

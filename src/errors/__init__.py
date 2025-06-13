"""This houses the custom error classes."""


class ConfigError(Exception):
    """This is the base class for all config errors."""

    def __init__(self, message: str) -> None:
        """Initialize the config error."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return the error message."""
        return self.message


class FileError(Exception):
    """This is the base class for all file errors."""

    def __init__(self, message: str) -> None:
        """Initialize the file error."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return the error message."""
        return self.message

"""This houses the interface for the config manager."""

import logging
from abc import ABC, abstractmethod

from src.schemas import GuildConfig


class IGuildConfigManager(ABC):
    """This is the interface for the guild config manager."""

    def __init__(self, name: str) -> None:
        """
        Initialize the guild config manager.

        Args:
            name: The __name__ of the guild config manager which inherits this class.
        """
        self.log = logging.getLogger(name)
        super().__init__()

    @abstractmethod
    def on_ready(self) -> None:
        """
        Call when the client is ready.

        Logs information to console about the guild config manager state.
        """
        pass

    @abstractmethod
    def load(self) -> None:
        """Load the guild config into memory."""
        pass

    @abstractmethod
    def save(self) -> None:
        """Save the guild config to the file."""
        pass

    @abstractmethod
    def add_config(self, guild_id: int, category_id: int) -> None:
        """Add a new guild configuration."""
        pass

    @abstractmethod
    def get_config(self, guild_id: int) -> GuildConfig:
        """Get the guild configuration."""
        pass

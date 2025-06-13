"""This houses the interface for the config manager."""

import logging
from abc import ABC, abstractmethod


class IAppConfigManager(ABC):
    """This is the interface for the config manager."""

    def __init__(self, name: str) -> None:
        """
        Initialize the config manager.

        Args:
            name: The __name__ of the config manager which inherits this class.
        """
        self.log = logging.getLogger(name)
        super().__init__()

    @abstractmethod
    def on_ready(self) -> None:
        """
        Call when the client is ready.

        Logs information to console about the config manager state.
        """
        pass

    @abstractmethod
    def get_app_id(self) -> str:
        """
        Get the app id.

        Returns:
            The app id.
        """
        pass

    @abstractmethod
    def get_public_key(self) -> str:
        """
        Get the public key.

        Returns:
            The public key.
        """
        pass

    @abstractmethod
    def get_token(self) -> str:
        """
        Get the token.

        Returns:
            The token.
        """
        pass

    @abstractmethod
    def get_primary_guild_id(self) -> int:
        """
        Get the primary guild id.

        Returns:
            The primary guild id.
        """
        pass

    @abstractmethod
    def get_nightreign_category_id(self) -> int:
        """
        Get the default nightreign category id.

        Returns:
            The nightreign category id.
        """
        pass

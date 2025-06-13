"""This houses the config manager."""

import os

from dotenv import load_dotenv

from src.config.interfaces import IAppConfigManager
from src.errors import ConfigError


class AppConfigManager(IAppConfigManager):
    """This is the app config manager."""

    def __init__(self) -> None:
        """Initialize the app config manager."""
        name = __name__
        super().__init__(name=name)

        load_dotenv()
        self.APP_ID = os.getenv("APP_ID", "")
        self.PUBLIC_KEY = os.getenv("PUBLIC_KEY", "")
        self.TOKEN = os.getenv("BOT_TOKEN", "")
        self.PRIMARY_GUILD_ID = int(os.getenv("PRIMARY_GUILD", "0"))
        self.NIGHTREIGN_CATEGORY_ID = int(os.getenv("NIGHTREIGN_GUILD_CATEGORY", "0"))
        self.BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "0"))

    def on_ready(self) -> None:
        """
        Call when the client is ready.

        Logs information to console about the app config manager state.
        """
        self.log.info("App Config Manager is checking for errors...")
        values_to_check = [
            self.APP_ID,
            self.PUBLIC_KEY,
            self.TOKEN,
            self.PRIMARY_GUILD_ID,
            self.NIGHTREIGN_CATEGORY_ID,
        ]
        for value in values_to_check:
            if not value:
                self.log.error(f"Missing value: {value}")
                raise ConfigError(f"Missing value: {value}")

        self.log.info("App Config Manager Info:")
        self.log.info(f"==> App ID: {self.APP_ID}")
        self.log.info(f"==> Public Key: {self.PUBLIC_KEY}")
        self.log.info(f"==> Token: {self.TOKEN[:3]}{'*' * (len(self.TOKEN) - 3)}")
        self.log.info(f"==> Primary Guild ID: {self.PRIMARY_GUILD_ID}")
        self.log.info(f"==> Nightreign Category ID: {self.NIGHTREIGN_CATEGORY_ID}")
        self.log.info("App Config Manager is ready.")

    def get_app_id(self) -> str:
        """
        Get the app id.

        Returns:
            The app id.
        """
        return self.APP_ID

    def get_public_key(self) -> str:
        """
        Get the public key.

        Returns:
            The public key.
        """
        return self.PUBLIC_KEY

    def get_token(self) -> str:
        """
        Get the token.

        Returns:
            The token.
        """
        return self.TOKEN

    def get_primary_guild_id(self) -> int:
        """
        Get the primary guild id.

        Returns:
            The primary guild id.
        """
        return self.PRIMARY_GUILD_ID

    def get_nightreign_category_id(self) -> int:
        """
        Get the default nightreign category id.

        Returns:
            The nightreign category id.
        """
        return self.NIGHTREIGN_CATEGORY_ID

    def get_bot_owner_id(self) -> int:
        """
        Get the bot owner id.

        Returns:
            The bot owner id.
        """
        return self.BOT_OWNER_ID

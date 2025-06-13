"""This houses the guild config manager."""

from src.config.interfaces import IAppConfigManager, IGuildConfigManager
from src.data import FileManager
from src.errors import ConfigError, FileError
from src.schemas import GuildConfig


class GuildConfigManager(IGuildConfigManager):
    """This is the guild config manager."""

    def __init__(self, app_config: IAppConfigManager) -> None:
        """Initialize the guild config manager."""
        name = __name__
        self.file = FileManager(file_path="data/guilds.json")
        self.app_config: IAppConfigManager = app_config
        self.data: dict[str, GuildConfig] = {}
        super().__init__(name=name)

    def on_ready(self) -> None:
        """Call when the client is ready."""
        self.log.info("Guild Config Manager is checking for errors...")
        values_to_check = [
            self.app_config.get_primary_guild_id(),
            self.app_config.get_nightreign_category_id(),
        ]
        for value in values_to_check:
            if not value:
                self.log.error(f"Missing value: {value}")
                raise ConfigError(f"Missing value: {value}")

        self.file.on_ready()

        self.log.info("Loading guild config into memory...")
        self.load()

        self.log.info("Creating default guild configuration...")
        primary_guild = self.app_config.get_primary_guild_id()
        nightreign_category = self.app_config.get_nightreign_category_id()
        self.data[str(primary_guild)] = GuildConfig(
            guild_id=primary_guild,
            nightreign_category_id=nightreign_category,
        )

        self.log.info("Saving guild config to file...")
        self.save()

        self.log.info("Guild Config Manager Info:")
        self.log.info(f"==> File: {self.file.file}")
        self.log.info(f"==> Guilds: {len(self.data)}")
        self.log.info("Guild Config Manager is ready.")

    def load(self) -> None:
        """Load the guild config into memory."""
        try:
            file_data = self.file.read()
        except Exception as error:
            self.log.warning(f"Error loading guild config: {error}")
            self.log.warning("Creating new configuration.")
            self.data = {}
            return

        if not isinstance(file_data, dict):
            raise FileError("Guild config file is not in the correct format.")

        for guild_id, guild_config in file_data.items():
            self.data[guild_id] = GuildConfig(**guild_config)

    def save(self) -> None:
        """Save the guild config to the file."""
        file_data = {}
        for guild_id, guild_config in self.data.items():
            file_data[guild_id] = guild_config.model_dump()
        self.file.write(file_data)

    def add_config(self, guild_id: int, category_id: int) -> None:
        """
        Add a new guild configuration.

        Args:
            guild_id: The guild id.
            category_id: The category id.
        """
        self.data[str(guild_id)] = GuildConfig(
            guild_id=guild_id,
            nightreign_category_id=category_id,
        )

    def get_config(self, guild_id: int) -> GuildConfig:
        """
        Get the guild configuration.

        Args:
            guild_id: The guild id.

        Returns:
            The guild configuration.
        """
        return self.data[str(guild_id)]

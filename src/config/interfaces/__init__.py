"""This houses the interfaces for the config managers."""

from src.config.interfaces.i_app_config_manager import IAppConfigManager
from src.config.interfaces.i_guild_config_manager import IGuildConfigManager

__all__ = ["IAppConfigManager", "IGuildConfigManager"]

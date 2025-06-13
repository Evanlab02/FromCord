"""This is the entry point for the project."""

from discord import Intents

from src.config import AppConfigManager, GuildConfigManager
from src.services import NightreignService

app_config = AppConfigManager()
guild_config = GuildConfigManager(app_config=app_config)
nightreign_service = NightreignService(
    app_config=app_config,
    guild_config=guild_config,
)

INTENTS = Intents.all()
TOKEN = app_config.get_token()

"""This houses the schemas for the guilds."""

from pydantic import BaseModel


class GuildConfig(BaseModel):
    """This is the schema for the guild config."""

    guild_id: int
    nightreign_category_id: int

"""This module contains the commands for the config."""

import logging

from discord import CategoryChannel, Interaction
from discord.app_commands import Group

from src import guild_config

group = Group(name="config", description="Configuration commands")
log = logging.getLogger(__name__)


@group.command(name="nightreign", description="Set the nightreign channel category.")
async def nightreign(interaction: Interaction, nightreign_category: str) -> None:
    """
    Command to set the nightreign channel category.

    Args:
        interaction: The interaction object.
    """
    log.info(
        f"User ({interaction.user.id}) is setting their nightreign category for their guild."
    )

    guild = interaction.guild
    if not guild:
        log.error("Could not determine the guild.")
        await interaction.response.send_message(
            "FAILURE: Could not determine the guild."
        )
        return

    category_id = int(nightreign_category)
    category = guild.get_channel(category_id)
    if not category or not isinstance(category, CategoryChannel):
        log.error("Category not found.")
        await interaction.response.send_message("FAILURE: Category not found.")
        return

    guild_config.add_config(guild_id=guild.id, category_id=category.id)
    await interaction.response.send_message(
        f"Nightreign category set to {category.mention}."
    )

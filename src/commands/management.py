"""This module contains the management commands for the project."""

import sys

from discord import Interaction
from discord.app_commands import Group

from src import app_config, guild_config, nightreign_service

group = Group(name="manage", description="Management commands.")


@group.command(name="save", description="Save the data.")
async def save(interaction: Interaction) -> None:
    """
    Save the data.

    Args:
        interaction: The interaction object.
    """
    if interaction.user.id != app_config.get_bot_owner_id():
        await interaction.response.send_message(
            "You are not authorized to use this command."
        )
        return

    await interaction.response.send_message("Saving data...")
    nightreign_service.save()
    guild_config.save()
    await interaction.followup.send("Data saved.")


@group.command(name="shutdown", description="Safely shutdown the bot.")
async def shutdown(interaction: Interaction) -> None:
    """
    Safely shutdown the bot.

    Args:
        interaction: The interaction object.
    """
    if interaction.user.id != app_config.get_bot_owner_id():
        await interaction.response.send_message(
            "You are not authorized to use this command."
        )
        return

    await interaction.response.send_message("Cleaning up...")
    await nightreign_service.clean(interaction.client)

    await interaction.followup.send("Saving data...")
    nightreign_service.save()
    guild_config.save()

    await interaction.followup.send("Shutting down...")
    await interaction.client.close()
    sys.exit(0)

"""This module contains the help commands."""

import logging

from discord import Interaction
from discord.app_commands import Group

log = logging.getLogger(__name__)
group = Group(name="help", description="Commands for help.")

VERSION = open("version.txt").read().strip()


@group.command(name="version", description="Get the version of the bot.")
async def version(interaction: Interaction) -> None:
    """
    Command to get the version of the bot.

    Args:
        interaction: The interaction object.
    """
    await interaction.response.send_message(
        f"Version {VERSION}\nDisclaimer: Fromcord is still in early development."
    )


NIGHTREIGN_HELP = """Nightreign commands:
- /nightreign create [session_id] [privacy] - Create a new session and channel.
- /nightreign join [session_id] - Join a session that was created, can not join private sessions.
- /nightreign add [user] - Add a user to a session, only way to add others to private sessions.
- /nightreign leave - Leave a session.
"""


@group.command(name="nightreign", description="Commands for elden ring nightreign.")
async def nightreign(interaction: Interaction) -> None:
    """
    Command to get help for the nightreign commands.

    Args:
        interaction: The interaction object.
    """
    await interaction.response.send_message(NIGHTREIGN_HELP)

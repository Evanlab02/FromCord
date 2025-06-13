"""This module contains the commands for nightreign."""

import logging
from typing import Literal
from uuid import uuid4

from discord import Interaction
from discord.app_commands import Group

from src import nightreign_service as service

log = logging.getLogger(__name__)
group = Group(name="nightreign", description="Commands for elden ring nightreign.")

GUILD_ERROR = "Could not determine the guild."
GUILD_FAILURE = f"FAILURE: {GUILD_ERROR}"


@group.command(name="create", description="Create a session.")
async def create(
    interaction: Interaction,
    session_id: str | None = None,
    privacy: Literal["public", "private"] | None = None,
) -> None:
    """
    Command to create a session.

    Args:
        interaction: The interaction object.
        session_id: The session ID.
        session_pw: The session password.
        privacy: The privacy of the session (public or private).
    """
    log.info(
        f"User ({interaction.user.id}) is creating a session with ID {session_id}."
    )
    session_pw = uuid4().hex

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    if not session_id:
        session_id = uuid4().hex

    if not privacy:
        privacy = "private"

    await interaction.response.send_message(f"Creating session (ID: {session_id})...")
    result = await service.create(
        interaction=interaction,
        guild=guild,
        session_id=session_id,
        session_pw=session_pw,
        privacy=privacy,
    )

    if result:
        await interaction.followup.send(
            f"Session created successfully! (ID: {session_id})"
        )
    else:
        await interaction.followup.send("FAILURE: Could not create session.")


@group.command(name="join", description="Join a session.")
async def join(interaction: Interaction, session_id: str) -> None:
    """
    Command to join a session.

    Args:
        interaction: The interaction object.
        session_id: The session ID.
    """
    log.info(f"User ({interaction.user.id}) is joining a session with ID {session_id}.")

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    result = await service.join(
        interaction=interaction,
        session_id=session_id,
        guild=guild,
    )

    if result:
        await interaction.response.send_message(
            f"Session joined successfully! (ID: {session_id})"
        )
    else:
        await interaction.response.send_message("FAILURE: Could not join session.")


@group.command(name="add", description="Add a user to a session.")
async def add(interaction: Interaction, user: str) -> None:
    """
    Command to add a user to a session.

    Args:
        interaction: The interaction object.
        user: A string version of the user id.
    """
    log.info(f"User ({interaction.user.id}) is adding user ({user}) to a session.")
    user_id = int(user)

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    result, mention = await service.add(
        interaction=interaction,
        guild=guild,
        user_id=user_id,
    )

    if result:
        await interaction.response.send_message(f"User added to session: {mention}")
    else:
        await interaction.response.send_message(
            "FAILURE: Could not add user to session."
        )


@group.command(name="leave", description="Leave a session.")
async def leave(interaction: Interaction) -> None:
    """
    Command to leave a session.

    Args:
        interaction: The interaction object.
    """
    log.info(f"User ({interaction.user.id}) is leaving a session.")

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    result, session_id = await service.leave(interaction=interaction, guild=guild)

    if result:
        await interaction.response.send_message(
            f"{interaction.user.mention} left the session."
        )
        await interaction.user.send(f"Left session (ID: {session_id})")
    else:
        await interaction.response.send_message("FAILURE: Could not leave session.")


@group.command(name="list", description="List all sessions.")
async def list(interaction: Interaction) -> None:
    """
    Command to list all sessions.

    Args:
        interaction: The interaction object.
    """
    log.info(f"User ({interaction.user.id}) is listing all sessions.")

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    sessions = service.list(guild)
    await interaction.response.send_message(f"```\n{sessions}\n```")


@group.command(name="start", description="Start a session.")
async def start(interaction: Interaction, day: Literal[1, 2]) -> None:
    """
    Command to start a session.

    Args:
        interaction: The interaction object.
        day: The day of the run.
    """
    log.info(f"User ({interaction.user.id}) is starting a session for day {day}.")

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    result = await service.start(interaction=interaction, guild=guild, day=day)

    if not result:
        await interaction.response.send_message("FAILURE: Could not start session.")


@group.command(name="close", description="Close a session.")
async def close(interaction: Interaction) -> None:
    """
    Command to close a session.

    Args:
        interaction: The interaction object.
        session_id: The session ID.
    """
    log.info(f"User ({interaction.user.id}) is closing a session.")

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    result, session_id = await service.close(interaction=interaction, guild=guild)

    if result:
        await interaction.user.send(f"Session closed successfully! (ID: {session_id})")
    else:
        await interaction.user.send("FAILURE: Could not close session.")


@group.command(name="boss", description="Set the boss for a session.")
async def boss(
    interaction: Interaction,
    boss: Literal[
        "Tricephalos",
        "Gaping Jaw",
        "Sentient Pest",
        "Augur",
        "Equilibrious Beast",
        "Darkdrift Knight",
        "Fissure In The Fog",
        "Night Aspect",
    ],
) -> None:
    """
    Command to set the boss for a session.

    Args:
        interaction: The interaction object.
        boss: The boss to set for the session.
    """
    log.info(f"User ({interaction.user.id}) is setting the boss for a session.")

    guild = interaction.guild
    if not guild:
        log.error(GUILD_ERROR)
        await interaction.response.send_message(GUILD_FAILURE)
        return

    result = await service.set_boss(interaction=interaction, guild=guild, boss=boss)

    if result:
        await interaction.response.send_message(f"Boss set to {boss}.")
    else:
        await interaction.response.send_message("FAILURE: Could not set boss.")

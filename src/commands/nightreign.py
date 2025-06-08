"""
This module contains the commands for the project.
"""

import json
import logging
import os

from uuid import uuid4

from discord import Interaction, PermissionOverwrite, TextChannel
from discord.app_commands import Group

NIGHTREIGN_GUILD_CATEGORY = int(os.getenv("NIGHTREIGN_GUILD_CATEGORY", 0))
GUILD_FAILURE_MESSAGE = "FAILURE: Could not determine the guild."
INCORRECT_CATEGORY_CHANNEL_MESSAGE = "FAILURE: Could not determine the category."
INCORRECT_SESSION_MESSAGE = "FAILURE: This is not a nightreign session."
SESSIONS_FILE = "data/sessions.json"

log = logging.getLogger(__name__)
group = Group(name="nightreign", description="Nightreign commands")


@group.command(name="create", description="Create a new nightreign session")
async def create(interaction: Interaction):
    """
    This is the command to create a new nightreign session.
    """
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message(GUILD_FAILURE_MESSAGE)
        return

    session_id = uuid4().hex
    await interaction.response.send_message(
        f"Creating Nightreign Session (Session ID: {session_id}) ..."
    )
    channel = await guild.create_text_channel(
        name=f"nightreign-{session_id}",
        overwrites={
            guild.default_role: PermissionOverwrite(read_messages=False),
            guild.me: PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.user: PermissionOverwrite(read_messages=True, send_messages=True),  # type: ignore # noqa: E501
        },
        category=guild.get_channel(NIGHTREIGN_GUILD_CATEGORY),  # type: ignore
    )

    data: dict = {}
    with open(SESSIONS_FILE, "r") as f:
        data = json.load(f)

    data[session_id] = {
        "session_id": session_id,
        "channel": channel.id,
        "members": [interaction.user.id],
    }

    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await channel.send(f"Welcome to the Nightreign Session\n\nSession Information:\nID: {session_id}\nChannel: {channel.mention}\nMembers: [{interaction.user.mention}]")  # noqa: E501


@group.command(name="join", description="Join a nightreign session")
async def join(interaction: Interaction, session_id: str):
    """
    This is the command to join a nightreign session.
    """
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message(GUILD_FAILURE_MESSAGE)
        return

    data: dict = {}
    with open(SESSIONS_FILE, "r") as f:
        data = json.load(f)

    if len(data[session_id]["members"]) >= 3:
        await interaction.response.send_message("FAILURE: This session is full.")
        return

    channel_id = data[session_id]["channel"]
    channel: TextChannel | None = guild.get_channel(channel_id)  # type: ignore
    if not channel:
        await interaction.response.send_message(INCORRECT_CATEGORY_CHANNEL_MESSAGE)  # noqa: E501
        return

    if interaction.user.id in data[session_id]["members"]:
        await interaction.response.send_message("FAILURE: You are already in this session.")
        return

    await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)  # type: ignore # noqa: E501
    await channel.send(f"{interaction.user.mention} has joined the session.")

    data[session_id]["members"].append(interaction.user.id)

    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message("You have joined the session.")


@group.command(name="add", description="Add a user to a nightreign session")
async def add(interaction: Interaction, user_id: str):
    """
    This is the command to add a user to a nightreign session.
    """
    user = int(user_id)

    guild = interaction.guild
    if not guild:
        await interaction.response.send_message(GUILD_FAILURE_MESSAGE)
        return

    channel: TextChannel = interaction.channel  # type: ignore
    category = channel.category   # type: ignore

    if not category or not channel:
        await interaction.response.send_message(INCORRECT_CATEGORY_CHANNEL_MESSAGE)  # noqa: E501
        return

    if category.id != NIGHTREIGN_GUILD_CATEGORY:
        await interaction.response.send_message(INCORRECT_SESSION_MESSAGE)
        return

    if not channel.name.startswith("nightreign-"):
        await interaction.response.send_message(INCORRECT_SESSION_MESSAGE)
        return

    data: dict = {}
    with open(SESSIONS_FILE, "r") as f:
        data = json.load(f)

    session_id = channel.name.replace("nightreign-", "")
    session_data = data[session_id]

    if len(session_data["members"]) >= 3:
        await interaction.response.send_message("FAILURE: This session is full.")
        return

    if user in session_data["members"]:
        await interaction.response.send_message("FAILURE: This user is already in the session.")
        return

    member = guild.get_member(user)
    if not member:
        await interaction.response.send_message("FAILURE: Could not determine the user.")
        return

    await channel.set_permissions(member, read_messages=True, send_messages=True)  # type: ignore # noqa: E501
    await channel.send(f"{member.mention} has been added to the session.")

    data[session_id]["members"].append(member.id)

    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)


@group.command(name="close", description="Close a nightreign session")
async def close(interaction: Interaction):
    """
    This is the command to close a nightreign session.
    """
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message(GUILD_FAILURE_MESSAGE)
        return

    channel: TextChannel = interaction.channel  # type: ignore
    category = channel.category   # type: ignore

    if not category or not channel:
        await interaction.response.send_message(INCORRECT_CATEGORY_CHANNEL_MESSAGE)  # noqa: E501
        return

    if category.id != NIGHTREIGN_GUILD_CATEGORY:
        await interaction.response.send_message(INCORRECT_SESSION_MESSAGE)
        return

    if not channel.name.startswith("nightreign-"):
        await interaction.response.send_message(INCORRECT_SESSION_MESSAGE)
        return

    session_id = channel.name.replace("nightreign-", "")
    await channel.delete()
    await interaction.user.send(f"Nightreign session {session_id} closed.")  # noqa: E501

    data: dict = {}
    with open(SESSIONS_FILE, "r") as f:
        data = json.load(f)

    data.pop(session_id)

    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)


@group.command(name="prepare", description="Prepare a nightreign session")
async def prepare(interaction: Interaction):
    """
    This is the command to prepare a nightreign session.
    """
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message(GUILD_FAILURE_MESSAGE)
        return

    channel: TextChannel = interaction.channel  # type: ignore
    category = channel.category   # type: ignore

    if not category or not channel:
        await interaction.response.send_message(INCORRECT_CATEGORY_CHANNEL_MESSAGE)  # noqa: E501
        return

    if category.id != NIGHTREIGN_GUILD_CATEGORY:
        await interaction.response.send_message(INCORRECT_SESSION_MESSAGE)
        return

    if not channel.name.startswith("nightreign-"):
        await interaction.response.send_message(INCORRECT_SESSION_MESSAGE)
        return

    session_id = channel.name.replace("nightreign-", "")

    data: dict = {}
    with open(SESSIONS_FILE, "r") as f:
        data = json.load(f)

    data[session_id]["prepare"] = True

    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message("Nightreign session prepared. Type in !run in the channel to start the run on fromcord.")  # noqa: E501

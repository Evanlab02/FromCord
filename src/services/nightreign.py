"""This module contains the Nightreign service."""

import logging
from datetime import datetime
from typing import Literal

from discord import (
    CategoryChannel,
    Client,
    Guild,
    Interaction,
    PermissionOverwrite,
    TextChannel,
)
from tabulate import tabulate

from src.config.interfaces import IAppConfigManager, IGuildConfigManager
from src.data import FileManager
from src.errors import FileError
from src.schemas import Session


class NightreignService:
    """This class contains the Nightreign service."""

    def __init__(
        self,
        app_config: IAppConfigManager,
        guild_config: IGuildConfigManager,
    ) -> None:
        """Initialize the Nightreign service."""
        self.log = logging.getLogger(__name__)
        self.file = FileManager(file_path="data/sessions.json")
        self.data: dict[str, Session] = {}
        self.app_config = app_config
        self.guild_config = guild_config

    def on_ready(self) -> None:
        """Call when the client is ready."""
        self.file.on_ready()

        self.log.info("Loading sessions into memory...")
        self.load()

        self.log.info("Nightreign Service Info:")
        self.log.info(f"==> File: {self.file.file}")
        self.log.info(f"==> Sessions: {len(self.data)}")
        self.log.info("Nightreign Service is ready.")

    def load(self) -> None:
        """Load the sessions into memory."""
        try:
            file_data = self.file.read()
        except Exception as error:
            self.log.warning(f"Error loading sessions: {error}")
            self.log.warning("Resetting sessions.")
            self.data = {}
            return

        if not isinstance(file_data, dict):
            raise FileError("Sessions file is not in the correct format.")

        for session_id, session in file_data.items():
            self.data[session_id] = Session(**session)

    def save(self) -> None:
        """Save the sessions to the file."""
        file_data = {}
        for session_id, session in self.data.items():
            file_data[session_id] = session.model_dump()
        self.file.write(file_data)

    async def clean(self, client: Client) -> None:
        """Clean up the sessions."""
        copy = self.data.copy()
        for session_id, session in copy.items():
            guild = client.get_guild(session.guild_id)
            if not guild:
                self.data.pop(session_id)
                continue

            channel = guild.get_channel(session.channel_id)
            if not channel:
                self.data.pop(session_id)
                continue

            guild_category = self.guild_config.get_config(
                guild.id
            ).nightreign_category_id
            category = channel.category
            if not category or category.id != guild_category:
                await channel.delete()
                self.data.pop(session_id)
                continue

            if len(session.members) == 0:
                await channel.delete()
                self.data.pop(session_id)

    async def create(
        self,
        interaction: Interaction,
        guild: Guild,
        session_id: str,
        session_pw: str,
        privacy: Literal["public", "private"],
    ) -> bool:
        """Create a new session."""
        user = interaction.user
        guild_config = self.guild_config.get_config(guild.id)
        category = guild.get_channel(guild_config.nightreign_category_id)

        if not category or not isinstance(category, CategoryChannel):
            return False

        if session_id in self.data:
            return False

        channel = await guild.create_text_channel(
            name=f"nightreign-{session_id}",
            category=category,
            overwrites={
                guild.default_role: PermissionOverwrite(read_messages=False),
                guild.me: PermissionOverwrite(read_messages=True, send_messages=True),
                user: PermissionOverwrite(read_messages=True, send_messages=True),  # type: ignore
            },
        )

        self.data[session_id] = Session(
            session_id=session_id,
            session_pw=session_pw,
            privacy=privacy,
            members=[user.id],
            channel_id=channel.id,
            guild_id=guild.id,
            active=False,
            day=0,
            timestamp=0,
            event_log=[],
            event_log_id=0,
        )

        await channel.send(
            "Welcome to the Nightreign session!\n"
            f"ID: {session_id}\n"
            f"Privacy: {privacy}\n"
            f"Channel: {channel.mention}\n"
            f"Members: [{user.mention}]"
        )

        return True

    async def join(
        self, interaction: Interaction, session_id: str, guild: Guild
    ) -> bool:
        """
        Join a session.

        Args:
            interaction: The interaction object.
            session_id: The ID of the session.

        Returns:
            True if the session was joined, otherwise False.
        """
        session = self.get(session_id)
        if not session:
            return False

        if session.guild_id != guild.id:
            return False

        if session.privacy == "private":
            return False

        if interaction.user.id in session.members:
            return False

        if len(session.members) >= 3:
            return False

        channel = guild.get_channel(session.channel_id)
        if not channel:
            return False

        if not isinstance(channel, TextChannel):
            return False

        await channel.set_permissions(
            interaction.user,  # type: ignore
            read_messages=True,
            send_messages=True,
        )

        session.members.append(interaction.user.id)

        members = [guild.get_member(member) for member in session.members]
        member_names = [member.name for member in members if member]

        await channel.send(
            f"{interaction.user.mention} joined the session.\n"
            f"Members: {', '.join(member_names)}"
        )

        return True

    async def add(
        self, interaction: Interaction, guild: Guild, user_id: int
    ) -> tuple[bool, str]:
        """
        Add a user to a session.

        Args:
            interaction: The interaction object.
            session_id: The ID of the session.
            guild: The guild object.
            user_id: The ID of the user to add.

        Returns:
            A tuple containing a boolean indicating success and the mention of the added user.
        """
        channel = interaction.channel
        if not channel:
            return False, ""

        if not isinstance(channel, TextChannel):
            return False, ""

        session_id = channel.name.split("-")[-1]
        session = self.get(session_id)
        if not session:
            return False, ""

        if session.guild_id != guild.id:
            return False, ""

        if session.channel_id != channel.id:
            return False, ""

        if user_id in session.members:
            return False, ""

        if len(session.members) >= 3:
            return False, ""

        member = guild.get_member(user_id)
        if not member:
            return False, ""

        await channel.set_permissions(
            member,
            read_messages=True,
            send_messages=True,
        )

        members = [guild.get_member(member) for member in session.members]
        member_names = [member.name for member in members if member]

        await channel.send(
            f"{member.mention} added to the session.\n"
            f"Members: {', '.join(member_names)}"
        )

        session.members.append(member.id)

        return True, member.mention

    async def leave(self, interaction: Interaction, guild: Guild) -> tuple[bool, str]:
        """
        Leave a session.

        Args:
            interaction: The interaction object.
            guild: The guild object.

        Returns:
            A tuple containing a boolean indicating success and the mention of the left user.
        """
        channel = interaction.channel
        if not channel:
            return False, ""

        if not isinstance(channel, TextChannel):
            return False, ""

        session_id = channel.name.split("-")[-1]
        session = self.get(session_id)
        if not session:
            return False, ""

        if session.guild_id != guild.id:
            return False, ""

        if session.channel_id != channel.id:
            return False, ""

        if interaction.user.id not in session.members:
            return False, ""

        channel = guild.get_channel(session.channel_id)
        if not channel:
            return False, ""

        if not isinstance(channel, TextChannel):
            return False, ""

        await channel.set_permissions(
            interaction.user,  # type: ignore
            read_messages=False,
            send_messages=False,
        )

        session.members.remove(interaction.user.id)

        return True, session.session_id

    async def remove(
        self, interaction: Interaction, guild: Guild, user_id: int
    ) -> tuple[bool, str]:
        """
        Remove a user from a session.

        Args:
            interaction: The interaction object.
            guild: The guild object.
            user_id: The ID of the user to remove.

        Returns:
            A tuple containing a boolean indicating success and the mention of the removed user.
        """
        channel = interaction.channel
        if not channel:
            return False, ""

        if not isinstance(channel, TextChannel):
            return False, ""

        session_id = channel.name.split("-")[-1]
        session = self.get(session_id)
        if not session:
            return False, ""

        if session.guild_id != guild.id:
            return False, ""

        if session.channel_id != channel.id:
            return False, ""

        if user_id not in session.members:
            return False, ""

        member = guild.get_member(user_id)
        if not member:
            return False, ""

        await channel.set_permissions(
            member,
            read_messages=False,
            send_messages=False,
        )

        session.members.remove(user_id)

        return True, member.mention

    def list(self, guild: Guild) -> str:
        """
        List all sessions.

        Args:
            guild: The guild object.
        """
        sessions = []
        for session in self.data.values():
            if session.guild_id != guild.id or session.privacy == "private":
                continue

            members = [guild.get_member(member) for member in session.members]
            member_names = [member.name for member in members if member]
            sessions.append([session.session_id, f"Members: {', '.join(member_names)}"])

        if not sessions:
            return "No sessions found."

        return tabulate(
            sessions, headers=["Session ID", "Members"], tablefmt="rounded_grid"
        )

    def get(self, session_id: str) -> Session | None:
        """
        Get a session by ID.

        Args:
            session_id: The ID of the session.

        Returns:
            The session if found, otherwise None.
        """
        return self.data.get(session_id)

    async def start(
        self, interaction: Interaction, guild: Guild, day: Literal[1, 2]
    ) -> bool:
        """
        Start a session.

        Args:
            interaction: The interaction object.
            guild: The guild object.
            day: Which day of the run you are on.

        Returns:
            True if the session was started, otherwise False.
        """
        channel = interaction.channel
        if not channel:
            return False

        if not isinstance(channel, TextChannel):
            return False

        session_id = channel.name.split("-")[-1]
        session = self.get(session_id)
        if not session:
            return False

        if session.guild_id != guild.id:
            return False

        if channel.id != session.channel_id:
            return False

        if interaction.user.id not in session.members:
            return False

        session.day = day
        session.timestamp = datetime.now().timestamp()
        session.active = True
        await interaction.response.send_message(
            "Starting the fight against the nightlords!\nGood luck and have fun!\n"
        )

        session.event_log.append(
            [str(day), "INFO", "Started the run", datetime.now().isoformat()]
        )
        table = tabulate(
            session.event_log,
            headers=["Day", "Type", "Event", "Timestamp"],
            tablefmt="rounded_grid",
        )
        message = await channel.send(f"```\n{table}\n```")
        session.event_log_id = message.id
        return True

    async def close(self, interaction: Interaction, guild: Guild) -> tuple[bool, str]:
        """
        Close a session.

        Args:
            interaction: The interaction object.
            guild: The guild object.
        """
        channel = interaction.channel
        if not channel:
            return False, ""

        if not isinstance(channel, TextChannel):
            return False, ""

        session_id = channel.name.split("-")[-1]
        session = self.get(session_id)
        if not session:
            return False, ""

        if session.guild_id != guild.id:
            return False, ""

        if session.channel_id != channel.id:
            return False, ""

        if interaction.user.id not in session.members:
            return False, ""

        await channel.delete()
        self.data.pop(session_id)

        return True, session_id

    async def set_boss(
        self,
        interaction: Interaction,
        guild: Guild,
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
    ) -> bool:
        """
        Set the boss for a session.

        Args:
            interaction: The interaction object.
            guild: The guild object.
            boss: The boss to set for the session.
        """
        channel = interaction.channel
        if not channel:
            return False

        if not isinstance(channel, TextChannel):
            return False

        session_id = channel.name.split("-")[-1]
        session = self.get(session_id)
        if not session:
            return False

        if session.guild_id != guild.id:
            return False

        if session.channel_id != channel.id:
            return False

        if interaction.user.id not in session.members:
            return False

        session.boss = boss
        return True

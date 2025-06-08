"""
This module contains the client for the project.
"""

import json
import logging
import os

from datetime import datetime

from discord import Client, Message, Object, TextChannel
from discord.app_commands import CommandTree
from discord.ext import tasks

SESSIONS_FILE = "data/sessions.json"


class FromCordClient(Client):
    """
    This is the client for the project.
    """

    def __init__(self, *args, **kwargs):
        """
        This is the constructor for the client.
        """
        self.log = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)
        self.primary_guild_id = int(os.getenv("PRIMARY_GUILD", 0))
        self.tree = None

    def set_tree(self, tree: CommandTree | None):
        """
        This is the method to set the command tree.
        """
        self.tree = tree

    async def on_ready(self):
        """
        This is the event handler for the on_ready event.
        """
        self.log.info(f'Logged on as {self.user}!')
        self.log.info(f"Primary guild ID: {self.primary_guild_id}")
        self.log.info('Syncing commands...')
        await self.tree.sync(guild=Object(id=self.primary_guild_id))
        await self.tree.sync()
        self.log.info('Commands synced.')
        self.core_sessions.start()

    async def on_message(self, message: Message):
        """
        This is the event handler for the on_message event.
        """
        CATEGORY_ID = int(os.getenv("NIGHTREIGN_GUILD_CATEGORY", 0))

        if message.author.bot:
            return

        try:
            category = message.channel.category  # type: ignore

            if not category or category.id != CATEGORY_ID:
                return

            if message.content.startswith("!run"):
                session_id = message.channel.name.replace("nightreign-", "")  # type: ignore
                data: dict = {}
                with open(SESSIONS_FILE, "r") as f:
                    data = json.load(f)

                if data[session_id]["prepare"]:
                    data[session_id]["active"] = True
                    data[session_id]["timestamp"] = datetime.now().timestamp()

                    with open(SESSIONS_FILE, "w") as f:
                        json.dump(data, f, indent=4)

                    await message.channel.send("Starting the fight against the Night Lord!\nGood luck & have fun!")  # noqa: E501
                    await message.channel.send("Guideline: You should now be level 1.")
        except Exception:
            return

    @tasks.loop(seconds=5)
    async def core_sessions(self) -> None:
        """
        This is the task to check the sessions.
        """
        self.log.info("Checking sessions...")
        data: dict = {}
        with open(SESSIONS_FILE, "r") as f:
            data = json.load(f)

        for _, session_data in data.items():
            if session_data.get("active", False):
                timestamp = session_data["timestamp"]
                start_time = datetime.fromtimestamp(timestamp)
                now = datetime.now()
                diff = now - start_time
                diff_seconds = diff.total_seconds()
                diff_minutes = diff_seconds / 60

                day1_ring1_start_warning_1 = session_data.get("day1_ring1_start_warning_1", None)
                if diff_minutes >= 3.5 and not day1_ring1_start_warning_1:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 1 is closing in approximately 1 minute.")
                    session_data["day1_ring1_start_warning_1"] = True
                    continue

                day1_ring1_start_warning_2 = session_data.get("day1_ring1_start_warning_2", None)
                if diff_minutes >= 4 and not day1_ring1_start_warning_2:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 1 is closing in approximately 30 seconds.")
                    session_data["day1_ring1_start_warning_2"] = True
                    continue

                day1_ring1_start_warning_3 = session_data.get("day1_ring1_start_warning_3", None)
                if diff_minutes >= 4.25 and not day1_ring1_start_warning_3:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 1 is closing in approximately 15 seconds.")
                    session_data["day1_ring1_start_warning_3"] = True
                    continue

                day1_ring1_start_warning_4 = session_data.get("day1_ring1_start_warning_4", None)
                if diff_minutes >= 4.5 and not day1_ring1_start_warning_4:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 1 is closing...")
                    session_data["day1_ring1_start_warning_4"] = True
                    continue

                day1_ring1_complete = session_data.get("day1_ring1_complete", None)
                if diff_minutes >= 7.5 and not day1_ring1_complete:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 1 is closed.")
                    session_data["day1_ring1_complete"] = True
                    continue

                day1_ring2_start_warning_1 = session_data.get("day1_ring2_start_warning_1", None)
                if diff_minutes >= 10 and not day1_ring2_start_warning_1:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 2 is closing in approximately 1 minute.")
                    session_data["day1_ring2_start_warning_1"] = True
                    continue

                day1_ring2_start_warning_2 = session_data.get("day1_ring2_start_warning_2", None)
                if diff_minutes >= 10.5 and not day1_ring2_start_warning_2:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 2 is closing in approximately 30 seconds.")
                    session_data["day1_ring2_start_warning_2"] = True
                    continue

                day1_ring2_start_warning_3 = session_data.get("day1_ring2_start_warning_3", None)
                if diff_minutes >= 10.75 and not day1_ring2_start_warning_3:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 2 is closing in approximately 15 seconds.")
                    session_data["day1_ring2_start_warning_3"] = True
                    continue

                day1_ring2_start_warning_4 = session_data.get("day1_ring2_start_warning_4", None)
                if diff_minutes >= 11 and not day1_ring2_start_warning_4:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 2 is closing...")
                    session_data["day1_ring2_start_warning_4"] = True
                    continue

                day1_ring2_complete = session_data.get("day1_ring2_complete", None)
                if diff_minutes >= 14 and not day1_ring2_complete:
                    channel_id = session_data["channel"]
                    channel: TextChannel = self.get_channel(channel_id)  # type: ignore
                    if channel:
                        await channel.send("Ring 2 is closed.")
                        await channel.send("Taking on the Day 1 Boss...\nGood luck & have fun!")
                    session_data["day1_ring2_complete"] = True

        with open(SESSIONS_FILE, "w") as f:
            json.dump(data, f, indent=4)

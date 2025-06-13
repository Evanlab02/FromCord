"""This module contains the primary client for the project."""

import logging
import sys

from discord import Client, Object
from discord.app_commands import CommandTree, Group
from discord.ext import tasks

from src import INTENTS, app_config, guild_config, nightreign_service
from src.commands import (
    CONFIG_COMMAND_GROUP,
    HELP_COMMAND_GROUP,
    MANAGEMENT_COMMAND_GROUP,
    NIGHTREIGN_COMMAND_GROUP,
)
from src.config.interfaces import IAppConfigManager, IGuildConfigManager
from src.services import NightreignService
from src.tasks.nightreign import check_sessions


class FromCordClient(Client):
    """This is the primary discord client for the project."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        """Initialize the client."""
        self.log = logging.getLogger(__name__)
        self.app_config: IAppConfigManager = kwargs.pop("app_config")
        self.guild_config: IGuildConfigManager = kwargs.pop("guild_config")
        self.nightreign_service: NightreignService = kwargs.pop("nightreign_service")
        self.tree: CommandTree | None = None
        self.save_counter: int = 0
        super().__init__(*args, **kwargs)

    async def on_ready(self) -> None:
        """Event handler for the on_ready event."""
        if not self.tree:
            self.log.error("Tree is not set.")
            sys.exit(1)

        self.log.info(f"Logged on as {self.user}!")
        self.app_config.on_ready()
        self.guild_config.on_ready()
        self.nightreign_service.on_ready()
        self.clean_and_save.start()
        self.nightreign_loop.start()

        self.log.info("Loading tree...")
        commands = self.tree.get_commands()
        self.log.info(f"Loaded {len(commands)} commands/groups.")

        for command in commands:
            if isinstance(command, Group):
                self.log.info(f"==> Group: {command.name} - {command.description}")
                for subcommand in command.commands:
                    self.log.info(f"===> {subcommand.name} - {subcommand.description}")

        self.log.info("Syncing primary guild commands...")
        await self.tree.sync(guild=Object(id=self.app_config.get_primary_guild_id()))
        await self.tree.sync(guild=Object(id=self.app_config.get_primary_guild_id()))

        self.log.info("Syncing commands...")
        await self.tree.sync()
        await self.tree.sync()

        self.log.info("Commands synced.")

    def set_tree(self, tree: CommandTree) -> None:
        """Set the tree."""
        self.tree = tree

    @tasks.loop(seconds=5)
    async def nightreign_loop(self) -> None:
        """Task to check the sessions for the nightreign service."""
        await check_sessions(self)

    @tasks.loop(minutes=5)
    async def clean_and_save(self) -> None:
        """Task to save the files periodically."""
        self.save_counter += 1
        if self.save_counter == 1:
            self.log.info("[TASK] Skipping first save...")
            return

        self.log.info("[TASK] Cleaning up the sessions...")
        await self.nightreign_service.clean(self)

        self.log.info("[TASK] Saving all in-memory data to files...")
        self.guild_config.save()
        self.nightreign_service.save()


CLIENT = FromCordClient(
    intents=INTENTS,
    app_config=app_config,
    guild_config=guild_config,
    nightreign_service=nightreign_service,
)

TREE = CommandTree(CLIENT)
TREE.add_command(CONFIG_COMMAND_GROUP)
TREE.add_command(HELP_COMMAND_GROUP)
TREE.add_command(MANAGEMENT_COMMAND_GROUP)
TREE.add_command(NIGHTREIGN_COMMAND_GROUP)

CLIENT.set_tree(TREE)

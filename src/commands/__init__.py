"""
This module contains the commands for the project.
"""

from discord.app_commands import CommandTree

from src import CLIENT
from src.commands.nightreign import group as NR_GROUP

tree = CommandTree(CLIENT)
tree.add_command(NR_GROUP)

__all__ = ["tree"]

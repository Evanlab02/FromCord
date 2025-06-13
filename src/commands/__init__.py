"""This module contains the commands for the project."""

from src.commands.config import group as CONFIG_COMMAND_GROUP
from src.commands.help import group as HELP_COMMAND_GROUP
from src.commands.management import group as MANAGEMENT_COMMAND_GROUP
from src.commands.nightreign import group as NIGHTREIGN_COMMAND_GROUP

__all__ = [
    "CONFIG_COMMAND_GROUP",
    "HELP_COMMAND_GROUP",
    "MANAGEMENT_COMMAND_GROUP",
    "NIGHTREIGN_COMMAND_GROUP",
]

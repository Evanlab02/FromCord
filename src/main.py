"""
This is the main module for the project.
"""

import os
import logging

from src import CLIENT
from src.commands import tree

TOKEN = os.getenv("BOT_TOKEN", "")
CLIENT.set_tree(tree)
CLIENT.run(TOKEN, log_level=logging.INFO, root_logger=True)

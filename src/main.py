"""This is the main module for the project."""

import logging

from src import TOKEN
from src.client import CLIENT

if __name__ == "__main__":
    CLIENT.run(TOKEN, log_level=logging.INFO, root_logger=True)

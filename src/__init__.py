"""
This is the entry point for the project.
"""

from dotenv import load_dotenv

from discord import Intents

from src.client import FromCordClient

load_dotenv()

INTENTS = Intents.all()
CLIENT = FromCordClient(intents=INTENTS)

__all__ = ["CLIENT"]

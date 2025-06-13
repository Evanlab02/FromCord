"""This module contains the schemas for the sessions."""

from typing import Literal

from pydantic import BaseModel


class SessionFlag(BaseModel):
    """A session flag."""

    ROUND_1_WARNING_1: bool = False
    ROUND_1_WARNING_2: bool = False
    ROUND_1_WARNING_3: bool = False
    ROUND_1_ANNOUNCEMENT: bool = False
    ROUND_1_CLOSED: bool = False
    ROUND_2_WARNING_1: bool = False
    ROUND_2_WARNING_2: bool = False
    ROUND_2_WARNING_3: bool = False
    ROUND_2_ANNOUNCEMENT: bool = False
    ROUND_2_CLOSED: bool = False
    LEVEL_5_7: bool = False
    LEVEL_10_12: bool = False


class Session(BaseModel):
    """A session."""

    session_id: str
    session_pw: str
    privacy: Literal["public", "private"]
    members: list[int]
    active: bool
    day: Literal[0, 1, 2]
    timestamp: float
    channel_id: int
    guild_id: int
    event_log: list[list[str]]
    event_log_id: int
    flags: SessionFlag = SessionFlag()

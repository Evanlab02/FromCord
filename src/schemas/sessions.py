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
    TRICEPHALOS_DAY_1: bool = False
    TRICEPHALOS_DAY_2: bool = False
    GAPING_JAW_DAY_1: bool = False
    GAPING_JAW_DAY_2: bool = False
    SENTIENT_PEST_DAY_1: bool = False
    SENTIENT_PEST_DAY_2: bool = False
    AUGUR_DAY_1: bool = False
    AUGUR_DAY_2: bool = False
    EQUILIBRIUM_DAY_1: bool = False
    EQUILIBRIUM_DAY_2: bool = False
    DARKDRIFT_KNIGHT_DAY_1: bool = False
    DARKDRIFT_KNIGHT_DAY_2: bool = False
    FISSURE_IN_THE_FOG_DAY_1: bool = False
    FISSURE_IN_THE_FOG_DAY_2: bool = False
    NIGHT_ASPECT_DAY_1: bool = False
    NIGHT_ASPECT_DAY_2: bool = False
    TRICEPHALOS_WEAKNESS: bool = False
    GAPING_JAW_WEAKNESS: bool = False
    SENTIENT_PEST_WEAKNESS: bool = False
    AUGUR_WEAKNESS: bool = False
    EQUILIBRIUM_WEAKNESS: bool = False
    DARKDRIFT_KNIGHT_WEAKNESS: bool = False
    FISSURE_IN_THE_FOG_WEAKNESS: bool = False
    NIGHT_ASPECT_WEAKNESS: bool = False


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
    boss: (
        Literal[
            "Tricephalos",
            "Gaping Jaw",
            "Sentient Pest",
            "Augur",
            "Equilibrious Beast",
            "Darkdrift Knight",
            "Fissure In The Fog",
            "Night Aspect",
        ]
        | None
    ) = None

"""Contains the task utilities for nightreign related functionality."""

import asyncio
import logging
from datetime import datetime

from discord import Client, TextChannel
from tabulate import tabulate

from src import nightreign_service as service
from src.schemas.sessions import Session, SessionFlag

log = logging.getLogger(__name__)

FIRST_EVENT = 3.5
SECOND_EVENT = FIRST_EVENT + 0.5
THIRD_EVENT = SECOND_EVENT + 0.25
FOURTH_EVENT = THIRD_EVENT + 0.25
FIFTH_EVENT = FOURTH_EVENT + 3
SIXTH_EVENT = FIFTH_EVENT + 2.5
SEVENTH_EVENT = SIXTH_EVENT + 0.5
EIGHTH_EVENT = SEVENTH_EVENT + 0.25
NINTH_EVENT = EIGHTH_EVENT + 0.25
TENTH_EVENT = NINTH_EVENT + 3

TRICEPHALOS = "Tricephalos"
GAPING_JAW = "Gaping Jaw"
SENTIENT_PEST = "Sentient Pest"
AUGUR = "Augur"
EQUILIBRIUM = "Equilibrious Beast"
DARKDRIFT_KNIGHT = "Darkdrift Knight"
FISSURE_IN_THE_FOG = "Fissure In The Fog"
NIGHT_ASPECT = "Night Aspect"

EVENT_CONFIG = {
    "TRICEPHALOS_WEAKNESS": {
        "time": 0.25,
        "message": "Tricephalos is weak to holy.",
        "type": "INFO",
        "day": 0,
        "boss": TRICEPHALOS,
    },
    "GAPING_JAW_WEAKNESS": {
        "time": 0.25,
        "message": "Gaping Jaw is weak to poison.",
        "type": "INFO",
        "day": 0,
        "boss": GAPING_JAW,
    },
    "SENTIENT_PEST_WEAKNESS": {
        "time": 0.25,
        "message": "Sentient Pest is weak to fire.",
        "type": "INFO",
        "day": 0,
        "boss": SENTIENT_PEST,
    },
    "AUGUR_WEAKNESS": {
        "time": 0.25,
        "message": "Augur is weak to lightning.",
        "type": "INFO",
        "day": 0,
        "boss": AUGUR,
    },
    "EQUILIBRIUM_WEAKNESS": {
        "time": 0.25,
        "message": "Equilibrious Beast is weak to madness.",
        "type": "INFO",
        "day": 0,
        "boss": EQUILIBRIUM,
    },
    "DARKDRIFT_KNIGHT_WEAKNESS": {
        "time": 0.25,
        "message": "Darkdrift Knight is weak to lightning.",
        "type": "INFO",
        "day": 0,
        "boss": DARKDRIFT_KNIGHT,
    },
    "FISSURE_IN_THE_FOG_WEAKNESS": {
        "time": 0.25,
        "message": "Fissure In The Fog is weak to fire.",
        "type": "INFO",
        "day": 0,
        "boss": FISSURE_IN_THE_FOG,
    },
    "NIGHT_ASPECT_WEAKNESS": {
        "time": 0.25,
        "message": "Night Aspect is weak to holy.",
        "type": "INFO",
        "day": 0,
        "boss": NIGHT_ASPECT,
    },
    "TRICEPHALOS_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Bell Bearing Hunter, Demi-Humans",
        "type": "INFO",
        "day": 1,
        "boss": TRICEPHALOS,
    },
    "TRICEPHALOS_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Fell Omen, Tree Sentinel",
        "type": "INFO",
        "day": 2,
        "boss": TRICEPHALOS,
    },
    "GAPING_JAW_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Night's Cavalry x2, Valiant Gargoyle, Wormface",
        "type": "INFO",
        "day": 1,
        "boss": GAPING_JAW,
    },
    "GAPING_JAW_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Ancient Dragon, Crucible Knight/Golden Hippopotamus, Outland Commander",  # noqa: E501
        "type": "INFO",
        "day": 2,
        "boss": GAPING_JAW,
    },
    "SENTIENT_PEST_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Battlefield Commander, Centipede Demon, Smelter Demon, Tibia Mariner, Ulcerated Tree Spirit",  # noqa: E501
        "type": "INFO",
        "day": 1,
        "boss": SENTIENT_PEST,
    },
    "SENTIENT_PEST_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Draconic Tree Sentinel, Great Wyrm, Nox Dragonkin Soldier",  # noqa: E501
        "type": "INFO",
        "day": 2,
        "boss": SENTIENT_PEST,
    },
    "AUGUR_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Gaping Dragon, Grafted Monarch, Wormface",  # noqa: E501
        "type": "INFO",
        "day": 1,
        "boss": AUGUR,
    },
    "AUGUR_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Full-Grown Fallingstar Beast, Tree Sentinel",  # noqa: E501
        "type": "INFO",
        "day": 2,
        "boss": AUGUR,
    },
    "EQUILIBRIUM_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Centipede Demon, The Duke's Dear Freja, Tibia Mariner, Royal Revenant",  # noqa: E501
        "type": "INFO",
        "day": 1,
        "boss": EQUILIBRIUM,
    },
    "EQUILIBRIUM_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Crucible Knight/Golden Hippopotamus, Death Rite Bird, Godskin Duo",  # noqa: E501
        "type": "INFO",
        "day": 2,
        "boss": EQUILIBRIUM,
    },
    "DARKDRIFT_KNIGHT_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Gaping Dragon, Night's Cavalry x2, Royal Revenant, Valiant Gargoyle, Wormface",  # noqa: E501
        "type": "INFO",
        "day": 1,
        "boss": DARKDRIFT_KNIGHT,
    },
    "DARKDRIFT_KNIGHT_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Nameless King, Nox Dragonkin Soldier, Outland Commander",  # noqa: E501
        "type": "INFO",
        "day": 2,
        "boss": DARKDRIFT_KNIGHT,
    },
    "FISSURE_IN_THE_FOG_DAY_1": {
        "time": 0.5,
        "message": "Potential night 1 bosses: Grafted Monarch, Smelter Demon, The Duke's Dear Freja, Tibia Mariner, Ulcerated Tree Spirit",  # noqa: E501
        "type": "INFO",
        "day": 1,
        "boss": FISSURE_IN_THE_FOG,
    },
    "FISSURE_IN_THE_FOG_DAY_2": {
        "time": 0.5,
        "message": "Potential night 2 bosses: Dancer Of The Boreal Valley, Draconic Tree Sentinel, Godskin Duo",  # noqa: E501
        "type": "INFO",
        "day": 2,
        "boss": FISSURE_IN_THE_FOG,
    },
    "ROUND_1_WARNING_1": {
        "time": FIRST_EVENT,
        "message": "Round 1 will start closing in 1 minute.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_1_WARNING_2": {
        "time": SECOND_EVENT,
        "message": "Round 1 will start closing in 30 seconds.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_1_WARNING_3": {
        "time": THIRD_EVENT,
        "message": "Round 1 will start closing in 15 seconds.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_1_ANNOUNCEMENT": {
        "time": FOURTH_EVENT,
        "message": "Round 1 has started closing.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_1_CLOSED": {
        "time": FIFTH_EVENT,
        "message": "Round 1 has closed.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_2_WARNING_1": {
        "time": SIXTH_EVENT,
        "message": "Round 2 will start closing in 1 minute.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_2_WARNING_2": {
        "time": SEVENTH_EVENT,
        "message": "Round 2 will start closing in 30 seconds.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_2_WARNING_3": {
        "time": EIGHTH_EVENT,
        "message": "Round 2 will start closing in 15 seconds.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_2_ANNOUNCEMENT": {
        "time": NINTH_EVENT,
        "message": "Round 2 has started closing.",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "ROUND_2_CLOSED": {
        "time": TENTH_EVENT,
        "message": "Round 2 has closed.\nGood luck and have fun!",
        "type": "TIMER",
        "day": 0,
        "boss": None,
    },
    "LEVEL_5_7": {
        "time": TENTH_EVENT + 0.5,
        "message": "You should now be level 5-7.",
        "type": "GUIDELINE",
        "day": 1,
        "boss": None,
    },
    "LEVEL_10_12": {
        "time": TENTH_EVENT + 0.5,
        "message": "You should now be level 10-12.",
        "type": "GUIDELINE",
        "day": 2,
        "boss": None,
    },
}


async def process_session(client: Client, session: Session) -> None:
    """Process the session for the nightreign service."""
    try:
        session_started = datetime.fromtimestamp(session.timestamp)
        now = datetime.now()
        diff = now - session_started

        minutes = diff.total_seconds() / 60

        for flag, config in EVENT_CONFIG.items():
            time: float | None = config.get("time")  # type: ignore
            if time is None:
                continue

            day = config.get("day", 0)
            if day != 0 and session.day != day:
                continue

            boss = config.get("boss", None)
            if boss and session.boss != boss:
                continue

            if minutes >= time and not getattr(session.flags, flag):
                setattr(session.flags, flag, True)
                channel = client.get_channel(session.channel_id)
                if channel and isinstance(channel, TextChannel):
                    partial_message = channel.get_partial_message(session.event_log_id)
                    message = await partial_message.fetch()

                    if len(message.content) > 1750:
                        session.event_log = []
                        message = await channel.send("LOADING...")
                        session.event_log_id = message.id

                    session.event_log.append(
                        [
                            str(session.day),
                            config.get("type", "INFO"),  # type: ignore
                            config.get("message", ""),  # type: ignore
                            datetime.now().isoformat(),
                        ]
                    )
                    table = tabulate(
                        session.event_log,
                        headers=["Day", "Type", "Event", "Timestamp"],
                        tablefmt="rounded_grid",
                    )
                    await message.edit(content=f"```\n{table}\n```")
                    break

        service.data[session.session_id] = session
        log.info(f"[NIGHTREIGN] Session {session.session_id} processed.")
    except Exception as e:
        log.error(f"[NIGHTREIGN] Error processing session {session.session_id}: {e}")
        log.warning(
            f"[NIGHTREIGN] Session {session.session_id} will be skipped and retried later."
        )


async def check_sessions(client: Client) -> None:
    """Check the sessions for the nightreign service."""
    tasks = []
    for session in service.data.values():
        if not session.active:
            continue

        if session.day == 0:
            continue

        flags = session.flags
        for flag in SessionFlag.model_fields:
            result = getattr(flags, flag)
            close = True

            if result:
                continue
            else:
                close = False

        if close:
            log.info(
                f"[NIGHTREIGN] Marking session {session.session_id} as inactive..."
            )
            service.data[session.session_id].active = False
            service.data[session.session_id].timestamp = 0
            service.data[session.session_id].flags = SessionFlag()
        else:
            task = asyncio.create_task(process_session(client, session))
            tasks.append(task)

    if tasks:
        log.info(f"[NIGHTREIGN] Scheduling {len(tasks)} tasks...")
        await asyncio.gather(*tasks)
        log.info("[NIGHTREIGN] Tasks Completed.")

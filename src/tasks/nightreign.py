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

EVENT_CONFIG = {
    "ROUND_1_WARNING_1": {
        "time": FIRST_EVENT,
        "message": "Round 1 will start closing in 1 minute.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_1_WARNING_2": {
        "time": SECOND_EVENT,
        "message": "Round 1 will start closing in 30 seconds.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_1_WARNING_3": {
        "time": THIRD_EVENT,
        "message": "Round 1 will start closing in 15 seconds.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_1_ANNOUNCEMENT": {
        "time": FOURTH_EVENT,
        "message": "Round 1 has started closing.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_1_CLOSED": {
        "time": FIFTH_EVENT,
        "message": "Round 1 has closed.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_2_WARNING_1": {
        "time": SIXTH_EVENT,
        "message": "Round 2 will start closing in 1 minute.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_2_WARNING_2": {
        "time": SEVENTH_EVENT,
        "message": "Round 2 will start closing in 30 seconds.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_2_WARNING_3": {
        "time": EIGHTH_EVENT,
        "message": "Round 2 will start closing in 15 seconds.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_2_ANNOUNCEMENT": {
        "time": NINTH_EVENT,
        "message": "Round 2 has started closing.",
        "type": "TIMER",
        "day": 0,
    },
    "ROUND_2_CLOSED": {
        "time": TENTH_EVENT,
        "message": "Round 2 has closed.\nGood luck and have fun!",
        "type": "TIMER",
        "day": 0,
    },
    "LEVEL_5_7": {
        "time": TENTH_EVENT + 0.5,
        "message": "You should now be level 5-7.",
        "type": "GUIDELINE",
        "day": 1,
    },
    "LEVEL_10_12": {
        "time": TENTH_EVENT + 0.5,
        "message": "You should now be level 10-12.",
        "type": "GUIDELINE",
        "day": 2,
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

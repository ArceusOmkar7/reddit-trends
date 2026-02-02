from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable

logger = logging.getLogger("reddit_trends.scheduler")

_last_run: datetime | None = None
_next_run: datetime | None = None
_interval_seconds: int | None = None
_enabled: bool = True
_wake_event: asyncio.Event | None = None


def get_polling_state() -> dict[str, str | int | None]:
    return {
        "interval_seconds": _interval_seconds,
        "last_run": _last_run.isoformat() if _last_run else None,
        "next_run": _next_run.isoformat() if _next_run else None,
    }


def set_ingestion_enabled(enabled: bool) -> None:
    global _enabled
    _enabled = enabled
    if enabled and _wake_event is not None:
        _wake_event.set()


def is_ingestion_enabled() -> bool:
    return _enabled


async def run_interval(task: Callable[[], Awaitable[None]], interval: int) -> None:
    global _wake_event
    if _wake_event is None:
        _wake_event = asyncio.Event()
    while True:
        global _last_run, _next_run, _interval_seconds
        if not _enabled:
            _next_run = None
            await _wake_event.wait()
            _wake_event.clear()
            continue
        _interval_seconds = interval
        _last_run = datetime.now(tz=timezone.utc)
        _next_run = _last_run + timedelta(seconds=interval)
        logger.info("Scheduler tick", extra={"interval": interval})
        await task()
        await asyncio.sleep(interval)

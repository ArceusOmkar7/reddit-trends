from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable

logger = logging.getLogger("reddit_trends.scheduler")

_last_run: datetime | None = None
_next_run: datetime | None = None
_interval_seconds: int | None = None


def get_polling_state() -> dict[str, str | int | None]:
    return {
        "interval_seconds": _interval_seconds,
        "last_run": _last_run.isoformat() if _last_run else None,
        "next_run": _next_run.isoformat() if _next_run else None,
    }


async def run_interval(task: Callable[[], Awaitable[None]], interval: int) -> None:
    while True:
        global _last_run, _next_run, _interval_seconds
        _interval_seconds = interval
        _last_run = datetime.now(tz=timezone.utc)
        _next_run = _last_run + timedelta(seconds=interval)
        logger.info("Scheduler tick", extra={"interval": interval})
        await task()
        await asyncio.sleep(interval)

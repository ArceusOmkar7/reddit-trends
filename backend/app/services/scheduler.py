from __future__ import annotations

import asyncio
import logging
from typing import Awaitable, Callable

logger = logging.getLogger("reddit_trends.scheduler")


async def run_interval(task: Callable[[], Awaitable[None]], interval: int) -> None:
    while True:
        logger.info("Scheduler tick", extra={"interval": interval})
        await task()
        await asyncio.sleep(interval)

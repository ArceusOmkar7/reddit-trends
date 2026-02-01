from __future__ import annotations

import asyncio
from typing import Awaitable, Callable


async def run_interval(task: Callable[[], Awaitable[None]], interval: int) -> None:
    while True:
        await task()
        await asyncio.sleep(interval)

from __future__ import annotations

import anyio
import pytest

from app.services.scheduler import run_interval


@pytest.mark.anyio
async def test_scheduler_runs_task():
    calls = {"count": 0}

    async def task():
        calls["count"] += 1

    async with anyio.create_task_group() as tg:
        tg.start_soon(run_interval, task, 0.01)
        await anyio.sleep(0.05)
        tg.cancel_scope.cancel()

    assert calls["count"] >= 1

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import PollingState
from app.services.scheduler import get_polling_state

router = APIRouter(prefix="/meta")


@router.get("/polling", response_model=PollingState)
def get_polling() -> PollingState:
    state = get_polling_state()
    interval = int(state.get("interval_seconds") or settings.poll_interval_seconds)
    return PollingState(
        enabled=settings.enable_ingestion,
        intervalSeconds=interval,
        lastRun=state.get("last_run"),
        nextRun=state.get("next_run"),
    )

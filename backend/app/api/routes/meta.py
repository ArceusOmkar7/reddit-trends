from __future__ import annotations

from fastapi import APIRouter, Query

from app.core.config import settings
from app.models.schemas import PollingState
from app.repositories.dashboard import fetch_active_events, fetch_active_subreddits
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


@router.get("/subreddits", response_model=list[str])
def get_active_subreddits(limit: int | None = Query(None, ge=1)) -> list[str]:
    return fetch_active_subreddits(limit=limit)


@router.get("/events", response_model=list[str])
def get_active_events(limit: int | None = Query(None, ge=1)) -> list[str]:
    return fetch_active_events(limit=limit)

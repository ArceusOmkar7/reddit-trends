from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from app.models.schemas import SentimentSummary, TrendSummary
from app.repositories.analytics import fetch_sentiment_series, fetch_trend_snapshots

router = APIRouter(prefix="/analytics")


@router.get("/sentiment", response_model=list[SentimentSummary])
def get_sentiment(
    hours: int = Query(24, ge=1, le=168),
    subreddit: Optional[str] = None,
) -> list[SentimentSummary]:
    return fetch_sentiment_series(hours=hours, subreddit=subreddit)


@router.get("/trends", response_model=list[TrendSummary])
def get_trends(hours: int = Query(24, ge=1, le=168)) -> list[TrendSummary]:
    return fetch_trend_snapshots(hours=hours)

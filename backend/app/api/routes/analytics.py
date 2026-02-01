from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from datetime import datetime, timezone

from app.models.schemas import DashboardSummary, EventSummary, SentimentSummary, SubredditSummary, TrendSummary
from app.repositories.analytics import fetch_sentiment_series, fetch_trend_snapshots
from app.repositories.dashboard import (
    fetch_active_events,
    fetch_active_subreddits,
    fetch_kpis,
    fetch_sentiment_timeline,
    fetch_trending_topic_contexts,
    fetch_trending_topics,
    fetch_volume_series,
)
from app.repositories.subreddit_analytics import (
    fetch_event_sentiment,
    fetch_event_topics,
    fetch_event_volume,
    fetch_subreddit_kpis,
    fetch_subreddit_sentiment,
    fetch_subreddit_topics,
)

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


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(hours: int = Query(24, ge=1, le=168)) -> DashboardSummary:
    kpis = fetch_kpis(hours=hours)
    sentiment_trend = fetch_sentiment_timeline(hours=hours)
    volume_trend = fetch_volume_series(hours=hours)
    trending_topics = fetch_trending_topics(hours=hours, limit=5)
    topic_contexts = fetch_trending_topic_contexts([item["keyword"] for item in trending_topics])

    dashboard_kpis = [
        {
            "label": "Sentiment",
            "value": f"{kpis['avg_sentiment']:+.2f}",
            "delta": "Stable",
            "trend": "neutral",
        },
        {
            "label": "Mentions",
            "value": f"{kpis['mentions']}",
            "delta": "+0%",
            "trend": "neutral",
        },
        {
            "label": "Active subs",
            "value": f"{kpis['active_subreddits']}",
            "delta": "Stable",
            "trend": "neutral",
        },
        {
            "label": "Spikes",
            "value": f"{kpis['spikes']}",
            "delta": "+0",
            "trend": "neutral",
        },
    ]

    formatted_topics = [
        {
            "keyword": item["keyword"],
            "velocity": f"+{item['velocity']:.0f}%",
            "context": topic_contexts.get(item["keyword"], ""),
            "sentiment": "Neutral",
            "spike": f"Spike x{item['spike']:.1f}",
        }
        for item in trending_topics
    ]

    active_subreddits = fetch_active_subreddits()
    active_events = fetch_active_events()
    return DashboardSummary(
        lastUpdated=datetime.now(tz=timezone.utc).isoformat(),
        kpis=dashboard_kpis,
        sentimentTrend=sentiment_trend,
        volumeTrend=volume_trend,
        trendingTopics=formatted_topics,
        activeSubreddits=active_subreddits,
        activeEvents=active_events,
    )


@router.get("/subreddits/{name}", response_model=SubredditSummary)
def get_subreddit_summary(
    name: str, hours: int = Query(24, ge=1, le=168)
) -> SubredditSummary:
    return SubredditSummary(
        lastUpdated=datetime.now(tz=timezone.utc).isoformat(),
        kpis=fetch_subreddit_kpis(name, hours=hours),
        sentimentTrend=fetch_subreddit_sentiment(name, hours=hours),
        topics=fetch_subreddit_topics(name, hours=hours),
    )


@router.get("/events/{event_id}", response_model=EventSummary)
def get_event_summary(
    event_id: str, hours: int = Query(24, ge=1, le=168)
) -> EventSummary:
    return EventSummary(
        lastUpdated=datetime.now(tz=timezone.utc).isoformat(),
        volumeTrend=fetch_event_volume(event_id, hours=hours),
        sentimentTrend=fetch_event_sentiment(event_id, hours=hours),
        topicCards=fetch_event_topics(event_id, hours=hours),
    )

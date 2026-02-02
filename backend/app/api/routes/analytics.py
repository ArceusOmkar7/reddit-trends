from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from datetime import datetime, timezone

from app.models.schemas import (
    DashboardSummary,
    EmergingTopicSummary,
    EventSummary,
    SentimentSummary,
    SubredditSummary,
    TrendSummary,
)
from app.repositories.analytics import fetch_sentiment_series, fetch_trend_snapshots
from app.repositories.emerging_topics import fetch_emerging_topics
from app.repositories.dashboard import (
    fetch_active_events,
    fetch_active_subreddits,
    fetch_kpis_window,
    fetch_sentiment_timeline,
    fetch_trending_topic_contexts,
    fetch_trending_topics,
    fetch_volume_series,
)
from app.repositories.subreddit_analytics import (
    fetch_event_sentiment,
    fetch_event_top_posts,
    fetch_event_leading_subreddits,
    fetch_event_lifecycle,
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


@router.get("/emerging-topics", response_model=list[EmergingTopicSummary])
def get_emerging_topics(
    hours: int = Query(24, ge=1, le=168), limit: int = Query(20, ge=1, le=100)
) -> list[EmergingTopicSummary]:
    return fetch_emerging_topics(hours=hours, limit=limit)


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(hours: int = Query(24, ge=1, le=168)) -> DashboardSummary:
    kpis, previous = fetch_kpis_window(hours=hours)
    sentiment_timeline = fetch_sentiment_timeline(hours=hours)
    volume_trend = fetch_volume_series(hours=hours)
    trending_topics = fetch_trending_topics(hours=hours, limit=5)
    topic_contexts = fetch_trending_topic_contexts([item["keyword"] for item in trending_topics])

    def percent_delta(current: int, prev: int) -> tuple[str, str]:
        if prev == 0:
            if current == 0:
                return "Stable", "neutral"
            return "+100%", "up"
        delta = ((current - prev) / prev) * 100
        trend = "up" if delta > 0 else "down" if delta < 0 else "neutral"
        return f"{delta:+.0f}%", trend

    def absolute_delta(current: int, prev: int) -> tuple[str, str]:
        delta = current - prev
        trend = "up" if delta > 0 else "down" if delta < 0 else "neutral"
        if delta == 0:
            return "Stable", "neutral"
        return f"{delta:+d}", trend

    def sentiment_delta(current: float, prev: float) -> tuple[str, str]:
        delta = current - prev
        trend = "up" if delta > 0 else "down" if delta < 0 else "neutral"
        if delta == 0:
            return "Stable", "neutral"
        return f"{delta:+.2f}", trend

    mentions_delta, mentions_trend = percent_delta(
        kpis["mentions"], previous["mentions"]
    )
    subs_delta, subs_trend = absolute_delta(
        kpis["active_subreddits"], previous["active_subreddits"]
    )
    sentiment_delta_value, sentiment_trend = sentiment_delta(
        kpis["avg_sentiment"], previous["avg_sentiment"]
    )
    spikes_delta, spikes_trend = absolute_delta(
        kpis["spikes"], previous["spikes"]
    )

    dashboard_kpis = [
        {
            "label": "Sentiment",
            "value": f"{kpis['avg_sentiment']:+.2f}",
            "delta": sentiment_delta_value,
            "trend": sentiment_trend,
        },
        {
            "label": "Mentions",
            "value": f"{kpis['mentions']}",
            "delta": mentions_delta,
            "trend": mentions_trend,
        },
        {
            "label": "Active subs",
            "value": f"{kpis['active_subreddits']}",
            "delta": subs_delta,
            "trend": subs_trend,
        },
        {
            "label": "Spikes",
            "value": f"{kpis['spikes']}",
            "delta": spikes_delta,
            "trend": spikes_trend,
        },
    ]

    formatted_topics = [
        {
            "keyword": item["keyword"],
            "velocity": f"{item['velocity'] * 100:+.0f}%",
            "context": topic_contexts.get(item["keyword"], ""),
            "spike": f"Spike x{item['spike']:.1f}",
        }
        for item in trending_topics
    ]

    active_subreddits = fetch_active_subreddits()
    active_events = fetch_active_events()
    return DashboardSummary(
        lastUpdated=datetime.now(tz=timezone.utc).isoformat(),
        kpis=dashboard_kpis,
        sentimentTrend=sentiment_timeline,
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
        topPosts=fetch_event_top_posts(event_id, hours=hours),
        leadingSubreddits=fetch_event_leading_subreddits(event_id, hours=hours),
        lifecycle=fetch_event_lifecycle(event_id),
    )

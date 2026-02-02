from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PostIn(BaseModel):
    id: str
    timestamp: str
    subreddit: str
    title: Optional[str] = None
    body: Optional[str] = None
    score: int = 0
    comment_count: int = 0


class HealthResponse(BaseModel):
    status: str = Field(json_schema_extra={"example": "ok"})


class PollingState(BaseModel):
    enabled: bool
    intervalSeconds: int
    lastRun: Optional[str] = None
    nextRun: Optional[str] = None


class SentimentRecord(BaseModel):
    id: str
    timestamp: str
    context: str
    label: str
    sentiment: float
    subreddit_id: Optional[int] = None
    event_id: Optional[int] = None


class TrendSnapshotRecord(BaseModel):
    id: str
    timestamp: str
    keyword: str
    velocity: float
    spike: float
    context: str
    keyword_id: Optional[int] = None
    subreddit_id: Optional[int] = None
    event_id: Optional[int] = None
    raw_mentions: Optional[int] = None
    weighted_mentions: Optional[float] = None
    previous_mentions: Optional[int] = None
    window_start: Optional[str] = None
    window_end: Optional[str] = None


class EmergingTopicRecord(BaseModel):
    id: str
    timestamp: str
    topic: str
    raw_mentions: int
    unique_posts: int
    velocity: float
    window_start: str
    window_end: str
    context: str
    topic_id: Optional[int] = None


class PostResponse(BaseModel):
    id: str
    timestamp: str
    subreddit: str
    title: Optional[str] = None
    body: Optional[str] = None
    score: int = 0
    comment_count: int = 0


class SentimentSummary(BaseModel):
    timestamp: str
    label: str
    sentiment: float


class TrendSummary(BaseModel):
    timestamp: str
    keyword: str
    velocity: float
    spike: float
    raw_mentions: Optional[int] = None
    weighted_mentions: Optional[float] = None
    previous_mentions: Optional[int] = None
    window_start: Optional[str] = None
    window_end: Optional[str] = None


class EmergingTopicSummary(BaseModel):
    timestamp: str
    topic: str
    raw_mentions: int
    unique_posts: int
    velocity: float
    first_seen: Optional[str] = None


class VolumePoint(BaseModel):
    time: str
    value: int


class SentimentPoint(BaseModel):
    time: str
    value: float


class DashboardKpiItem(BaseModel):
    label: str
    value: str
    delta: str
    trend: str


class DashboardTopic(BaseModel):
    keyword: str
    velocity: str
    context: str
    sentiment: Optional[str] = None
    spike: str


class DashboardSummary(BaseModel):
    lastUpdated: str
    kpis: list[DashboardKpiItem]
    sentimentTrend: list[SentimentPoint]
    volumeTrend: list[VolumePoint]
    trendingTopics: list[DashboardTopic]
    activeSubreddits: list[str]
    activeEvents: list[str]


class SubredditSummary(BaseModel):
    lastUpdated: str
    kpis: list[dict]
    sentimentTrend: list[SentimentPoint]
    topics: list[DashboardTopic]


class EventSummary(BaseModel):
    lastUpdated: str
    volumeTrend: list[VolumePoint]
    sentimentTrend: list[SentimentPoint]
    topicCards: list[DashboardTopic]
    topPosts: list[dict] = []
    leadingSubreddits: list[dict] = []
    lifecycle: dict | None = None


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
    status: str = Field(example="ok")


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

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

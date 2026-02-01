from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from app.models.schemas import PostResponse
from app.repositories.raw import fetch_posts

router = APIRouter(prefix="/raw")


@router.get("/posts", response_model=list[PostResponse])
def get_posts(
    limit: int = Query(100, ge=1, le=500),
    subreddit: Optional[str] = None,
) -> list[PostResponse]:
    return fetch_posts(limit=limit, subreddit=subreddit)

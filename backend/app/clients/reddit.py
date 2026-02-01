from __future__ import annotations

from typing import Any
import asyncio

import praw

from app.core.config import settings


class RedditClient:
    def __init__(self) -> None:
        self._client = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
        )

    async def fetch_new_posts(self, subreddit: str, limit: int = 50) -> list[dict[str, Any]]:
        return await asyncio.to_thread(self._fetch_new_posts_sync, subreddit, limit)

    def _fetch_new_posts_sync(self, subreddit: str, limit: int) -> list[dict[str, Any]]:
        items = []
        for submission in self._client.subreddit(subreddit).new(limit=limit):
            items.append(
                {
                    "id": submission.id,
                    "created_utc": submission.created_utc,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                }
            )
        return items

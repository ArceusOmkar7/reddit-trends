from __future__ import annotations

from datetime import datetime, timezone

import logging

from app.clients.reddit import RedditClient
from app.core.config import settings
from app.models.schemas import PostIn
from app.repositories.posts import store_posts


def parse_scope(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


logger = logging.getLogger("reddit_trends.ingestion")


async def poll_reddit() -> list[PostIn]:
    client = RedditClient()
    posts: list[PostIn] = []
    logger.info("Starting ingestion cycle")

    for subreddit in parse_scope(settings.subreddits):
        items = await client.fetch_new_posts(subreddit)
        for item in items:
            posts.append(
                PostIn(
                    id=item.get("id", ""),
                    timestamp=datetime.fromtimestamp(
                        item.get("created_utc", 0), tz=timezone.utc
                    ).isoformat(),
                    subreddit=subreddit,
                    title=item.get("title"),
                    body=item.get("selftext", ""),
                    score=item.get("score", 0),
                    comment_count=item.get("num_comments", 0),
                )
            )

    inserted = 0
    if posts:
        inserted = store_posts(posts)

    logger.info(
        "Ingestion cycle complete",
        extra={"fetched": len(posts), "inserted": inserted},
    )

    return posts

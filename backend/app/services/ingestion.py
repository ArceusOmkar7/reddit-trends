from __future__ import annotations

from datetime import datetime, timezone

import logging

from app.clients.reddit import RedditClient
from app.core.config import settings
from app.models.schemas import PostIn
from app.repositories.posts import store_posts
from app.repositories.sentiment import store_sentiment
from app.repositories.trends import store_trends
from app.services.sentiment import aggregate_sentiment
from app.services.trends import detect_trends


def parse_scope(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


logger = logging.getLogger("reddit_trends.ingestion")


async def poll_reddit() -> list[PostIn]:
    client = RedditClient()
    posts: list[PostIn] = []
    subreddit_scope = parse_scope(settings.subreddits)
    logger.info(
        "Starting ingestion cycle",
        extra={"subreddits": subreddit_scope},
    )

    for subreddit in subreddit_scope:
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

        sentiment_records = aggregate_sentiment(posts)
        if sentiment_records:
            store_sentiment(sentiment_records)

        trend_records = detect_trends(posts)
        if trend_records:
            store_trends(trend_records)

    logger.info(
        "Ingestion cycle complete",
        extra={"fetched": len(posts), "inserted": inserted},
    )

    return posts

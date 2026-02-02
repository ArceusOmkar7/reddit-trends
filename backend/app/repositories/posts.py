from __future__ import annotations

from typing import Iterable

import logging

from app.db.database import get_connection
from app.models.schemas import PostIn
from app.repositories.subreddits import get_or_create_subreddit_id

logger = logging.getLogger("reddit_trends.posts")


def store_posts(posts: Iterable[PostIn]) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    enriched = []
    for post in posts:
        if not post.id:
            continue
        subreddit = post.subreddit or ""
        subreddit_id = get_or_create_subreddit_id(subreddit) if subreddit else None
        enriched.append(
            (
                post.id,
                post.timestamp,
                subreddit_id,
                post.title,
                post.body,
                post.score,
                post.comment_count,
            )
        )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO posts (
            id,
            timestamp,
            subreddit_id,
            title,
            body,
            score,
            comment_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        enriched,
    )

    connection.commit()
    inserted = cursor.rowcount
    connection.close()
    logger.info("Stored posts | received=%s inserted=%s", len(enriched), inserted)
    return inserted


def update_post_sentiment(
    scores: Iterable[tuple[str, float, float, float, float]]
) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        UPDATE posts
        SET sentiment_compound = ?,
            sentiment_pos = ?,
            sentiment_neg = ?,
            sentiment_neu = ?
        WHERE id = ?
        """,
        [
            (compound, pos, neg, neu, post_id)
            for post_id, compound, pos, neg, neu in scores
        ],
    )

    connection.commit()
    updated = cursor.rowcount
    connection.close()
    logger.info("Updated post sentiment | records=%s", updated)
    return updated

from __future__ import annotations

from typing import Iterable

from app.db.database import get_connection
from app.models.schemas import PostIn
from app.repositories.subreddits import get_or_create_subreddit_id


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
    return inserted

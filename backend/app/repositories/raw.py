from __future__ import annotations

from typing import Optional

from app.db.database import get_connection
from app.models.schemas import PostResponse


def fetch_posts(limit: int = 100, subreddit: Optional[str] = None) -> list[PostResponse]:
    connection = get_connection()
    cursor = connection.cursor()
    if subreddit:
        cursor.execute(
            """
            SELECT id, timestamp, subreddit, title, body, score, comment_count
            FROM posts
            WHERE subreddit = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (subreddit, limit),
        )
    else:
        cursor.execute(
            """
            SELECT id, timestamp, subreddit, title, body, score, comment_count
            FROM posts
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )

    rows = cursor.fetchall()
    connection.close()
    return [
        PostResponse(
            id=row["id"],
            timestamp=row["timestamp"],
            subreddit=row["subreddit"],
            title=row["title"],
            body=row["body"],
            score=row["score"],
            comment_count=row["comment_count"],
        )
        for row in rows
    ]

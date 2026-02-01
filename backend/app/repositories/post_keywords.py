from __future__ import annotations

from typing import Iterable

from app.db.database import get_connection


def store_post_keywords(rows: Iterable[tuple[str, int, int]]) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT OR REPLACE INTO post_keywords (post_id, keyword_id, count)
        VALUES (?, ?, ?)
        """,
        list(rows),
    )
    connection.commit()
    inserted = cursor.rowcount
    connection.close()
    return inserted

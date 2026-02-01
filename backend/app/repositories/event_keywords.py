from __future__ import annotations

from app.db.database import get_connection


def link_event_keyword(event_id: int, keyword_id: int) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO event_keywords (event_id, keyword_id) VALUES (?, ?);",
        (event_id, keyword_id),
    )
    connection.commit()
    connection.close()

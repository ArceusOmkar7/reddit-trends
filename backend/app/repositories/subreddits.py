from __future__ import annotations

from app.db.database import get_connection


def get_or_create_subreddit_id(name: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO subreddits (name) VALUES (?);", (name,))
    cursor.execute("SELECT id FROM subreddits WHERE name = ?;", (name,))
    row = cursor.fetchone()
    connection.commit()
    connection.close()
    return int(row["id"]) if row else 0

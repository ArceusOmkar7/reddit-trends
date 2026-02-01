from __future__ import annotations

from app.db.database import get_connection


def get_or_create_keyword_id(keyword: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO keywords (phrase) VALUES (?);", (keyword,))
    cursor.execute("SELECT id FROM keywords WHERE phrase = ?;", (keyword,))
    row = cursor.fetchone()
    connection.commit()
    connection.close()
    return int(row["id"]) if row else 0

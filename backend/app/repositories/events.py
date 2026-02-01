from __future__ import annotations

from typing import Optional

from app.db.database import get_connection


def get_or_create_event_id(name: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO events (name) VALUES (?);", (name,))
    cursor.execute("SELECT id FROM events WHERE name = ?;", (name,))
    row = cursor.fetchone()
    connection.commit()
    connection.close()
    return int(row["id"]) if row else 0


def get_event_id_by_name(name: str) -> Optional[int]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM events WHERE name = ?;", (name,))
    row = cursor.fetchone()
    connection.close()
    return int(row["id"]) if row else None

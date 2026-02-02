from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from app.db.database import get_connection
from app.models.schemas import EmergingTopicRecord, EmergingTopicSummary


def get_or_create_topic_id(phrase: str, first_seen: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, first_seen
        FROM emerging_topics
        WHERE phrase = ?
        """,
        (phrase,),
    )
    row = cursor.fetchone()
    if row:
        topic_id = int(row["id"])
    else:
        cursor.execute(
            """
            INSERT INTO emerging_topics (phrase, first_seen)
            VALUES (?, ?)
            """,
            (phrase, first_seen),
        )
        topic_id = int(cursor.lastrowid)
    connection.commit()
    connection.close()
    return topic_id


def fetch_existing_topics(phrases: list[str]) -> dict[str, tuple[int, str]]:
    if not phrases:
        return {}
    placeholders = ",".join(["?"] * len(phrases))
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT id, phrase, first_seen
        FROM emerging_topics
        WHERE phrase IN ({placeholders})
        """,
        tuple(phrases),
    )
    rows = cursor.fetchall()
    connection.close()
    return {row["phrase"]: (int(row["id"]), row["first_seen"]) for row in rows}


def store_emerging_topic_snapshots(records: Iterable[EmergingTopicRecord]) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    payload = [
        (
            record.id,
            record.timestamp,
            record.topic_id,
            record.raw_mentions,
            record.unique_posts,
            record.velocity,
            record.window_start,
            record.window_end,
            record.context,
        )
        for record in records
    ]
    cursor.executemany(
        """
        INSERT INTO emerging_topic_snapshots (
            id,
            timestamp,
            topic_id,
            raw_mentions,
            unique_posts,
            velocity,
            window_start,
            window_end,
            context
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(topic_id, window_start, window_end)
        DO UPDATE SET
            timestamp = excluded.timestamp,
            raw_mentions = excluded.raw_mentions,
            unique_posts = excluded.unique_posts,
            velocity = excluded.velocity,
            context = excluded.context
        """,
        payload,
    )
    connection.commit()
    inserted = cursor.rowcount
    connection.close()
    return inserted


def fetch_emerging_topics(hours: int = 24, limit: int = 20) -> list[EmergingTopicSummary]:
    connection = get_connection()
    cursor = connection.cursor()
    since = (datetime.now(tz=timezone.utc) - timedelta(hours=hours)).isoformat()
    cursor.execute(
        """
        SELECT ets.timestamp,
               t.phrase AS topic,
               ets.raw_mentions,
               ets.unique_posts,
               ets.velocity,
               t.first_seen
        FROM emerging_topic_snapshots ets
        JOIN emerging_topics t ON t.id = ets.topic_id
        WHERE ets.timestamp >= ?
        ORDER BY ets.velocity DESC, ets.raw_mentions DESC
        LIMIT ?
        """,
        (since, limit),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        EmergingTopicSummary(
            timestamp=row["timestamp"],
            topic=row["topic"],
            raw_mentions=int(row["raw_mentions"]),
            unique_posts=int(row["unique_posts"]),
            velocity=float(row["velocity"]),
            first_seen=row["first_seen"],
        )
        for row in rows
    ]

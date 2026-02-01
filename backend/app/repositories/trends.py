from __future__ import annotations

from typing import Iterable, Optional

from app.db.database import get_connection
from app.models.schemas import TrendSnapshotRecord


def store_trends(records: Iterable[TrendSnapshotRecord]) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    payload = [
        (
            record.id,
            record.timestamp,
            record.keyword,
            record.velocity,
            record.spike,
            record.context,
            record.keyword_id,
            record.subreddit_id,
            record.event_id,
        )
        for record in records
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO trend_snapshots (
            id,
            timestamp,
            keyword,
            velocity,
            spike,
            context,
            keyword_id,
            subreddit_id,
            event_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        payload,
    )

    connection.commit()
    inserted = cursor.rowcount
    connection.close()
    return inserted


def get_latest_keyword_snapshot(keyword: str) -> Optional[TrendSnapshotRecord]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, timestamp, keyword, velocity, spike, context, keyword_id, subreddit_id, event_id
        FROM trend_snapshots
        WHERE keyword = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (keyword,),
    )
    row = cursor.fetchone()
    connection.close()
    if not row:
        return None
    return TrendSnapshotRecord(
        id=row["id"],
        timestamp=row["timestamp"],
        keyword=row["keyword"],
        velocity=float(row["velocity"]),
        spike=float(row["spike"]),
        context=row["context"],
        keyword_id=row["keyword_id"],
        subreddit_id=row["subreddit_id"],
        event_id=row["event_id"],
    )

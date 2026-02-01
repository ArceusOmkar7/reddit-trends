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
            keyword_id,
            velocity,
            spike,
            context,
            subreddit_id,
            event_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                record.id,
                record.timestamp,
                record.keyword_id,
                record.velocity,
                record.spike,
                record.context,
                record.subreddit_id,
                record.event_id,
            )
            for record in records
        ],
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
        SELECT ts.id, ts.timestamp, k.phrase AS keyword, ts.velocity, ts.spike, ts.context,
               ts.keyword_id, ts.subreddit_id, ts.event_id
        FROM trend_snapshots ts
        JOIN keywords k ON k.id = ts.keyword_id
        WHERE k.phrase = ?
        ORDER BY ts.timestamp DESC
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

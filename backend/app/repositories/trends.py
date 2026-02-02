from __future__ import annotations

from typing import Iterable, Optional

import logging

from app.db.database import get_connection
from app.models.schemas import TrendSnapshotRecord

logger = logging.getLogger("reddit_trends.trends_store")


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
            record.raw_mentions,
            record.weighted_mentions,
            record.previous_mentions,
            record.window_start,
            record.window_end,
        )
        for record in records
    ]

    cursor.executemany(
        """
        INSERT INTO trend_snapshots (
            id,
            timestamp,
            keyword_id,
            velocity,
            spike,
            context,
            subreddit_id,
            event_id,
            raw_mentions,
            weighted_mentions,
            previous_mentions,
            window_start,
            window_end
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(keyword_id, window_start, window_end)
        DO UPDATE SET
            timestamp = excluded.timestamp,
            velocity = excluded.velocity,
            spike = excluded.spike,
            context = excluded.context,
            subreddit_id = excluded.subreddit_id,
            event_id = excluded.event_id,
            raw_mentions = excluded.raw_mentions,
            weighted_mentions = excluded.weighted_mentions,
            previous_mentions = excluded.previous_mentions
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
                record.raw_mentions,
                record.weighted_mentions,
                record.previous_mentions,
                record.window_start,
                record.window_end,
            )
            for record in records
        ],
    )

    connection.commit()
    inserted = cursor.rowcount
    connection.close()
    logger.info("Stored trends | records=%s", len(payload))
    return inserted


def get_latest_keyword_snapshot(keyword: str) -> Optional[TrendSnapshotRecord]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
         SELECT ts.id, ts.timestamp, k.phrase AS keyword, ts.velocity, ts.spike, ts.context,
             ts.keyword_id, ts.subreddit_id, ts.event_id, ts.raw_mentions,
             ts.weighted_mentions, ts.previous_mentions, ts.window_start, ts.window_end
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
        raw_mentions=row["raw_mentions"],
        weighted_mentions=row["weighted_mentions"],
        previous_mentions=row["previous_mentions"],
        window_start=row["window_start"],
        window_end=row["window_end"],
    )

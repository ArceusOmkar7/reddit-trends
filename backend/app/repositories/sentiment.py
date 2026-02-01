from __future__ import annotations

from typing import Iterable

from app.db.database import get_connection
from app.models.schemas import SentimentRecord


def store_sentiment(records: Iterable[SentimentRecord]) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    payload = [
        (
            record.id,
            record.timestamp,
            record.context,
            record.label,
            record.sentiment,
            record.subreddit_id,
            record.event_id,
        )
        for record in records
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO sentiment_series (
            id,
            timestamp,
            context,
            sentiment,
            subreddit_id,
            event_id
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                record.id,
                record.timestamp,
                record.context,
                record.sentiment,
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

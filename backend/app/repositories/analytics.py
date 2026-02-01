from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from app.db.database import get_connection
from app.models.schemas import SentimentSummary, TrendSummary


def _since(hours: int) -> str:
    return (datetime.now(tz=timezone.utc) - timedelta(hours=hours)).isoformat()


def fetch_sentiment_series(hours: int = 24, subreddit: Optional[str] = None) -> list[SentimentSummary]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)

    if subreddit:
        cursor.execute(
            """
            SELECT s.timestamp, r.name AS label, s.sentiment
            FROM sentiment_series s
            JOIN subreddits r ON r.id = s.subreddit_id
            WHERE r.name = ? AND s.timestamp >= ?
            ORDER BY s.timestamp ASC
            """,
            (subreddit, since),
        )
    else:
        cursor.execute(
            """
            SELECT s.timestamp, r.name AS label, s.sentiment
            FROM sentiment_series s
            LEFT JOIN subreddits r ON r.id = s.subreddit_id
            WHERE s.timestamp >= ?
            ORDER BY s.timestamp ASC
            """,
            (since,),
        )

    rows = cursor.fetchall()
    connection.close()
    return [
        SentimentSummary(
            timestamp=row["timestamp"],
            label=row["label"],
            sentiment=float(row["sentiment"]),
        )
        for row in rows
    ]


def fetch_trend_snapshots(hours: int = 24) -> list[TrendSummary]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    cursor.execute(
        """
        SELECT ts.timestamp, k.phrase AS keyword, ts.velocity, ts.spike
        FROM trend_snapshots ts
        JOIN keywords k ON k.id = ts.keyword_id
        WHERE ts.timestamp >= ?
        ORDER BY ts.spike DESC
        """,
        (since,),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        TrendSummary(
            timestamp=row["timestamp"],
            keyword=row["keyword"],
            velocity=float(row["velocity"]),
            spike=float(row["spike"]),
        )
        for row in rows
    ]

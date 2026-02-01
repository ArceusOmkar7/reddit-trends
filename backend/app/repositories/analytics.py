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
            SELECT timestamp, label, sentiment
            FROM sentiment_series
            WHERE label = ? AND timestamp >= ?
            ORDER BY timestamp ASC
            """,
            (subreddit, since),
        )
    else:
        cursor.execute(
            """
            SELECT timestamp, label, sentiment
            FROM sentiment_series
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
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
        SELECT timestamp, keyword, velocity, spike
        FROM trend_snapshots
        WHERE timestamp >= ?
        ORDER BY spike DESC
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

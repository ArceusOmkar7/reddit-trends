from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from app.db.database import get_connection
from app.models.schemas import SentimentSummary, TrendSummary

_TREND_DENYLIST = {"https", "says", "said", "new", "original", "today", "breaking"}


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
    placeholders = ",".join(["?"] * len(_TREND_DENYLIST))
    cursor.execute(
        f"""
        SELECT ts.timestamp, k.phrase AS keyword, ts.velocity, ts.spike,
               ts.raw_mentions, ts.weighted_mentions, ts.previous_mentions,
               ts.window_start, ts.window_end
        FROM trend_snapshots ts
        JOIN keywords k ON k.id = ts.keyword_id
        WHERE COALESCE(ts.window_end, ts.timestamp) >= ?
          AND ts.raw_mentions IS NOT NULL
          AND ts.window_start IS NOT NULL
          AND substr(ts.window_start, 15, 2) = '00'
          AND substr(ts.window_start, 18, 2) = '00'
          AND substr(ts.window_end, 15, 2) = '00'
          AND substr(ts.window_end, 18, 2) = '00'
          AND k.phrase NOT IN ({placeholders})
          AND (
            ts.raw_mentions >= 5
            OR ts.weighted_mentions >= 5
            OR ts.velocity >= 0.5
          )
        ORDER BY ts.spike DESC
        """,
        (since, *_TREND_DENYLIST),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        TrendSummary(
            timestamp=row["timestamp"],
            keyword=row["keyword"],
            velocity=float(row["velocity"]),
            spike=float(row["spike"]),
            raw_mentions=row["raw_mentions"],
            weighted_mentions=row["weighted_mentions"],
            previous_mentions=row["previous_mentions"],
            window_start=row["window_start"],
            window_end=row["window_end"],
        )
        for row in rows
    ]

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.database import get_connection
from app.core.config import settings


def _since(hours: int) -> str:
    return (datetime.now(tz=timezone.utc) - timedelta(hours=hours)).isoformat()


def fetch_kpis(hours: int = 24) -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM posts
        WHERE timestamp >= ?
        """,
        (since,),
    )
    mentions = int(cursor.fetchone()["count"])

    cursor.execute("SELECT COUNT(*) AS count FROM subreddits;")
    subreddits = int(cursor.fetchone()["count"])

    cursor.execute(
        """
        SELECT AVG(sentiment) AS avg_sentiment
        FROM sentiment_series
        WHERE timestamp >= ?
        """,
        (since,),
    )
    avg_sentiment = cursor.fetchone()["avg_sentiment"]
    avg_sentiment = float(avg_sentiment) if avg_sentiment is not None else 0.0

    cursor.execute(
        """
        SELECT COUNT(DISTINCT keyword_id) AS spikes
        FROM trend_snapshots
        WHERE timestamp >= ? AND spike >= 1.5
        """,
        (since,),
    )
    spikes = int(cursor.fetchone()["spikes"])

    connection.close()
    return {
        "mentions": mentions,
        "active_subreddits": subreddits,
        "avg_sentiment": round(avg_sentiment, 4),
        "spikes": spikes,
    }


def fetch_active_subreddits(limit: int = 8) -> list[str]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT name
        FROM subreddits
        ORDER BY name ASC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    connection.close()
    return [f"r/{row['name']}" for row in rows]


def fetch_active_events(limit: int = 6) -> list[str]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT name
        FROM events
        ORDER BY name ASC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    connection.close()
    if rows:
        return [row["name"] for row in rows]

    keywords = [item.strip().lower() for item in settings.keywords.split(",") if item.strip()]
    return keywords[:limit]


def fetch_volume_series(hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    cursor.execute(
        """
        SELECT substr(timestamp, 1, 13) AS hour_bucket, COUNT(*) AS count
        FROM posts
        WHERE timestamp >= ?
        GROUP BY hour_bucket
        ORDER BY hour_bucket ASC
        """,
        (since,),
    )
    rows = cursor.fetchall()
    connection.close()
    return [{"time": row["hour_bucket"], "value": int(row["count"])} for row in rows]


def fetch_sentiment_timeline(hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    cursor.execute(
        """
        SELECT substr(timestamp, 1, 13) AS hour_bucket, AVG(sentiment) AS avg_sentiment
        FROM sentiment_series
        WHERE timestamp >= ?
        GROUP BY hour_bucket
        ORDER BY hour_bucket ASC
        """,
        (since,),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "time": row["hour_bucket"],
            "value": round(float(row["avg_sentiment"] or 0.0), 4),
        }
        for row in rows
    ]


def fetch_trending_topics(hours: int = 24, limit: int = 5) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    cursor.execute(
        """
        SELECT k.phrase AS keyword, ts.velocity, ts.spike
        FROM trend_snapshots ts
        JOIN keywords k ON k.id = ts.keyword_id
        WHERE ts.timestamp >= ?
        ORDER BY ts.spike DESC
        LIMIT ?
        """,
        (since, limit),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "keyword": row["keyword"],
            "velocity": float(row["velocity"]),
            "spike": float(row["spike"]),
        }
        for row in rows
    ]


def fetch_trending_topic_contexts(keywords: list[str]) -> dict[str, str]:
    if not keywords:
        return {}
    placeholders = ",".join(["?"] * len(keywords))
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT k.phrase AS keyword, r.name AS subreddit, COUNT(*) AS mentions
        FROM post_keywords pk
        JOIN keywords k ON k.id = pk.keyword_id
        JOIN posts p ON p.id = pk.post_id
        JOIN subreddits r ON r.id = p.subreddit_id
        WHERE k.phrase IN ({placeholders})
        GROUP BY k.phrase, r.name
        ORDER BY k.phrase, mentions DESC
        """,
        tuple(keywords),
    )
    rows = cursor.fetchall()
    connection.close()

    contexts: dict[str, list[str]] = {}
    for row in rows:
        contexts.setdefault(row["keyword"], []).append(f"r/{row['subreddit']}")

    return {key: ", ".join(values[:2]) for key, values in contexts.items()}

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.database import get_connection
from app.services.sentiment import score_text


def _since(hours: int) -> str:
    return (datetime.now(tz=timezone.utc) - timedelta(hours=hours)).isoformat()


def fetch_subreddit_kpis(subreddit: str, hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)

    cursor.execute(
        """
        SELECT r.id
        FROM subreddits r
        WHERE r.name = ?
        """,
        (subreddit,),
    )
    row = cursor.fetchone()
    subreddit_id = row["id"] if row else None

    if subreddit_id is None:
        connection.close()
        return [
            {"label": "Posts", "value": "0", "delta": "Stable"},
            {"label": "Comments", "value": "0", "delta": "Stable"},
            {"label": "Sentiment", "value": "+0.00", "delta": "Stable"},
        ]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM posts
        WHERE subreddit_id = ? AND timestamp >= ?
        """,
        (subreddit_id, since),
    )
    posts = int(cursor.fetchone()["count"])

    cursor.execute(
        """
        SELECT AVG(sentiment) AS avg_sentiment
        FROM sentiment_series
        WHERE subreddit_id = ? AND timestamp >= ?
        """,
        (subreddit_id, since),
    )
    avg_sentiment = cursor.fetchone()["avg_sentiment"]
    avg_sentiment = float(avg_sentiment) if avg_sentiment is not None else 0.0

    connection.close()

    return [
        {"label": "Posts", "value": f"{posts}", "delta": "Stable"},
        {"label": "Comments", "value": "0", "delta": "Stable"},
        {"label": "Sentiment", "value": f"{avg_sentiment:+.2f}", "delta": "Stable"},
    ]


def fetch_subreddit_sentiment(subreddit: str, hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    cursor.execute(
        """
        SELECT s.timestamp, s.sentiment
        FROM sentiment_series s
        JOIN subreddits r ON r.id = s.subreddit_id
        WHERE r.name = ? AND s.timestamp >= ?
        ORDER BY s.timestamp ASC
        """,
        (subreddit, since),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        {"time": row["timestamp"][11:16], "value": float(row["sentiment"])}
        for row in rows
    ]


def fetch_subreddit_topics(subreddit: str, hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    cursor.execute(
        """
        SELECT k.phrase AS keyword, SUM(pk.count) AS mentions
        FROM post_keywords pk
        JOIN keywords k ON k.id = pk.keyword_id
        JOIN posts p ON p.id = pk.post_id
        JOIN subreddits r ON r.id = p.subreddit_id
        WHERE r.name = ? AND p.timestamp >= ?
        GROUP BY k.phrase
        ORDER BY mentions DESC
        LIMIT 5
        """,
        (subreddit, since),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "keyword": row["keyword"],
            "velocity": f"+{int(row['mentions'])}%",
            "context": "Top posts",
            "sentiment": "Neutral",
            "spike": "Spike x1.0",
        }
        for row in rows
    ]


def fetch_event_volume(event_keyword: str, hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    event_name = event_keyword.lower()
    cursor.execute(
        """
        SELECT substr(p.timestamp, 1, 13) AS hour_bucket, COUNT(DISTINCT p.id) AS count
        FROM events e
        JOIN event_keywords ek ON ek.event_id = e.id
        JOIN post_keywords pk ON pk.keyword_id = ek.keyword_id
        JOIN posts p ON p.id = pk.post_id
        WHERE e.name = ? AND p.timestamp >= ?
        GROUP BY hour_bucket
        ORDER BY hour_bucket ASC
        """,
        (event_name, since),
    )
    rows = cursor.fetchall()
    connection.close()
    return [{"time": row["hour_bucket"], "value": int(row["count"])} for row in rows]


def fetch_event_sentiment(event_keyword: str, hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    event_name = event_keyword.lower()
    cursor.execute(
        """
        SELECT DISTINCT p.id, p.timestamp, p.title, p.body, p.sentiment_compound
        FROM events e
        JOIN event_keywords ek ON ek.event_id = e.id
        JOIN post_keywords pk ON pk.keyword_id = ek.keyword_id
        JOIN posts p ON p.id = pk.post_id
        WHERE e.name = ? AND p.timestamp >= ?
        ORDER BY p.timestamp ASC
        """,
        (event_name, since),
    )
    rows = cursor.fetchall()
    connection.close()

    buckets: dict[str, list[float]] = {}
    for row in rows:
        bucket = row["timestamp"][11:16]
        if row["sentiment_compound"] is None:
            score = score_text(f"{row['title'] or ''} {row['body'] or ''}")
        else:
            score = float(row["sentiment_compound"])
        buckets.setdefault(bucket, []).append(score)

    return [
        {"time": time, "value": sum(values) / len(values)}
        for time, values in buckets.items()
    ]


def fetch_event_topics(event_keyword: str, hours: int = 24) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    since = _since(hours)
    event_name = event_keyword.lower()
    cursor.execute(
        """
        SELECT k2.phrase AS keyword, SUM(pk2.count) AS mentions
        FROM (
            SELECT DISTINCT p.id
            FROM events e
            JOIN event_keywords ek ON ek.event_id = e.id
            JOIN post_keywords pk ON pk.keyword_id = ek.keyword_id
            JOIN posts p ON p.id = pk.post_id
            WHERE e.name = ? AND p.timestamp >= ?
        ) ep
        JOIN post_keywords pk2 ON pk2.post_id = ep.id
        JOIN keywords k2 ON k2.id = pk2.keyword_id
        GROUP BY k2.phrase
        ORDER BY mentions DESC
        LIMIT 5
        """,
        (event_name, since),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "keyword": row["keyword"],
            "velocity": f"+{int(row['mentions'])}%",
            "context": "Event posts",
            "sentiment": "Neutral",
            "spike": "Spike x1.0",
        }
        for row in rows
    ]

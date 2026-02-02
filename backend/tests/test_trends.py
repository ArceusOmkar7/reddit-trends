from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models.schemas import PostIn, TrendSnapshotRecord
from app.repositories.posts import store_posts
from app.repositories.keywords import get_or_create_keyword_id
from app.repositories.trends import store_trends
from app.db.database import get_connection
from app.services.trends import detect_trends


def test_trend_detection(client):
    now = datetime.now(tz=timezone.utc)
    current = (now - timedelta(minutes=10)).isoformat()
    prev = (now - timedelta(minutes=90)).isoformat()
    posts = [
        PostIn(
            id="t1",
            timestamp=current,
            subreddit="technology",
            title="Disney update",
            body="disney disney disney",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="t2",
            timestamp=current,
            subreddit="science",
            title="Disney reports",
            body="disney disney https://example.com",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="t3",
            timestamp=current,
            subreddit="movies",
            title="Original disney news",
            body="disney says new",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="t4",
            timestamp=prev,
            subreddit="movies",
            title="Previous window",
            body="movie release",
            score=1,
            comment_count=0,
        ),
    ]

    store_posts(posts)

    records = detect_trends(posts)
    assert records
    store_trends(records)

    response = client.get("/analytics/trends?hours=1")
    assert response.status_code == 200
    data = response.json()
    assert data
    terms = {item["keyword"] for item in data}
    assert "disney" in terms
    assert "https" not in terms
    assert "new" not in terms
    assert "original" not in terms
    assert "says" not in terms


def test_trend_upsert_dedup(temp_db):
    now = datetime.now(tz=timezone.utc)
    window_start = (now - timedelta(hours=1)).isoformat()
    window_end = now.isoformat()
    keyword_id = get_or_create_keyword_id("disney")

    records = [
        {
            "id": "r1",
            "timestamp": window_end,
            "keyword_id": keyword_id,
            "velocity": 1.0,
            "spike": 2.0,
            "context": "global",
            "raw_mentions": 5,
            "weighted_mentions": 6.0,
            "previous_mentions": 1,
            "window_start": window_start,
            "window_end": window_end,
        },
        {
            "id": "r2",
            "timestamp": window_end,
            "keyword_id": keyword_id,
            "velocity": 2.0,
            "spike": 3.0,
            "context": "global",
            "raw_mentions": 6,
            "weighted_mentions": 7.0,
            "previous_mentions": 1,
            "window_start": window_start,
            "window_end": window_end,
        },
    ]

    store_trends(
        [
            TrendSnapshotRecord(
                id=record["id"],
                timestamp=record["timestamp"],
                keyword="disney",
                velocity=record["velocity"],
                spike=record["spike"],
                context=record["context"],
                keyword_id=record["keyword_id"],
                raw_mentions=record["raw_mentions"],
                weighted_mentions=record["weighted_mentions"],
                previous_mentions=record["previous_mentions"],
                window_start=record["window_start"],
                window_end=record["window_end"],
            )
            for record in records
        ]
    )

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM trend_snapshots
        WHERE keyword_id = ? AND window_start = ? AND window_end = ?
        """,
        (keyword_id, window_start, window_end),
    )
    count = int(cursor.fetchone()["count"])
    connection.close()
    assert count == 1


def test_trend_api_gating(client):
    now = datetime.now(tz=timezone.utc)
    window_start = (now - timedelta(hours=1)).isoformat()
    window_end = now.isoformat()
    keyword_id = get_or_create_keyword_id("validterm")
    store_trends(
        [
            TrendSnapshotRecord(
                id="g1",
                timestamp=window_end,
                keyword="validterm",
                velocity=0.1,
                spike=1.0,
                context="global",
                keyword_id=keyword_id,
                raw_mentions=4,
                weighted_mentions=2.0,
                previous_mentions=4,
                window_start=window_start,
                window_end=window_end,
            ),
            TrendSnapshotRecord(
                id="g2",
                timestamp=window_end,
                keyword="validterm",
                velocity=0.6,
                spike=1.2,
                context="global",
                keyword_id=keyword_id,
                raw_mentions=3,
                weighted_mentions=2.0,
                previous_mentions=2,
                window_start=window_start,
                window_end=window_end,
            ),
        ]
    )

    response = client.get("/analytics/trends?hours=1")
    assert response.status_code == 200
    data = response.json()
    assert any(item["keyword"] == "validterm" for item in data)

from __future__ import annotations

from datetime import datetime, timezone

from app.models.schemas import PostIn
from app.repositories.sentiment import store_sentiment
from app.services.sentiment import aggregate_sentiment, backfill_post_sentiment, score_text
from app.repositories.posts import store_posts
from app.db.database import get_connection


def test_sentiment_aggregation(client):
    now = datetime.now(tz=timezone.utc).isoformat()
    posts = [
        PostIn(
            id="p1",
            timestamp=now,
            subreddit="technology",
            title="Great growth",
            body="Strong win",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="p2",
            timestamp=now,
            subreddit="technology",
            title="Bad decline",
            body="Weak loss",
            score=1,
            comment_count=0,
        ),
    ]

    records = aggregate_sentiment(posts)
    assert records
    store_sentiment(records)

    response = client.get("/analytics/sentiment?subreddit=technology&hours=1")
    assert response.status_code == 200
    data = response.json()
    assert data
    assert data[-1]["label"] == "technology"


def test_dashboard_summary(client):
    response = client.get("/analytics/dashboard?hours=1")
    assert response.status_code == 200
    payload = response.json()
    assert "kpis" in payload
    assert "sentimentTrend" in payload
    assert "volumeTrend" in payload
    assert "trendingTopics" in payload
    assert "activeSubreddits" in payload
    assert "activeEvents" in payload


def test_vader_scoring_unit():
    assert score_text("This is amazing and wonderful") > 0
    assert score_text("This is terrible and awful") < 0


def test_post_sentiment_backfill(temp_db):
    now = datetime.now(tz=timezone.utc).isoformat()
    posts = [
        PostIn(
            id="b1",
            timestamp=now,
            subreddit="technology",
            title="Amazing growth",
            body="Strong results",
            score=1,
            comment_count=0,
        )
    ]
    store_posts(posts)
    updated = backfill_post_sentiment()
    assert updated >= 1

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT sentiment_compound
        FROM posts
        WHERE id = ?
        """,
        ("b1",),
    )
    row = cursor.fetchone()
    connection.close()
    assert row["sentiment_compound"] is not None

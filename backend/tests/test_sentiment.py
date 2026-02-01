from __future__ import annotations

from datetime import datetime, timezone

from app.models.schemas import PostIn
from app.repositories.sentiment import store_sentiment
from app.services.sentiment import aggregate_sentiment


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

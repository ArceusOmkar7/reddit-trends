from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models.schemas import PostIn
from app.repositories.posts import store_posts
from app.repositories.emerging_topics import store_emerging_topic_snapshots
from app.services.trends import detect_emerging_topics


def test_emerging_topics_detection(client):
    now = datetime.now(tz=timezone.utc)
    current = (now - timedelta(minutes=10)).isoformat()
    prev = (now - timedelta(minutes=90)).isoformat()

    posts = [
        PostIn(
            id="e1",
            timestamp=current,
            subreddit="movies",
            title="Disney reveal",
            body="disney disney",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="e2",
            timestamp=current,
            subreddit="movies",
            title="Disney update",
            body="disney disney https://example.com",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="e3",
            timestamp=current,
            subreddit="movies",
            title="Original disney news",
            body="disney says new",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="e4",
            timestamp=prev,
            subreddit="movies",
            title="Previous window",
            body="movie release",
            score=1,
            comment_count=0,
        ),
    ]

    store_posts(posts)
    records = detect_emerging_topics()
    assert records
    topics = {record.topic for record in records}
    assert "disney" in topics
    assert "https" not in topics
    assert "new" not in topics
    assert "original" not in topics
    assert "says" not in topics

    store_emerging_topic_snapshots(records)
    response = client.get("/analytics/emerging-topics?hours=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert any(item["topic"] == "disney" for item in data)

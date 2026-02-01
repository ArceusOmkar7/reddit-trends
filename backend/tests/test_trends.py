from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import settings
from app.models.schemas import PostIn
from app.repositories.posts import store_posts
from app.repositories.trends import store_trends
from app.services.trends import detect_trends


def test_trend_detection(client):
    settings.keywords = "ai releases,climate"
    now = datetime.now(tz=timezone.utc).isoformat()
    posts = [
        PostIn(
            id="t1",
            timestamp=now,
            subreddit="technology",
            title="AI releases are here",
            body="Big ai releases for 2026",
            score=1,
            comment_count=0,
        ),
        PostIn(
            id="t2",
            timestamp=now,
            subreddit="science",
            title="Climate event",
            body="climate climate climate",
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
    keywords = {item["keyword"] for item in data}
    assert "ai releases" in keywords
    assert "climate" in keywords

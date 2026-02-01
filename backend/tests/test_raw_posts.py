from __future__ import annotations

from datetime import datetime, timezone

from app.models.schemas import PostIn
from app.repositories.posts import store_posts


def test_raw_posts_empty(client):
    response = client.get("/raw/posts")
    assert response.status_code == 200
    assert response.json() == []


def test_raw_posts_with_data(client):
    now = datetime.now(tz=timezone.utc).isoformat()
    store_posts(
        [
            PostIn(
                id="post-1",
                timestamp=now,
                subreddit="technology",
                title="Test",
                body="Hello",
                score=10,
                comment_count=2,
            )
        ]
    )

    response = client.get("/raw/posts?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "post-1"

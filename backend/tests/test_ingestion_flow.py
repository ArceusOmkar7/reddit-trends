from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.clients import reddit as reddit_module
from app.core.config import settings
from app.db.database import get_connection
from app.services.ingestion import poll_reddit


def _count_rows(table: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) AS count FROM {table};")
    row = cursor.fetchone()
    connection.close()
    return int(row["count"])


@pytest.mark.anyio
async def test_ingestion_persists_posts_sentiment_and_trends(monkeypatch, temp_db):
    settings.subreddits = "technology,science"
    settings.keywords = "ai releases,climate"

    async def fake_fetch_new_posts(self, subreddit: str, limit: int = 50):
        now = datetime.now(tz=timezone.utc).timestamp()
        return [
            {
                "id": f"{subreddit}-1",
                "created_utc": now,
                "title": "AI releases are great" if subreddit == "technology" else "Climate update",
                "selftext": "Strong growth" if subreddit == "technology" else "climate climate",
                "score": 5,
                "num_comments": 2,
            }
        ]

    monkeypatch.setattr(reddit_module.RedditClient, "fetch_new_posts", fake_fetch_new_posts)

    await poll_reddit()

    assert _count_rows("posts") == 2
    assert _count_rows("sentiment_series") >= 2
    assert _count_rows("trend_snapshots") >= 2

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime, timezone
from uuid import uuid4

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.db.database import get_connection
from app.models.schemas import PostIn, SentimentRecord
from app.repositories.subreddits import get_or_create_subreddit_id

logger = logging.getLogger("reddit_trends.sentiment")

_analyzer: SentimentIntensityAnalyzer | None = None


def _get_analyzer() -> SentimentIntensityAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def score_text_detail(text: str) -> dict[str, float]:
    analyzer = _get_analyzer()
    scores = analyzer.polarity_scores(text or "")
    return {
        "compound": float(scores.get("compound", 0.0)),
        "pos": float(scores.get("pos", 0.0)),
        "neg": float(scores.get("neg", 0.0)),
        "neu": float(scores.get("neu", 0.0)),
    }


def score_text(text: str) -> float:
    return score_text_detail(text).get("compound", 0.0)


def aggregate_sentiment(posts: list[PostIn]) -> list[SentimentRecord]:
    subreddit_scores: dict[str, list[float]] = defaultdict(list)
    for post in posts:
        content = f"{post.title or ''} {post.body or ''}".strip()
        subreddit_scores[post.subreddit].append(score_text(content))

    timestamp = datetime.now(tz=timezone.utc).isoformat()
    records: list[SentimentRecord] = []

    for subreddit, scores in subreddit_scores.items():
        avg = sum(scores) / max(len(scores), 1)
        subreddit_id = get_or_create_subreddit_id(subreddit) if subreddit else None
        records.append(
            SentimentRecord(
                id=str(uuid4()),
                timestamp=timestamp,
                context="subreddit",
                label=subreddit,
                sentiment=round(avg, 4),
                subreddit_id=subreddit_id,
            )
        )

    logger.info("Sentiment aggregated", extra={"records": len(records)})
    return records


def score_posts(posts: list[PostIn]) -> list[tuple[str, float, float, float, float]]:
    payload: list[tuple[str, float, float, float, float]] = []
    for post in posts:
        if not post.id:
            continue
        content = f"{post.title or ''} {post.body or ''}".strip()
        scores = score_text_detail(content)
        payload.append(
            (
                post.id,
                scores["compound"],
                scores["pos"],
                scores["neg"],
                scores["neu"],
            )
        )
    return payload


def backfill_post_sentiment(batch_size: int = 500) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, title, body
        FROM posts
        WHERE sentiment_compound IS NULL
        LIMIT ?
        """,
        (batch_size,),
    )
    rows = cursor.fetchall()
    if not rows:
        connection.close()
        return 0

    updates: list[tuple[float, float, float, float, str]] = []
    for row in rows:
        content = f"{row['title'] or ''} {row['body'] or ''}".strip()
        scores = score_text_detail(content)
        updates.append(
            (
                scores["compound"],
                scores["pos"],
                scores["neg"],
                scores["neu"],
                row["id"],
            )
        )

    cursor.executemany(
        """
        UPDATE posts
        SET sentiment_compound = ?,
            sentiment_pos = ?,
            sentiment_neg = ?,
            sentiment_neu = ?
        WHERE id = ?
        """,
        updates,
    )
    connection.commit()
    connection.close()
    logger.info("Backfilled post sentiment | updated=%s", len(updates))
    return len(updates)

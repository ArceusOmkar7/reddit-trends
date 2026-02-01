from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime, timezone
from uuid import uuid4

from app.models.schemas import PostIn, SentimentRecord
from app.repositories.subreddits import get_or_create_subreddit_id

logger = logging.getLogger("reddit_trends.sentiment")

POSITIVE_WORDS = {
    "good",
    "great",
    "positive",
    "growth",
    "win",
    "success",
    "improve",
    "bull",
    "up",
    "gain",
    "strong",
    "optimistic",
}

NEGATIVE_WORDS = {
    "bad",
    "poor",
    "negative",
    "loss",
    "fail",
    "decline",
    "bear",
    "down",
    "drop",
    "weak",
    "concern",
    "crisis",
}


def score_text(text: str) -> float:
    words = [word.strip(".,!?;:()[]{}\"").lower() for word in text.split()]
    if not words:
        return 0.0

    pos = sum(1 for word in words if word in POSITIVE_WORDS)
    neg = sum(1 for word in words if word in NEGATIVE_WORDS)
    if pos == 0 and neg == 0:
        return 0.0
    return (pos - neg) / max(pos + neg, 1)


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

from __future__ import annotations

import logging
import re
from collections import Counter
from datetime import datetime, timezone
from uuid import uuid4

from app.core.config import settings
from app.models.schemas import PostIn, TrendSnapshotRecord
from app.repositories.events import get_event_id_by_name
from app.repositories.keywords import get_or_create_keyword_id
from app.repositories.post_keywords import store_post_keywords
from app.repositories.trends import get_latest_keyword_snapshot

logger = logging.getLogger("reddit_trends.trends")


def parse_scope(value: str) -> list[str]:
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def detect_trends(posts: list[PostIn]) -> list[TrendSnapshotRecord]:
    keywords = parse_scope(settings.keywords)
    if not keywords:
        return []

    corpus = " ".join(
        f"{post.title or ''} {post.body or ''}".lower() for post in posts
    )

    counts = Counter()
    per_post_mappings: list[tuple[str, int, int]] = []

    for keyword in keywords:
        pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
        total = len(pattern.findall(corpus))
        counts[keyword] = total

        keyword_id = get_or_create_keyword_id(keyword)
        for post in posts:
            content = f"{post.title or ''} {post.body or ''}".lower()
            count = len(pattern.findall(content))
            if count > 0:
                per_post_mappings.append((post.id, keyword_id, count))

    timestamp = datetime.now(tz=timezone.utc).isoformat()
    records: list[TrendSnapshotRecord] = []

    for keyword, count in counts.items():
        previous = get_latest_keyword_snapshot(keyword)
        previous_velocity = previous.velocity if previous else 0.0
        spike = count / max(previous_velocity, 1.0)
        keyword_id = get_or_create_keyword_id(keyword)
        event_id = get_event_id_by_name(keyword)

        records.append(
            TrendSnapshotRecord(
                id=str(uuid4()),
                timestamp=timestamp,
                keyword=keyword,
                velocity=float(count),
                spike=round(float(spike), 4),
                context="global",
                keyword_id=keyword_id,
                event_id=event_id,
            )
        )

    if per_post_mappings:
        store_post_keywords(per_post_mappings)

    logger.info("Trend detection complete", extra={"records": len(records)})
    return records

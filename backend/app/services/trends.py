from __future__ import annotations

import logging
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.db.database import get_connection
from app.models.schemas import EmergingTopicRecord, PostIn, TrendSnapshotRecord
from app.repositories.emerging_topics import fetch_existing_topics, get_or_create_topic_id
from app.repositories.keywords import get_or_create_keyword_id
from app.services.nlp import filter_stopwords, tokenize

logger = logging.getLogger("reddit_trends.trends")


WINDOW_HOURS = 1
_URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
_DENYLIST = {"says", "said", "new", "original", "today", "breaking"}
_MIN_TERM_LENGTH = 4


def _align_hour(value: datetime) -> datetime:
    return value.replace(minute=0, second=0, microsecond=0)


def _window_bounds_at(end: datetime) -> tuple[datetime, datetime, datetime, datetime]:
    aligned_end = _align_hour(end)
    start = aligned_end - timedelta(hours=WINDOW_HOURS)
    prev_start = start - timedelta(hours=WINDOW_HOURS)
    return start, aligned_end, prev_start, start


def _window_bounds() -> tuple[datetime, datetime, datetime, datetime]:
    return _window_bounds_at(datetime.now(tz=timezone.utc))


def _fetch_posts_in_window(start: str, end: str) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, timestamp, title, body, score, comment_count
        FROM posts
        WHERE timestamp >= ? AND timestamp < ?
        """,
        (start, end),
    )
    rows = cursor.fetchall()
    connection.close()
    return rows


def fetch_posts_since(hours: int) -> list[PostIn]:
    start = datetime.now(tz=timezone.utc) - timedelta(hours=hours)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT p.id, p.timestamp, p.title, p.body, p.score, p.comment_count, r.name AS subreddit
        FROM posts p
        LEFT JOIN subreddits r ON r.id = p.subreddit_id
        WHERE p.timestamp >= ?
        """,
        (start.isoformat(),),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        PostIn(
            id=row["id"],
            timestamp=row["timestamp"],
            subreddit=row["subreddit"] or "",
            title=row["title"],
            body=row["body"],
            score=int(row["score"] or 0),
            comment_count=int(row["comment_count"] or 0),
        )
        for row in rows
    ]


def _extract_terms(text: str) -> list[str]:
    cleaned_text = _URL_PATTERN.sub(" ", text or "")
    tokens = filter_stopwords(tokenize(cleaned_text))
    return [
        token
        for token in tokens
        if token.isalpha()
        and len(token) >= _MIN_TERM_LENGTH
        and token not in _DENYLIST
    ]


def _extract_terms_for_post(text: str) -> list[str]:
    cleaned_text = _URL_PATTERN.sub(" ", text or "")
    tokens = filter_stopwords(tokenize(cleaned_text))
    cleaned = [
        token
        for token in tokens
        if token.isalpha()
        and len(token) >= _MIN_TERM_LENGTH
        and token not in _DENYLIST
    ]
    terms = list(cleaned)
    if len(cleaned) > 1:
        terms.extend(
            f"{cleaned[i]} {cleaned[i + 1]}" for i in range(len(cleaned) - 1)
        )
    return terms


def _window_term_stats(start: str, end: str) -> tuple[Counter[str], dict[str, float]]:
    rows = _fetch_posts_in_window(start, end)
    counts: Counter[str] = Counter()
    weighted: dict[str, float] = defaultdict(float)

    for row in rows:
        post_id = row["id"]
        content = f"{row['title'] or ''} {row['body'] or ''}".strip()
        if not content:
            continue
        terms = _extract_terms_for_post(content)
        if not terms:
            continue
        per_post_counts = Counter(terms)
        counts.update(per_post_counts)

        score = int(row["score"] or 0)
        comments = int(row["comment_count"] or 0)
        weight = math.log(1 + score + comments)
        for term, count in per_post_counts.items():
            weighted[term] += count * weight

    return counts, weighted


def detect_trends(posts: list[PostIn]) -> list[TrendSnapshotRecord]:
    start, end, prev_start, prev_end = _window_bounds()
    return detect_trends_for_window(end)


def detect_trends_for_window(end: datetime) -> list[TrendSnapshotRecord]:
    start, end, prev_start, prev_end = _window_bounds_at(end)
    current_counts, current_weighted = _window_term_stats(
        start.isoformat(), end.isoformat()
    )
    previous_counts, _ = _window_term_stats(
        prev_start.isoformat(), prev_end.isoformat()
    )

    timestamp = end.isoformat()
    records: list[TrendSnapshotRecord] = []

    for term, current in current_counts.items():
        if current < 5:
            continue
        previous = int(previous_counts.get(term, 0))
        velocity = (current - previous) / max(previous, 1)
        spike = current / max(previous, 1)
        keyword_id = get_or_create_keyword_id(term)

        records.append(
            TrendSnapshotRecord(
                id=str(uuid4()),
                timestamp=timestamp,
                keyword=term,
                velocity=round(float(velocity), 4),
                spike=round(float(spike), 4),
                context="global",
                keyword_id=keyword_id,
                event_id=None,
                raw_mentions=int(current),
                weighted_mentions=round(float(current_weighted.get(term, 0.0)), 4),
                previous_mentions=int(previous),
                window_start=start.isoformat(),
                window_end=end.isoformat(),
            )
        )

    logger.info("Trend detection complete", extra={"records": len(records)})
    return records


def detect_emerging_topics() -> list[EmergingTopicRecord]:
    return detect_emerging_topics_for_window(datetime.now(tz=timezone.utc))


def detect_emerging_topics_for_window(end: datetime) -> list[EmergingTopicRecord]:
    start, end, prev_start, prev_end = _window_bounds_at(end)
    current_posts = _fetch_posts_in_window(start.isoformat(), end.isoformat())
    prev_posts = _fetch_posts_in_window(prev_start.isoformat(), prev_end.isoformat())

    current_counts: Counter[str] = Counter()
    current_unique: dict[str, set[str]] = defaultdict(set)
    current_first_seen: dict[str, str] = {}

    for row in current_posts:
        post_id = row["id"]
        content = f"{row['title'] or ''} {row['body'] or ''}".strip()
        terms = _extract_terms(content)
        if not terms:
            continue
        current_counts.update(terms)
        for term in set(terms):
            current_unique[term].add(post_id)
            if term not in current_first_seen or row["timestamp"] < current_first_seen[term]:
                current_first_seen[term] = row["timestamp"]

        if len(terms) > 1:
            bigrams = [
                f"{terms[i]} {terms[i + 1]}" for i in range(len(terms) - 1)
            ]
            current_counts.update(bigrams)
            for term in set(bigrams):
                current_unique[term].add(post_id)
                if term not in current_first_seen or row["timestamp"] < current_first_seen[term]:
                    current_first_seen[term] = row["timestamp"]

    prev_counts: Counter[str] = Counter()
    for row in prev_posts:
        content = f"{row['title'] or ''} {row['body'] or ''}".strip()
        terms = _extract_terms(content)
        if not terms:
            continue
        prev_counts.update(terms)
        if len(terms) > 1:
            bigrams = [
                f"{terms[i]} {terms[i + 1]}" for i in range(len(terms) - 1)
            ]
            prev_counts.update(bigrams)

    if not current_counts:
        return []

    existing_topics = fetch_existing_topics(list(current_counts.keys()))
    records: list[EmergingTopicRecord] = []
    now_iso = end.isoformat()

    for topic, count in current_counts.items():
        unique_posts = len(current_unique.get(topic, set()))
        if count < 5 or unique_posts < 3:
            continue
        prev_count = int(prev_counts.get(topic, 0))
        velocity = (count - prev_count) / max(prev_count, 1)
        if velocity < 1.0:
            continue

        if topic in existing_topics:
            topic_id, first_seen = existing_topics[topic]
        else:
            first_seen = current_first_seen.get(topic, now_iso)
            topic_id = get_or_create_topic_id(topic, first_seen)

        first_seen_dt = datetime.fromisoformat(first_seen)
        if (end - first_seen_dt) > timedelta(hours=24):
            continue

        records.append(
            EmergingTopicRecord(
                id=str(uuid4()),
                timestamp=now_iso,
                topic=topic,
                raw_mentions=count,
                unique_posts=unique_posts,
                velocity=round(float(velocity), 4),
                window_start=start.isoformat(),
                window_end=end.isoformat(),
                context="global",
                topic_id=topic_id,
            )
        )

    logger.info("Emerging topic detection complete", extra={"records": len(records)})
    return records

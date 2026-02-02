from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger("reddit_trends.db")


def _resolve_sqlite_path(database_url: str) -> Path:
    if database_url == "sqlite:///:memory:":
        return Path(":memory:")
    if database_url.startswith("sqlite:///" ):
        return Path(database_url.replace("sqlite:///", "", 1))
    raise ValueError("Only sqlite:/// URLs are supported in this prototype")


def get_connection() -> sqlite3.Connection:
    path = _resolve_sqlite_path(settings.database_url)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def init_db() -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subreddits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT NOT NULL UNIQUE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS event_keywords (
            event_id INTEGER NOT NULL,
            keyword_id INTEGER NOT NULL,
            PRIMARY KEY (event_id, keyword_id),
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            subreddit_id INTEGER NOT NULL,
            title TEXT,
            body TEXT,
            score INTEGER,
            comment_count INTEGER,
            FOREIGN KEY (subreddit_id) REFERENCES subreddits(id) ON DELETE SET NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS post_keywords (
            post_id TEXT NOT NULL,
            keyword_id INTEGER NOT NULL,
            count INTEGER NOT NULL,
            PRIMARY KEY (post_id, keyword_id),
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            subreddit_id INTEGER NOT NULL,
            post_id TEXT NOT NULL,
            body TEXT,
            score INTEGER,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (subreddit_id) REFERENCES subreddits(id) ON DELETE SET NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiment_series (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            context TEXT NOT NULL,
            sentiment REAL NOT NULL,
            subreddit_id INTEGER,
            event_id INTEGER,
            FOREIGN KEY (subreddit_id) REFERENCES subreddits(id) ON DELETE SET NULL,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trend_snapshots (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            keyword_id INTEGER NOT NULL,
            velocity REAL NOT NULL,
            spike REAL NOT NULL,
            context TEXT NOT NULL,
            subreddit_id INTEGER,
            event_id INTEGER,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
            FOREIGN KEY (subreddit_id) REFERENCES subreddits(id) ON DELETE SET NULL,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS emerging_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT NOT NULL UNIQUE,
            first_seen TEXT NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS emerging_topic_snapshots (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            topic_id INTEGER NOT NULL,
            raw_mentions INTEGER NOT NULL,
            unique_posts INTEGER NOT NULL,
            velocity REAL NOT NULL,
            window_start TEXT NOT NULL,
            window_end TEXT NOT NULL,
            context TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES emerging_topics(id) ON DELETE CASCADE
        );
        """
    )

    def ensure_column(table: str, column: str, definition: str) -> None:
        cursor.execute(f"PRAGMA table_info({table});")
        existing = {row[1] for row in cursor.fetchall()}
        if column not in existing:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {definition};")

    ensure_column("posts", "subreddit_id", "subreddit_id INTEGER")
    ensure_column("posts", "sentiment_compound", "sentiment_compound REAL")
    ensure_column("posts", "sentiment_pos", "sentiment_pos REAL")
    ensure_column("posts", "sentiment_neg", "sentiment_neg REAL")
    ensure_column("posts", "sentiment_neu", "sentiment_neu REAL")
    ensure_column("comments", "subreddit_id", "subreddit_id INTEGER")
    ensure_column("sentiment_series", "subreddit_id", "subreddit_id INTEGER")
    ensure_column("sentiment_series", "event_id", "event_id INTEGER")
    ensure_column("trend_snapshots", "subreddit_id", "subreddit_id INTEGER")
    ensure_column("trend_snapshots", "event_id", "event_id INTEGER")
    ensure_column("trend_snapshots", "raw_mentions", "raw_mentions INTEGER")
    ensure_column("trend_snapshots", "weighted_mentions", "weighted_mentions REAL")
    ensure_column("trend_snapshots", "previous_mentions", "previous_mentions INTEGER")
    ensure_column("trend_snapshots", "window_start", "window_start TEXT")
    ensure_column("trend_snapshots", "window_end", "window_end TEXT")

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_posts_subreddit_id_time ON posts(subreddit_id, timestamp);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_sentiment_context_time ON sentiment_series(context, timestamp);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_trends_keyword_time ON trend_snapshots(keyword_id, timestamp);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_trends_window ON trend_snapshots(window_start, window_end);"
    )
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ux_trends_keyword_window
        ON trend_snapshots(keyword_id, window_start, window_end);
        """
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_emerging_topics_phrase ON emerging_topics(phrase);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_emerging_topic_snapshots_time ON emerging_topic_snapshots(timestamp);"
    )

    cursor.execute(
        """
        DELETE FROM emerging_topic_snapshots
        WHERE window_start IS NULL OR window_end IS NULL
        """
    )
    cursor.execute(
        """
        DELETE FROM emerging_topic_snapshots
        WHERE rowid NOT IN (
            SELECT MAX(rowid)
            FROM emerging_topic_snapshots
            GROUP BY topic_id, window_start, window_end
        )
        """
    )
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ux_emerging_topic_window
        ON emerging_topic_snapshots(topic_id, window_start, window_end);
        """
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_post_keywords_keyword ON post_keywords(keyword_id);"
    )

    keywords = [item.strip().lower() for item in settings.keywords.split(",") if item.strip()]
    if keywords:
        cursor.executemany(
            "INSERT OR IGNORE INTO keywords (phrase) VALUES (?);",
            [(keyword,) for keyword in keywords],
        )
        cursor.executemany(
            "INSERT OR IGNORE INTO events (name) VALUES (?);",
            [(keyword,) for keyword in keywords],
        )
        cursor.executemany(
            """
            INSERT OR IGNORE INTO event_keywords (event_id, keyword_id)
            SELECT e.id, k.id
            FROM events e
            JOIN keywords k ON k.phrase = e.name
            WHERE e.name = ?
            """,
            [(keyword,) for keyword in keywords],
        )

    cursor.execute(
        """
        DELETE FROM trend_snapshots
        WHERE raw_mentions IS NULL OR window_start IS NULL
        """
    )

    connection.commit()
    connection.close()
    logger.info("Database initialized")

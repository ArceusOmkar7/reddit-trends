from __future__ import annotations

from app.db.database import get_connection, init_db


def test_db_schema_tables_and_columns(temp_db):
    init_db()
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row["name"] for row in cursor.fetchall()}
    assert {"posts", "comments", "sentiment_series", "trend_snapshots"}.issubset(tables)
    assert {"subreddits", "events", "keywords", "event_keywords"}.issubset(tables)

    cursor.execute("PRAGMA table_info(posts);")
    columns = {row["name"] for row in cursor.fetchall()}
    assert "subreddit_id" in columns

    cursor.execute("PRAGMA table_info(comments);")
    columns = {row["name"] for row in cursor.fetchall()}
    assert "subreddit_id" in columns

    cursor.execute("PRAGMA table_info(sentiment_series);")
    columns = {row["name"] for row in cursor.fetchall()}
    assert "subreddit_id" in columns
    assert "event_id" in columns

    cursor.execute("PRAGMA table_info(trend_snapshots);")
    columns = {row["name"] for row in cursor.fetchall()}
    assert "keyword_id" in columns
    assert "subreddit_id" in columns
    assert "event_id" in columns

    connection.close()

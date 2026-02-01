from __future__ import annotations

from app.repositories.trends import get_latest_keyword_snapshot


def test_latest_keyword_snapshot_empty(temp_db):
    assert get_latest_keyword_snapshot("nonexistent") is None

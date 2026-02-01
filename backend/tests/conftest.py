from __future__ import annotations

from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import settings
from app.db.database import init_db
from app.main import app


@pytest.fixture()
def temp_db(tmp_path: Path):
    db_path = tmp_path / "test.db"
    settings.database_url = f"sqlite:///{db_path.as_posix()}"
    init_db()
    yield db_path


@pytest.fixture()
def client(temp_db: Path):
    return TestClient(app)

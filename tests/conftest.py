"""Shared test fixtures.

watch.py opens its SQLAlchemy engine and runs schema migrations at import
time (module-level code, not inside a function) against whatever
DATABASE_URL is set when it's first imported. That import happens as a
side effect of importing `main` (main.py includes watch's router), so the
env var has to be pointed at an isolated file before anything in the app
package is imported -- doing it inside a fixture would run too late.
"""

import os
import tempfile

_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"

import pytest
from fastapi.testclient import TestClient

import main
import watch


@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture(autouse=True)
def _reset_watch_tables():
    """Every watch.py test shares the one on-disk sqlite file (set up
    above), so wipe its tables after each test to keep them isolated."""
    yield
    with watch.engine.begin() as conn:
        conn.execute(watch.ComparisonRow.__table__.delete())
        conn.execute(watch.LikeRow.__table__.delete())
        conn.execute(watch.DislikeRow.__table__.delete())
        conn.execute(watch.VideoRow.__table__.delete())


@pytest.fixture
def make_video():
    """Inserts a VideoRow with sensible defaults, overridable per test."""

    def _make(**overrides):
        defaults = dict(
            id="vid-1",
            language="es",
            youtube_id="yt-1",
            title="A video",
            channel="A channel",
            duration_seconds=120,
            difficulty_score=watch.DEFAULT_RATING,
            rating_deviation=watch.DEFAULT_RD,
            like_count=0,
            is_available=True,
        )
        defaults.update(overrides)
        video = watch.VideoRow(**defaults)
        with watch.SessionLocal() as db:
            db.add(video)
            db.commit()
        return defaults["id"]

    return _make

import math
import os
import random
from datetime import datetime, timezone
from typing import Literal

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import ForeignKey, String, create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

load_dotenv()

# DATABASE_URL points at Neon -- a Lambda env var in production, and .env
# locally (local dev uses the same prod DB for now). The sqlite branch is
# only for the test suite's throwaway DB (see tests/conftest.py).
DATABASE_URL = os.environ["DATABASE_URL"]
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Starting rating for a video with no comparisons yet, on the same 400-point
# logistic scale Elo uses -- that's why the CEFR cutoffs in level_for_score
# didn't need to change when this moved from Elo to Glicko. DEFAULT_RD is the
# starting rating deviation (Glickman's "RD"): how uncertain we are about
# that rating. A vote between two low-RD videos barely moves either one; a
# vote involving a fresh video swings its own rating hard until enough
# comparisons pull its RD down.
DEFAULT_RATING = 1000.0
DEFAULT_RD = 350.0

# Glicko constant that converts the 400-point logistic scale into the
# natural-log scale the rating math is defined in (Glickman, "Parameter
# Estimation in Large Dynamic Paired Comparison Experiments", 1999).
_Q = math.log(10) / 400


def _g(rd: float) -> float:
    """Shrinks the impact of an opponent's rating in proportion to how
    uncertain (high-RD) that opponent's own rating still is."""
    return 1 / math.sqrt(1 + 3 * _Q**2 * rd**2 / math.pi**2)


def _expected_score(rating: float, opponent_rating: float, opponent_rd: float) -> float:
    return 1 / (1 + 10 ** (-_g(opponent_rd) * (rating - opponent_rating) / 400))


def _glicko_update(
    rating: float, rd: float, opponent_rating: float, opponent_rd: float, score: float
) -> tuple[float, float]:
    """Single-comparison Glicko update: how `rating`/`rd` move after playing
    one game worth `score` (1.0 win, 0.5 draw, 0.0 loss) against an opponent.
    Call it once per side with the score mirrored for the other video."""
    g_opp = _g(opponent_rd)
    e = _expected_score(rating, opponent_rating, opponent_rd)
    d_squared = 1 / (_Q**2 * g_opp**2 * e * (1 - e))
    new_rd = math.sqrt(1 / (1 / rd**2 + 1 / d_squared))
    new_rating = rating + _Q * new_rd**2 * g_opp * (score - e)
    return new_rating, new_rd


class Base(DeclarativeBase):
    pass


class VideoRow(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    language: Mapped[str] = mapped_column(String, index=True)
    youtube_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String, index=True)
    duration_seconds: Mapped[int]
    difficulty_score: Mapped[float] = mapped_column(default=DEFAULT_RATING)
    rating_deviation: Mapped[float] = mapped_column(default=DEFAULT_RD)
    like_count: Mapped[int] = mapped_column(default=0)
    # Tracks when title/channel/duration were last pulled from the YouTube
    # Data API, and whether the video was still there the last time we
    # checked. YouTube's API terms cap cached data at 30 days before it must
    # be refreshed -- refresh_metadata.py re-syncs anything older than that
    # (see STALE_AFTER_DAYS) and flips is_available off for videos that have
    # gone private/deleted, so a stale title/duration never keeps serving.
    is_available: Mapped[bool] = mapped_column(default=True)
    metadata_synced_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class BlacklistedVideoRow(Base):
    """Videos that were deliberately removed and must never come back.

    Checked by import_channel.py before a video is inserted, so re-running an
    import on a channel that includes one of these doesn't reimport it. Keyed
    by youtube_id alone (not language) so a video already imported under
    multiple languages is blocked in all of them at once.
    """

    __tablename__ = "blacklisted_videos"

    youtube_id: Mapped[str] = mapped_column(String, primary_key=True)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class LikeRow(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    session_id: Mapped[str] = mapped_column(String)


class DislikeRow(Base):
    __tablename__ = "dislikes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    session_id: Mapped[str] = mapped_column(String)


class ComparisonRow(Base):
    __tablename__ = "comparisons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # video_id is whichever video the viewer picked as harder; result is kept
    # around for older rows (back when a vote could also be "easier" or
    # "same") but is always "harder" now that a vote is just picking the
    # harder of the two thumbnails -- video_id/previous_video_id alone say
    # which video that was.
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    previous_video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    result: Mapped[str] = mapped_column(String)
    session_id: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(bind=engine)

# create_all only creates missing tables, not missing columns on tables that
# already existed -- is_available/metadata_synced_at were added after some
# deployments already had a videos table, so add them by hand if needed.
_existing_video_columns = {col["name"] for col in inspect(engine).get_columns("videos")}
with engine.begin() as _conn:
    if "is_available" not in _existing_video_columns:
        _conn.execute(text("ALTER TABLE videos ADD COLUMN is_available BOOLEAN DEFAULT TRUE"))
    if "metadata_synced_at" not in _existing_video_columns:
        _conn.execute(text("ALTER TABLE videos ADD COLUMN metadata_synced_at TIMESTAMP"))
    if "rating_deviation" not in _existing_video_columns:
        _conn.execute(
            text(f"ALTER TABLE videos ADD COLUMN rating_deviation FLOAT DEFAULT {DEFAULT_RD}")
        )
        # Existing rows predate rating_deviation and get the column's default
        # via ALTER TABLE ... DEFAULT, but that only applies going forward on
        # some backends -- set it explicitly so every already-imported video
        # starts as uncertain as a brand new one, not at 0.
        _conn.execute(text(f"UPDATE videos SET rating_deviation = {DEFAULT_RD} WHERE rating_deviation IS NULL"))
    # create_all() only adds indexes when it creates a table from scratch, so
    # a channel index added after the table already existed in prod needs to
    # be created by hand too, same as the columns above. IF NOT EXISTS makes
    # this safe to run on every startup.
    _conn.execute(text("CREATE INDEX IF NOT EXISTS ix_videos_channel ON videos (channel)"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def level_for_score(score: float) -> str:
    if score < 700:
        return "a1"
    if score < 850:
        return "a2"
    if score < 1000:
        return "b1"
    if score < 1150:
        return "b2"
    if score < 1300:
        return "c1"
    return "c2"


class VideoResponse(BaseModel):
    id: str
    youtube_id: str
    title: str
    channel: str
    duration_seconds: int
    difficulty_score: float
    like_count: int

    model_config = {"from_attributes": True}


class LikeRequest(BaseModel):
    session_id: str


class CompareRequest(BaseModel):
    # The video in the URL path is always the one the viewer picked as
    # harder -- this is just the other half of the pair.
    easier_video_id: str
    session_id: str


class CompareResponse(BaseModel):
    harder_video: VideoResponse
    easier_video: VideoResponse


class VideoListResponse(BaseModel):
    items: list[VideoResponse]
    has_more: bool


router = APIRouter()


def get_video_or_404(db: Session, language: str, video_id: str) -> VideoRow:
    video = db.get(VideoRow, video_id)
    if not video or video.language != language or not video.is_available:
        raise HTTPException(status_code=404, detail=f"Video '{video_id}' not found")
    return video


@router.get("/{language}/videos", response_model=VideoListResponse)
def list_videos(
    language: str,
    level: Literal["a1", "a2", "b1", "b2", "c1", "c2"] | None = None,
    sort: Literal["easiest", "hardest", "most-liked", "random"] = "random",
    # Only used for sort=random: the frontend generates one seed when a
    # browsing session starts (new filters, new sort, fresh page load) and
    # reuses it for every "load more" call in that session. Without a
    # shared seed, each page would reshuffle independently -- the same
    # video could turn up on multiple pages while others never appear.
    seed: int | None = None,
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    videos = (
        db.query(VideoRow)
        .filter(VideoRow.language == language, VideoRow.is_available.is_(True))
        .all()
    )

    if level:
        videos = [v for v in videos if level_for_score(v.difficulty_score) == level]

    if sort == "easiest":
        videos.sort(key=lambda v: v.difficulty_score)
    elif sort == "hardest":
        videos.sort(key=lambda v: v.difficulty_score, reverse=True)
    elif sort == "most-liked":
        videos.sort(key=lambda v: v.like_count, reverse=True)
    else:
        # Most videos still share the same cold-start rating (see
        # DEFAULT_RATING), so an "easiest first" default would show the same
        # handful of videos in the same order on every visit. Randomizing
        # gives actual variety until real comparisons spread the ratings out.
        random.Random(seed).shuffle(videos)

    page = videos[offset : offset + limit]
    return {"items": page, "has_more": offset + limit < len(videos)}


@router.get("/{language}/videos/{video_id}", response_model=VideoResponse)
def get_video(language: str, video_id: str, db: Session = Depends(get_db)):
    return get_video_or_404(db, language, video_id)


@router.get("/{language}/videos/{video_id}/related", response_model=list[VideoResponse])
def list_related_videos(
    language: str,
    video_id: str,
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Other videos from the same channel, for the "more from this creator"
    rail under the player -- most-liked first, since that's the closest
    signal this app has to "worth watching next" for a given channel."""
    video = get_video_or_404(db, language, video_id)
    return (
        db.query(VideoRow)
        .filter(
            VideoRow.language == language,
            VideoRow.channel == video.channel,
            VideoRow.is_available.is_(True),
            VideoRow.id != video_id,
        )
        .order_by(VideoRow.like_count.desc())
        .limit(limit)
        .all()
    )


@router.post("/{language}/videos/{video_id}/like", response_model=VideoResponse)
def toggle_like(language: str, video_id: str, body: LikeRequest, db: Session = Depends(get_db)):
    video = get_video_or_404(db, language, video_id)

    # A session can only be in one of the two states at a time, so liking
    # first clears any standing dislike (undoing its -1) before applying
    # the like toggle -- that's what keeps like_count a single net score
    # instead of letting both counts move independently.
    existing_dislike = (
        db.query(DislikeRow)
        .filter_by(video_id=video_id, session_id=body.session_id)
        .first()
    )
    if existing_dislike:
        db.delete(existing_dislike)
        video.like_count += 1

    existing_like = (
        db.query(LikeRow)
        .filter_by(video_id=video_id, session_id=body.session_id)
        .first()
    )
    if existing_like:
        db.delete(existing_like)
        video.like_count -= 1
    else:
        db.add(LikeRow(video_id=video_id, session_id=body.session_id))
        video.like_count += 1

    db.commit()
    db.refresh(video)
    return video


@router.post("/{language}/videos/{video_id}/dislike", response_model=VideoResponse)
def toggle_dislike(language: str, video_id: str, body: LikeRequest, db: Session = Depends(get_db)):
    video = get_video_or_404(db, language, video_id)

    existing_like = (
        db.query(LikeRow)
        .filter_by(video_id=video_id, session_id=body.session_id)
        .first()
    )
    if existing_like:
        db.delete(existing_like)
        video.like_count -= 1

    existing_dislike = (
        db.query(DislikeRow)
        .filter_by(video_id=video_id, session_id=body.session_id)
        .first()
    )
    if existing_dislike:
        db.delete(existing_dislike)
        video.like_count += 1
    else:
        db.add(DislikeRow(video_id=video_id, session_id=body.session_id))
        video.like_count -= 1

    db.commit()
    db.refresh(video)
    return video


@router.post("/{language}/videos/{video_id}/compare", response_model=CompareResponse)
def compare_videos(
    language: str, video_id: str, body: CompareRequest, db: Session = Depends(get_db)
):
    harder = get_video_or_404(db, language, video_id)
    easier = get_video_or_404(db, language, body.easier_video_id)

    # Same dedupe idea as toggle_like, but a compare isn't a toggle -- once a
    # session has voted on this pair, in either order, later attempts are a
    # no-op instead of moving the score again.
    already_voted = (
        db.query(ComparisonRow)
        .filter(
            ComparisonRow.session_id == body.session_id,
            ComparisonRow.video_id.in_([video_id, body.easier_video_id]),
            ComparisonRow.previous_video_id.in_([video_id, body.easier_video_id]),
        )
        .first()
        is not None
    )

    if not already_voted:
        # Both updates read each other's pre-update rating/RD, so compute
        # them from the original values before either one is written.
        new_harder_rating, new_harder_rd = _glicko_update(
            harder.difficulty_score,
            harder.rating_deviation,
            easier.difficulty_score,
            easier.rating_deviation,
            1.0,
        )
        new_easier_rating, new_easier_rd = _glicko_update(
            easier.difficulty_score,
            easier.rating_deviation,
            harder.difficulty_score,
            harder.rating_deviation,
            0.0,
        )
        harder.difficulty_score, harder.rating_deviation = new_harder_rating, new_harder_rd
        easier.difficulty_score, easier.rating_deviation = new_easier_rating, new_easier_rd

        db.add(
            ComparisonRow(
                video_id=video_id,
                previous_video_id=body.easier_video_id,
                result="harder",
                session_id=body.session_id,
            )
        )
        db.commit()
        db.refresh(harder)
        db.refresh(easier)

    return {"harder_video": harder, "easier_video": easier}

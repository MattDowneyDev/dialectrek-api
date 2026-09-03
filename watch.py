import os
import random
from datetime import datetime, timezone
from typing import Literal

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

load_dotenv()

# DATABASE_URL points at Neon in production (set as a Lambda env var) and
# falls back to a local SQLite file so nobody needs a real DB for dev.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./watch.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Starting rating for a video with no comparisons yet, and how many points a
# single "harder/easier" vote moves the two videos being compared. These are
# arbitrary Elo-style constants -- what matters is the gap between them, not
# the absolute numbers.
DEFAULT_RATING = 1000.0
RATING_STEP = 40.0


class Base(DeclarativeBase):
    pass


class VideoRow(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    language: Mapped[str] = mapped_column(String, index=True)
    youtube_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String)
    duration_seconds: Mapped[int]
    difficulty_score: Mapped[float] = mapped_column(default=DEFAULT_RATING)
    like_count: Mapped[int] = mapped_column(default=0)


class LikeRow(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    session_id: Mapped[str] = mapped_column(String)


class ComparisonRow(Base):
    __tablename__ = "comparisons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    previous_video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"))
    result: Mapped[str] = mapped_column(String)
    session_id: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def level_for_score(score: float) -> str:
    if score < 700:
        return "novice"
    if score < 1000:
        return "beginner"
    if score < 1300:
        return "intermediate"
    return "advanced"


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
    previous_video_id: str
    result: Literal["easier", "same", "harder"]
    session_id: str


class CompareResponse(BaseModel):
    video: VideoResponse
    previous_video: VideoResponse


class VideoListResponse(BaseModel):
    items: list[VideoResponse]
    has_more: bool


router = APIRouter()


def get_video_or_404(db: Session, language: str, video_id: str) -> VideoRow:
    video = db.get(VideoRow, video_id)
    if not video or video.language != language:
        raise HTTPException(status_code=404, detail=f"Video '{video_id}' not found")
    return video


@router.get("/{language}/videos", response_model=VideoListResponse)
def list_videos(
    language: str,
    level: Literal["novice", "beginner", "intermediate", "advanced"] | None = None,
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
    videos = db.query(VideoRow).filter(VideoRow.language == language).all()

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


@router.post("/{language}/videos/{video_id}/like", response_model=VideoResponse)
def toggle_like(language: str, video_id: str, body: LikeRequest, db: Session = Depends(get_db)):
    video = get_video_or_404(db, language, video_id)

    existing = (
        db.query(LikeRow)
        .filter_by(video_id=video_id, session_id=body.session_id)
        .first()
    )
    if existing:
        db.delete(existing)
        video.like_count -= 1
    else:
        db.add(LikeRow(video_id=video_id, session_id=body.session_id))
        video.like_count += 1

    db.commit()
    db.refresh(video)
    return video


@router.post("/{language}/videos/{video_id}/compare", response_model=CompareResponse)
def compare_videos(
    language: str, video_id: str, body: CompareRequest, db: Session = Depends(get_db)
):
    video = get_video_or_404(db, language, video_id)
    previous = get_video_or_404(db, language, body.previous_video_id)

    # Same dedupe idea as toggle_like, but a compare isn't a toggle -- once a
    # session has voted on this pair, in either order, later attempts are a
    # no-op instead of moving the score again.
    already_voted = (
        db.query(ComparisonRow)
        .filter(
            ComparisonRow.session_id == body.session_id,
            ComparisonRow.video_id.in_([video_id, body.previous_video_id]),
            ComparisonRow.previous_video_id.in_([video_id, body.previous_video_id]),
        )
        .first()
        is not None
    )

    if not already_voted:
        if body.result != "same":
            delta = RATING_STEP if body.result == "harder" else -RATING_STEP
            video.difficulty_score += delta
            previous.difficulty_score -= delta

        db.add(
            ComparisonRow(
                video_id=video_id,
                previous_video_id=body.previous_video_id,
                result=body.result,
                session_id=body.session_id,
            )
        )
        db.commit()
        db.refresh(video)
        db.refresh(previous)

    return {"video": video, "previous_video": previous}

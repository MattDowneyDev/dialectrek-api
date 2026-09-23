"""Blacklists a video so import_channel.py never (re)imports it, and by
default deletes any rows already in watch.db for it (all languages, plus
their likes/dislikes/comparisons).

Usage:
    venv/bin/python blacklist_video.py dQw4w9WgXcQ --reason "not actually Spanish"
    venv/bin/python blacklist_video.py https://youtube.com/watch?v=dQw4w9WgXcQ
    venv/bin/python blacklist_video.py dQw4w9WgXcQ --keep   # blacklist without deleting existing rows
    venv/bin/python blacklist_video.py dQw4w9WgXcQ --remove # un-blacklist
"""

import argparse
import re
from datetime import datetime, timezone

from sqlalchemy import or_

from watch import Base, BlacklistedVideoRow, ComparisonRow, DislikeRow, LikeRow, SessionLocal, VideoRow, engine


def extract_youtube_id(value: str) -> str:
    """Accepts a bare 11-char video id or a youtube.com/youtu.be URL."""
    match = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{11})", value)
    if match:
        return match.group(1)
    if re.fullmatch(r"[\w-]{11}", value):
        return value
    raise SystemExit(f"'{value}' doesn't look like a YouTube video id or URL")


def blacklist_video(youtube_id: str, reason: str | None, delete_existing: bool) -> None:
    db = SessionLocal()
    try:
        db.merge(
            BlacklistedVideoRow(youtube_id=youtube_id, reason=reason, created_at=datetime.now(timezone.utc))
        )

        if delete_existing:
            existing_ids = [
                row.id for row in db.query(VideoRow).filter(VideoRow.youtube_id == youtube_id).all()
            ]
            if existing_ids:
                db.query(LikeRow).filter(LikeRow.video_id.in_(existing_ids)).delete(synchronize_session=False)
                db.query(DislikeRow).filter(DislikeRow.video_id.in_(existing_ids)).delete(synchronize_session=False)
                db.query(ComparisonRow).filter(
                    or_(ComparisonRow.video_id.in_(existing_ids), ComparisonRow.previous_video_id.in_(existing_ids))
                ).delete(synchronize_session=False)
                db.query(VideoRow).filter(VideoRow.id.in_(existing_ids)).delete(synchronize_session=False)
                print(f"Deleted {len(existing_ids)} row(s) from videos for youtube id {youtube_id}")
            else:
                print(f"No existing rows in videos for youtube id {youtube_id}")

        db.commit()
        print(f"Blacklisted {youtube_id}" + (f" -- {reason}" if reason else ""))
    finally:
        db.close()


def remove_from_blacklist(youtube_id: str) -> None:
    db = SessionLocal()
    try:
        row = db.get(BlacklistedVideoRow, youtube_id)
        if not row:
            print(f"{youtube_id} isn't blacklisted")
            return
        db.delete(row)
        db.commit()
        print(f"Removed {youtube_id} from the blacklist")
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", help="YouTube video id or URL")
    parser.add_argument("--reason", help="Why this video is blacklisted, stored alongside it")
    parser.add_argument("--keep", action="store_true", help="Blacklist without deleting existing rows for this video")
    parser.add_argument("--remove", action="store_true", help="Un-blacklist this video instead of adding it")
    args = parser.parse_args()

    yt_id = extract_youtube_id(args.video)
    if args.remove:
        remove_from_blacklist(yt_id)
    else:
        blacklist_video(yt_id, args.reason, delete_existing=not args.keep)

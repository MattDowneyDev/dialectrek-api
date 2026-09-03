"""Re-syncs title/channel/duration for videos whose YouTube metadata is stale.

YouTube's API Terms of Service cap how long data pulled from the Data API v3
can be cached before it must be refreshed -- 30 days. import_channel.py only
writes that data once, at import time, so this is the other half: it finds
every video last synced more than STALE_AFTER_DAYS ago, re-fetches it in
batches of 50 (same videos.list endpoint import_channel.py uses), and updates
the row. A video that no longer comes back from the API -- deleted or made
private -- gets marked unavailable instead, which hides it from list_videos
and get_video_or_404 in watch.py.

Meant to run on a schedule (see refresh_handler.py for the Lambda entry
point), but it's also fine to run by hand:

    venv/bin/python refresh_metadata.py
"""

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from import_channel import fetch_videos_raw, get_api_key, parse_iso8601_duration
from watch import SessionLocal, VideoRow

# Kept comfortably under YouTube's 30-day cache limit so a video is never
# served on data older than the terms allow, even if a run gets skipped.
STALE_AFTER_DAYS = 25


def refresh_stale_videos() -> dict:
    api_key = get_api_key()
    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_AFTER_DAYS)
        stale = (
            db.query(VideoRow)
            .filter((VideoRow.metadata_synced_at == None) | (VideoRow.metadata_synced_at < cutoff))  # noqa: E711
            .all()
        )
        if not stale:
            print("Nothing due for refresh.")
            return {"checked": 0, "updated": 0, "marked_unavailable": 0}

        # A youtube_id could in principle back more than one row (e.g. the
        # same video imported under two languages), so refresh by id once
        # and fan the result out to every row sharing it.
        rows_by_youtube_id: dict[str, list[VideoRow]] = defaultdict(list)
        for row in stale:
            rows_by_youtube_id[row.youtube_id].append(row)
        youtube_ids = list(rows_by_youtube_id)

        print(f"Refreshing {len(youtube_ids)} video(s) last synced more than {STALE_AFTER_DAYS} days ago...")

        now = datetime.now(timezone.utc)
        seen_ids = set()
        updated = 0
        for start in range(0, len(youtube_ids), 50):
            batch = youtube_ids[start : start + 50]
            for item in fetch_videos_raw(batch, api_key):
                seen_ids.add(item["id"])
                duration_seconds = parse_iso8601_duration(item["contentDetails"]["duration"])
                for row in rows_by_youtube_id[item["id"]]:
                    row.title = item["snippet"]["title"]
                    row.channel = item["snippet"]["channelTitle"]
                    if duration_seconds is not None:
                        row.duration_seconds = duration_seconds
                    row.is_available = True
                    row.metadata_synced_at = now
                    updated += 1

        missing_ids = [yid for yid in youtube_ids if yid not in seen_ids]
        for youtube_id in missing_ids:
            for row in rows_by_youtube_id[youtube_id]:
                row.is_available = False
                row.metadata_synced_at = now

        db.commit()
        print(f"Updated {updated} row(s); {len(missing_ids)} video(s) no longer available and hidden.")
        return {"checked": len(youtube_ids), "updated": updated, "marked_unavailable": len(missing_ids)}
    finally:
        db.close()


if __name__ == "__main__":
    refresh_stale_videos()

"""Bulk-imports every public video from a YouTube channel into watch.db.

Uses the official YouTube Data API v3 rather than scraping the channel
page -- same "use the approved API" principle as the embedded player in
the frontend. Needs a free API key:

    1. Go to https://console.cloud.google.com and create (or pick) a project.
    2. APIs & Services -> Library -> enable "YouTube Data API v3".
    3. APIs & Services -> Credentials -> Create Credentials -> API key.
    4. Put it in dialectrek-api/.env (gitignored, never commit it) as:
       YOUTUBE_API_KEY=your-key-here

The free tier's daily quota (10,000 units) covers this easily -- listing a
channel's uploads and fetching video details costs about 1 unit per 50
videos, so even a channel with a thousand videos is ~40 units.

Every imported video starts at the same neutral difficulty rating and zero
likes. There's no reasonable way to eyeball difficulty across an entire
channel's back catalog by hand -- the Elo comparisons in watch.py are what
actually rank these as real votes come in.

Usage:
    venv/bin/python import_channel.py --channel @luisitocomunica --language es
    venv/bin/python import_channel.py --channel UCxxxxxxxxxxxxxxxxxxxxxx --language es
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from watch import Base, DEFAULT_RATING, SessionLocal, VideoRow, engine

load_dotenv()

API_BASE = "https://www.googleapis.com/youtube/v3"


def get_api_key() -> str:
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit(
            "Set YOUTUBE_API_KEY in dialectrek-api/.env first -- see the "
            "module docstring at the top of import_channel.py for how to get one."
        )
    return key


def resolve_uploads_playlist(channel: str, api_key: str) -> tuple[str, str]:
    """Returns (uploads_playlist_id, channel_title) for a handle like '@luisitocomunica' or a raw UC... channel id."""
    params = {"part": "snippet,contentDetails", "key": api_key}
    if channel.startswith("UC"):
        params["id"] = channel
    else:
        params["forHandle"] = channel.lstrip("@")

    response = requests.get(f"{API_BASE}/channels", params=params, timeout=10)
    response.raise_for_status()
    items = response.json().get("items", [])
    if not items:
        sys.exit(f"No channel found for '{channel}'")

    channel_data = items[0]
    return channel_data["contentDetails"]["relatedPlaylists"]["uploads"], channel_data["snippet"]["title"]


def fetch_playlist_video_ids(playlist_id: str, api_key: str) -> list[str]:
    video_ids = []
    page_token = None
    while True:
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(f"{API_BASE}/playlistItems", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        video_ids.extend(item["contentDetails"]["videoId"] for item in data["items"])

        page_token = data.get("nextPageToken")
        if not page_token:
            return video_ids


def parse_iso8601_duration(duration: str) -> int | None:
    """Converts YouTube's ISO 8601 duration (e.g. "PT15M33S") to whole seconds.

    Premieres and live streams report "P0D" (a days-only duration with no
    clock component) instead of a real PT##H##M##S length -- returns None
    for those and any other shape this doesn't recognize, so the caller can
    skip the video instead of crashing the whole import over one row.
    """
    match = re.fullmatch(r"P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?", duration)
    if not match:
        return None
    days, hours, minutes, seconds = (int(group) if group else 0 for group in match.groups())
    total = days * 86400 + hours * 3600 + minutes * 60 + seconds
    # A real video always has a nonzero length -- 0 only shows up for the
    # "P0D" placeholder YouTube reports for premieres/live streams that
    # haven't aired yet, so treat it the same as an unparseable duration.
    return total or None


def fetch_videos_raw(video_ids: list[str], api_key: str) -> list[dict]:
    """The videos.list endpoint takes at most 50 ids per call, so this batches them.

    Returns the raw API items (snippet + contentDetails) keyed by video id.
    Ids that no longer resolve -- deleted or made private -- are simply
    absent from the response, which callers use to detect that.
    """
    items = []
    for start in range(0, len(video_ids), 50):
        batch = video_ids[start : start + 50]
        response = requests.get(
            f"{API_BASE}/videos",
            params={"part": "snippet,contentDetails", "id": ",".join(batch), "key": api_key},
            timeout=10,
        )
        response.raise_for_status()
        items.extend(response.json()["items"])
    return items


def fetch_video_details(video_ids: list[str], api_key: str) -> list[dict]:
    details = []
    for item in fetch_videos_raw(video_ids, api_key):
        duration_seconds = parse_iso8601_duration(item["contentDetails"]["duration"])
        if duration_seconds is None:
            print(f"Skipping '{item['snippet']['title']}' -- no fixed duration (likely a premiere/live stream)")
            continue
        details.append(
            {
                "id": item["id"],
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "duration_seconds": duration_seconds,
            }
        )
    return details


def import_channel(channel: str, language: str):
    api_key = get_api_key()

    uploads_playlist_id, channel_title = resolve_uploads_playlist(channel, api_key)
    print(f"Found channel '{channel_title}', listing uploads...")

    video_ids = fetch_playlist_video_ids(uploads_playlist_id, api_key)
    print(f"Found {len(video_ids)} videos, fetching details...")

    videos = fetch_video_details(video_ids, api_key)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        for video in videos:
            # Keyed by youtube id so re-running an import (or importing a
            # channel that overlaps with a previous one) updates the same
            # row instead of creating a duplicate.
            db.merge(
                VideoRow(
                    id=f"{language}-{video['id']}",
                    language=language,
                    youtube_id=video["id"],
                    title=video["title"],
                    channel=video["channel"],
                    duration_seconds=video["duration_seconds"],
                    difficulty_score=DEFAULT_RATING,
                    like_count=0,
                    is_available=True,
                    metadata_synced_at=now,
                )
            )
        db.commit()
        print(f"Imported {len(videos)} videos from '{channel_title}' into watch.db")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", required=True, help="Channel handle (e.g. @luisitocomunica) or UC... channel id")
    parser.add_argument("--language", required=True, help="Language code to tag these videos with, e.g. es")
    args = parser.parse_args()
    import_channel(args.channel, args.language)

import pytest

import import_channel
import watch


class TestImportChannelReimport:
    """import_channel() upserts by youtube id, so re-running it against a
    channel that's already been imported must not clobber real Glicko
    ratings that accumulated from actual viewer votes in the meantime."""

    def _run_import(self, monkeypatch, rating=None):
        monkeypatch.setattr(import_channel, "get_api_key", lambda: "fake-key")
        monkeypatch.setattr(
            import_channel, "resolve_uploads_playlist", lambda channel, api_key: ("playlist-1", "Channel Title")
        )
        monkeypatch.setattr(import_channel, "fetch_playlist_video_ids", lambda playlist_id, api_key: ["vid1"])
        monkeypatch.setattr(
            import_channel,
            "fetch_video_details",
            lambda video_ids, api_key, blacklisted_ids: [
                {"id": "vid1", "title": "Video One", "channel": "Channel Title", "duration_seconds": 120}
            ],
        )
        kwargs = {"rating": rating} if rating is not None else {}
        import_channel.import_channel("@handle", "es", **kwargs)

    def test_preserves_rating_for_a_video_that_has_real_votes(self, monkeypatch, make_video):
        make_video(id="es-vid1", youtube_id="vid1", language="es", difficulty_score=1234.0, rating_deviation=55.0)

        self._run_import(monkeypatch)

        row = watch.SessionLocal().get(watch.VideoRow, "es-vid1")
        assert row.difficulty_score == pytest.approx(1234.0)
        assert row.rating_deviation == pytest.approx(55.0)

    def test_preserves_rating_across_a_flat_rating_reimport(self, monkeypatch, make_video):
        make_video(id="es-vid1", youtube_id="vid1", language="es", difficulty_score=1234.0, rating_deviation=55.0)

        self._run_import(monkeypatch, rating=650.0)

        row = watch.SessionLocal().get(watch.VideoRow, "es-vid1")
        assert row.difficulty_score == pytest.approx(1234.0)

    def test_applies_flat_rating_for_a_video_never_voted_on(self, monkeypatch, make_video):
        make_video(
            id="es-vid1",
            youtube_id="vid1",
            language="es",
            difficulty_score=watch.DEFAULT_RATING,
            rating_deviation=watch.DEFAULT_RD,
        )

        self._run_import(monkeypatch, rating=650.0)

        row = watch.SessionLocal().get(watch.VideoRow, "es-vid1")
        assert row.difficulty_score == pytest.approx(650.0)

    def test_new_video_defaults_to_default_rating_without_a_rating_flag(self, monkeypatch):
        self._run_import(monkeypatch)

        row = watch.SessionLocal().get(watch.VideoRow, "es-vid1")
        assert row.difficulty_score == pytest.approx(watch.DEFAULT_RATING)

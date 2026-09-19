import pytest

import watch


@pytest.mark.parametrize(
    "score,expected_level",
    [
        (699, "a1"),
        (700, "a2"),
        (849, "a2"),
        (850, "b1"),
        (999, "b1"),
        (1000, "b2"),
        (1149, "b2"),
        (1150, "c1"),
        (1299, "c1"),
        (1300, "c2"),
        (2000, "c2"),
    ],
)
def test_level_for_score_boundaries(score, expected_level):
    assert watch.level_for_score(score) == expected_level


class TestListVideos:
    def test_lists_only_available_videos_for_the_language(self, client, make_video):
        make_video(id="es-1", language="es")
        make_video(id="fr-1", language="fr")
        make_video(id="es-unavailable", language="es", is_available=False)

        response = client.get("/es/videos")
        assert response.status_code == 200
        ids = [v["id"] for v in response.json()["items"]]
        assert ids == ["es-1"]

    def test_filters_by_level(self, client, make_video):
        make_video(id="easy", difficulty_score=500)  # a1
        make_video(id="hard", difficulty_score=1400)  # c2

        response = client.get("/es/videos", params={"level": "a1"})
        ids = [v["id"] for v in response.json()["items"]]
        assert ids == ["easy"]

    def test_sort_easiest_orders_ascending_by_difficulty(self, client, make_video):
        make_video(id="hard", difficulty_score=1200)
        make_video(id="easy", difficulty_score=600)

        response = client.get("/es/videos", params={"sort": "easiest"})
        ids = [v["id"] for v in response.json()["items"]]
        assert ids == ["easy", "hard"]

    def test_sort_hardest_orders_descending_by_difficulty(self, client, make_video):
        make_video(id="hard", difficulty_score=1200)
        make_video(id="easy", difficulty_score=600)

        response = client.get("/es/videos", params={"sort": "hardest"})
        ids = [v["id"] for v in response.json()["items"]]
        assert ids == ["hard", "easy"]

    def test_sort_most_liked_orders_descending_by_like_count(self, client, make_video):
        make_video(id="popular", like_count=10)
        make_video(id="unpopular", like_count=0)

        response = client.get("/es/videos", params={"sort": "most-liked"})
        ids = [v["id"] for v in response.json()["items"]]
        assert ids == ["popular", "unpopular"]

    def test_sort_random_with_same_seed_is_deterministic(self, client, make_video):
        for i in range(5):
            make_video(id=f"v{i}")

        first = client.get("/es/videos", params={"sort": "random", "seed": 42}).json()
        second = client.get("/es/videos", params={"sort": "random", "seed": 42}).json()
        assert [v["id"] for v in first["items"]] == [v["id"] for v in second["items"]]

    def test_pagination_has_more_flag(self, client, make_video):
        for i in range(5):
            make_video(id=f"v{i}")

        response = client.get("/es/videos", params={"limit": 2, "offset": 0})
        body = response.json()
        assert len(body["items"]) == 2
        assert body["has_more"] is True

        response = client.get("/es/videos", params={"limit": 2, "offset": 4})
        body = response.json()
        assert len(body["items"]) == 1
        assert body["has_more"] is False


class TestGetVideo:
    def test_returns_video_by_id(self, client, make_video):
        make_video(id="v1", title="Hello")
        response = client.get("/es/videos/v1")
        assert response.status_code == 200
        assert response.json()["title"] == "Hello"

    def test_missing_video_is_404(self, client):
        assert client.get("/es/videos/does-not-exist").status_code == 404

    def test_video_from_other_language_is_404(self, client, make_video):
        make_video(id="v1", language="fr")
        assert client.get("/es/videos/v1").status_code == 404

    def test_unavailable_video_is_404(self, client, make_video):
        make_video(id="v1", is_available=False)
        assert client.get("/es/videos/v1").status_code == 404


class TestToggleLike:
    def test_liking_increments_like_count(self, client, make_video):
        make_video(id="v1", like_count=0)
        response = client.post("/es/videos/v1/like", json={"session_id": "s1"})
        assert response.status_code == 200
        assert response.json()["like_count"] == 1

    def test_liking_twice_toggles_it_off(self, client, make_video):
        make_video(id="v1", like_count=0)
        client.post("/es/videos/v1/like", json={"session_id": "s1"})
        response = client.post("/es/videos/v1/like", json={"session_id": "s1"})
        assert response.json()["like_count"] == 0

    def test_liking_after_disliking_clears_the_dislike(self, client, make_video):
        make_video(id="v1", like_count=0)
        client.post("/es/videos/v1/dislike", json={"session_id": "s1"})  # like_count -1
        response = client.post("/es/videos/v1/like", json={"session_id": "s1"})
        # undoes the -1 dislike (back to 0), then applies +1 like
        assert response.json()["like_count"] == 1

    def test_missing_video_is_404(self, client):
        response = client.post("/es/videos/nope/like", json={"session_id": "s1"})
        assert response.status_code == 404


class TestToggleDislike:
    def test_disliking_decrements_like_count(self, client, make_video):
        make_video(id="v1", like_count=0)
        response = client.post("/es/videos/v1/dislike", json={"session_id": "s1"})
        assert response.json()["like_count"] == -1

    def test_disliking_twice_toggles_it_off(self, client, make_video):
        make_video(id="v1", like_count=0)
        client.post("/es/videos/v1/dislike", json={"session_id": "s1"})
        response = client.post("/es/videos/v1/dislike", json={"session_id": "s1"})
        assert response.json()["like_count"] == 0

    def test_disliking_after_liking_clears_the_like(self, client, make_video):
        make_video(id="v1", like_count=0)
        client.post("/es/videos/v1/like", json={"session_id": "s1"})  # like_count +1
        response = client.post("/es/videos/v1/dislike", json={"session_id": "s1"})
        # undoes the +1 like (back to 0), then applies -1 dislike
        assert response.json()["like_count"] == -1


class TestCompareVideos:
    def test_harder_video_rating_increases_and_easier_decreases(self, client, make_video):
        make_video(id="harder", difficulty_score=1000, rating_deviation=350)
        make_video(id="easier", difficulty_score=1000, rating_deviation=350)

        response = client.post(
            "/es/videos/harder/compare",
            json={"easier_video_id": "easier", "session_id": "s1"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["harder_video"]["difficulty_score"] > 1000
        assert body["easier_video"]["difficulty_score"] < 1000

    def test_repeat_vote_from_same_session_is_a_no_op(self, client, make_video):
        make_video(id="harder", difficulty_score=1000, rating_deviation=350)
        make_video(id="easier", difficulty_score=1000, rating_deviation=350)

        first = client.post(
            "/es/videos/harder/compare",
            json={"easier_video_id": "easier", "session_id": "s1"},
        ).json()
        second = client.post(
            "/es/videos/harder/compare",
            json={"easier_video_id": "easier", "session_id": "s1"},
        ).json()
        assert first == second

    def test_missing_harder_video_is_404(self, client, make_video):
        make_video(id="easier")
        response = client.post(
            "/es/videos/nope/compare", json={"easier_video_id": "easier", "session_id": "s1"}
        )
        assert response.status_code == 404

    def test_missing_easier_video_is_404(self, client, make_video):
        make_video(id="harder")
        response = client.post(
            "/es/videos/harder/compare", json={"easier_video_id": "nope", "session_id": "s1"}
        )
        assert response.status_code == 404

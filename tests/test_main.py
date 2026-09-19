import json

import main


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


SPANISH_VERBS = load_json("./languages/spanish/verbs.json")
FRENCH_VERBS = load_json("./languages/french/verbs.json")
SPANISH_WORDS = load_json("./languages/spanish/words.json")


def test_alphabetic_sort_key_folds_accents_to_base_letter():
    # plain code-point order would put "único" after "zapato"; folding
    # accents to their base letter fixes that
    words = ["zapato", "único", "andar"]
    assert sorted(words, key=main.alphabetic_sort_key) == ["andar", "único", "zapato"]


def test_alphabetic_sort_key_uses_original_as_tiebreaker():
    assert main.alphabetic_sort_key("a") < main.alphabetic_sort_key("á")


class TestGetAllVerbs:
    def test_returns_sorted_target_english_pairs(self, client):
        response = client.get("/es/get-all-verbs")
        assert response.status_code == 200
        pairs = response.json()
        assert len(pairs) == len(SPANISH_VERBS)
        targets = [pair[0] for pair in pairs]
        assert targets == sorted(targets, key=main.alphabetic_sort_key)

    def test_unsupported_language_is_404(self, client):
        response = client.get("/de/get-all-verbs")
        assert response.status_code == 404

    def test_language_without_verbs_file_is_404(self, client, monkeypatch):
        from languages.registry import LANGUAGES

        monkeypatch.setattr(LANGUAGES["es"], "verbs_file", None)
        response = client.get("/es/get-all-verbs")
        assert response.status_code == 404


class TestGetVerbConjugation:
    def test_known_regular_verb_present_indicative(self, client):
        response = client.get("/es/get-verb-conjugation", params={"verb": "hablar"})
        assert response.status_code == 200
        body = response.json()
        assert body["infinitive_target"] == "hablar"
        assert body["mood"] == "indicative"
        assert body["tense"] == "present"
        assert len(body["conjugations"]) == 6
        assert body["conjugations"][0]["form_target"] == "hablo"

    def test_unknown_verb_is_404(self, client):
        response = client.get("/es/get-verb-conjugation", params={"verb": "not-a-real-verb"})
        assert response.status_code == 404

    def test_imperative_tense_returns_affirmative_and_negative_shape(self, client):
        response = client.get(
            "/es/get-verb-conjugation", params={"verb": "hablar", "tense": "imperative"}
        )
        assert response.status_code == 200
        body = response.json()
        row = body["conjugations"][0]
        assert "form_target_affirmative" in row
        assert "form_target_negative" in row
        pronouns = [row["pronoun_target"] for row in body["conjugations"]]
        assert "yo" not in pronouns  # no "yo" command form

    def test_indicative_only_tense_rejects_subjunctive_with_422(self, client):
        response = client.get(
            "/es/get-verb-conjugation",
            params={"verb": "hablar", "mood": "subjunctive", "tense": "preterite"},
        )
        assert response.status_code == 422

    def test_french_verb_conjugation(self, client):
        response = client.get("/fr/get-verb-conjugation", params={"verb": "parler"})
        assert response.status_code == 200
        body = response.json()
        assert body["infinitive_target"] == "parler"

    def test_french_unsupported_tense_is_422(self, client):
        response = client.get(
            "/fr/get-verb-conjugation", params={"verb": "parler", "tense": "preterite"}
        )
        assert response.status_code == 422


class TestGetRandomVerbConjugation:
    def test_returns_single_row_list(self, client):
        response = client.get("/es/get-random-verb-conjugation", params={"use_irregular": True})
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1
        row = body[0]
        assert row["infinitive_target"] in {v["spanish"] for v in SPANISH_VERBS}

    def test_use_irregular_false_only_picks_regular_verbs(self, client):
        from conjugation import is_irregular

        for _ in range(15):
            response = client.get(
                "/es/get-random-verb-conjugation", params={"use_irregular": False}
            )
            assert response.status_code == 200
            verb = response.json()[0]["infinitive_target"]
            assert is_irregular(verb, "indicative", "present") is False

    def test_use_regional_variant_false_excludes_vosotros(self, client):
        for _ in range(15):
            response = client.get(
                "/es/get-random-verb-conjugation",
                params={"use_irregular": True, "use_regional_variant": False},
            )
            pronoun = response.json()[0]["pronoun_target"]
            assert pronoun != "vosotros"

    def test_imperative_tense_excludes_yo_pronoun(self, client):
        for _ in range(15):
            response = client.get(
                "/es/get-random-verb-conjugation",
                params={"use_irregular": True, "tense": "imperative"},
            )
            pronoun = response.json()[0]["pronoun_target"]
            assert pronoun != "yo"

    def test_unsupported_language_is_404(self, client):
        response = client.get("/de/get-random-verb-conjugation", params={"use_irregular": True})
        assert response.status_code == 404


class TestGetWordCategories:
    def test_returns_sorted_unique_categories(self, client):
        response = client.get("/es/get-word-categories")
        assert response.status_code == 200
        categories = response.json()
        expected = sorted({w["category"] for w in SPANISH_WORDS})
        assert categories == expected


class TestGetRandomWord:
    def test_returns_a_word_shape(self, client):
        response = client.get("/es/get-random-word")
        assert response.status_code == 200
        body = response.json()
        assert set(body.keys()) == {"rank", "word_target", "word_english", "category"}

    def test_filters_by_category(self, client):
        category = SPANISH_WORDS[0]["category"]
        for _ in range(10):
            response = client.get("/es/get-random-word", params={"category": category})
            assert response.status_code == 200
            assert response.json()["category"] == category

    def test_unknown_category_is_404(self, client):
        response = client.get("/es/get-random-word", params={"category": "not-a-real-category"})
        assert response.status_code == 404

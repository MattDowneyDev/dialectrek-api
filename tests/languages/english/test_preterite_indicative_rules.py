import pytest

from languages.english.preterite_indicative_rules import (
    BE_PAST_FORMS,
    IRREGULAR_PAST,
    conjugate_past,
    conjugate_past_word,
)


class TestConjugatePastWord:
    @pytest.mark.parametrize("verb,expected", list(IRREGULAR_PAST.items()))
    def test_irregular_past_dict(self, verb, expected):
        assert conjugate_past_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("like", "liked"),
            ("bake", "baked"),
            ("close", "closed"),
        ],
    )
    def test_silent_e_just_adds_d(self, verb, expected):
        assert conjugate_past_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("study", "studied"),
            ("carry", "carried"),
            ("try", "tried"),
        ],
    )
    def test_y_to_ied_after_consonant(self, verb, expected):
        assert conjugate_past_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("stay", "stayed"),
            ("play", "played"),
        ],
    )
    def test_y_after_vowel_just_adds_ed(self, verb, expected):
        assert conjugate_past_word(verb) == expected

    def test_default_adds_ed(self):
        assert conjugate_past_word("walk") == "walked"


class TestConjugatePast:
    @pytest.mark.parametrize("pronoun_index,expected", enumerate(BE_PAST_FORMS))
    def test_be_varies_by_every_person(self, pronoun_index, expected):
        assert conjugate_past("to be", pronoun_index) == expected

    def test_be_able_to_composes_rest(self):
        assert conjugate_past("to be able to", 5) == "were able to"
        assert conjugate_past("to be able to", 0) == "was able to"

    def test_be_born(self):
        assert conjugate_past("to be born", 0) == "was born"
        assert conjugate_past("to be born", 3) == "were born"

    def test_regular_verb(self):
        assert conjugate_past("to walk", 0) == "walked"

    def test_pronoun_index_irrelevant_for_non_be_verbs(self):
        for idx in range(6):
            assert conjugate_past("to walk", idx) == "walked"

    @pytest.mark.parametrize(
        "infinitive,expected",
        [
            ("to go out", "went out"),
            ("to look for", "looked for"),
            ("to ask for", "asked for"),
            ("to take out", "took out"),
            ("to turn out", "turned out"),
        ],
    )
    def test_phrasal_verb_only_conjugates_first_word(self, infinitive, expected):
        assert conjugate_past(infinitive, 0) == expected

    def test_multi_translation_takes_first_slash_option(self):
        assert conjugate_past("to get up/raise", 0) == "got up"

    @pytest.mark.parametrize(
        "infinitive,expected",
        [
            ("to have", "had"),
            ("to do", "did"),
            ("to put", "put"),
            ("to read", "read"),
            ("to stop", "stopped"),
            ("to occur", "occurred"),
            ("to permit", "permitted"),
        ],
    )
    def test_irregular_via_full_conjugate_past(self, infinitive, expected):
        assert conjugate_past(infinitive, 0) == expected

    def test_infinitive_without_to_prefix_still_works(self):
        assert conjugate_past("walk", 0) == "walked"

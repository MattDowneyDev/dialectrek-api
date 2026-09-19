import pytest

from languages.english.participle_rules import (
    BE_PAST_PARTICIPLE,
    IRREGULAR_PAST_PARTICIPLES,
    conjugate_past_participle_word,
)
from languages.english.preterite_indicative_rules import IRREGULAR_PAST, conjugate_past_word


def test_be_is_invariable():
    assert conjugate_past_participle_word("be") == BE_PAST_PARTICIPLE == "been"


@pytest.mark.parametrize("verb,expected", list(IRREGULAR_PAST_PARTICIPLES.items()))
def test_irregular_participle_dict(verb, expected):
    assert conjugate_past_participle_word(verb) == expected


@pytest.mark.parametrize(
    "verb,expected",
    [
        ("walk", "walked"),
        ("study", "studied"),
        ("bring", "brought"),
        ("find", "found"),
        ("have", "had"),
    ],
)
def test_regular_and_shared_irregular_forms_fall_through_to_past_tense(verb, expected):
    assert conjugate_past_participle_word(verb) == expected


@pytest.mark.parametrize(
    "verb",
    [v for v in IRREGULAR_PAST if v not in IRREGULAR_PAST_PARTICIPLES and v != "be"],
)
def test_every_irregular_past_verb_not_overridden_matches_simple_past(verb):
    assert conjugate_past_participle_word(verb) == conjugate_past_word(verb)

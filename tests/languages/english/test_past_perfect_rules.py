import pytest

from languages.english.participle_rules import IRREGULAR_PAST_PARTICIPLES
from languages.english.past_perfect_rules import conjugate_past_perfect


@pytest.mark.parametrize("pronoun_index", range(6))
def test_had_never_varies_by_person(pronoun_index):
    assert conjugate_past_perfect("to speak", pronoun_index) == "had spoken"


@pytest.mark.parametrize("verb,participle", list(IRREGULAR_PAST_PARTICIPLES.items()))
def test_irregular_participles(verb, participle):
    assert conjugate_past_perfect(f"to {verb}", 0) == f"had {participle}"


def test_regular_verb():
    assert conjugate_past_perfect("to walk", 0) == "had walked"


def test_be():
    assert conjugate_past_perfect("to be", 0) == "had been"


def test_be_born():
    assert conjugate_past_perfect("to be born", 0) == "had been born"


def test_be_able_to():
    assert conjugate_past_perfect("to be able to", 5) == "had been able to"


def test_have_as_the_verb_itself():
    assert conjugate_past_perfect("to have", 0) == "had had"


def test_phrasal_verb_only_first_word_conjugated():
    assert conjugate_past_perfect("to go out", 2) == "had gone out"


def test_multi_translation_takes_first_slash_option():
    assert conjugate_past_perfect("to get up/raise", 0) == "had gotten up"

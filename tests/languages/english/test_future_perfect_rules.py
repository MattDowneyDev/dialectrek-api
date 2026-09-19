import pytest

from languages.english.future_perfect_rules import conjugate_future_perfect
from languages.english.participle_rules import IRREGULAR_PAST_PARTICIPLES


@pytest.mark.parametrize("pronoun_index", range(6))
def test_will_have_never_varies_by_person(pronoun_index):
    assert conjugate_future_perfect("to speak", pronoun_index) == "will have spoken"


@pytest.mark.parametrize("verb,participle", list(IRREGULAR_PAST_PARTICIPLES.items()))
def test_irregular_participles(verb, participle):
    assert conjugate_future_perfect(f"to {verb}", 0) == f"will have {participle}"


def test_regular_verb():
    assert conjugate_future_perfect("to walk", 0) == "will have walked"


def test_be():
    assert conjugate_future_perfect("to be", 0) == "will have been"


def test_be_born():
    assert conjugate_future_perfect("to be born", 0) == "will have been born"


def test_be_able_to():
    assert conjugate_future_perfect("to be able to", 5) == "will have been able to"


def test_have_as_the_verb_itself():
    assert conjugate_future_perfect("to have", 0) == "will have had"


def test_phrasal_verb_only_first_word_conjugated():
    assert conjugate_future_perfect("to go out", 2) == "will have gone out"


def test_multi_translation_takes_first_slash_option():
    assert conjugate_future_perfect("to get up/raise", 0) == "will have gotten up"

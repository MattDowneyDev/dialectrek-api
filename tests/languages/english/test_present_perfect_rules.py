import pytest

from languages.english.participle_rules import IRREGULAR_PAST_PARTICIPLES
from languages.english.present_perfect_rules import HAVE_THIRD_PERSON, conjugate_present_perfect


def test_have_third_person_is_has():
    assert HAVE_THIRD_PERSON == "has"


@pytest.mark.parametrize("pronoun_index", [0, 1, 3, 4, 5])
def test_non_third_person_uses_have(pronoun_index):
    assert conjugate_present_perfect("to walk", pronoun_index) == "have walked"


def test_third_person_uses_has():
    assert conjugate_present_perfect("to speak", 2) == "has spoken"


@pytest.mark.parametrize("verb,participle", list(IRREGULAR_PAST_PARTICIPLES.items()))
def test_irregular_participles(verb, participle):
    assert conjugate_present_perfect(f"to {verb}", 0) == f"have {participle}"


def test_be_uses_been_with_no_special_case_needed():
    assert conjugate_present_perfect("to be", 0) == "have been"
    assert conjugate_present_perfect("to be", 2) == "has been"


def test_be_able_to():
    assert conjugate_present_perfect("to be able to", 5) == "have been able to"


def test_be_born():
    assert conjugate_present_perfect("to be born", 0) == "have been born"


def test_have_as_the_verb_itself():
    assert conjugate_present_perfect("to have", 0) == "have had"


def test_die_regular_silent_e():
    assert conjugate_present_perfect("to die", 0) == "have died"


@pytest.mark.parametrize(
    "infinitive,pronoun_index,expected",
    [
        ("to go out", 2, "has gone out"),
        ("to look for", 0, "have looked for"),
        ("to get up/raise", 0, "have gotten up"),
    ],
)
def test_phrasal_and_multi_translation(infinitive, pronoun_index, expected):
    assert conjugate_present_perfect(infinitive, pronoun_index) == expected

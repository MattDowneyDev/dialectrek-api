import pytest

from languages.english.gerund_rules import DOUBLED_CONSONANT_GERUNDS
from languages.english.imperfect_indicative_rules import conjugate_imperfect
from languages.english.preterite_indicative_rules import BE_PAST_FORMS


@pytest.mark.parametrize("pronoun_index,be_form", enumerate(BE_PAST_FORMS))
def test_be_matches_simple_past_be_forms_with_no_gerund(pronoun_index, be_form):
    assert conjugate_imperfect("to be", pronoun_index) == be_form


def test_be_able_to():
    assert conjugate_imperfect("to be able to", 5) == "were able to"
    assert conjugate_imperfect("to be able to", 0) == "was able to"


def test_be_born():
    assert conjugate_imperfect("to be born", 0) == "was born"


def test_regular_verb_takes_gerund():
    assert conjugate_imperfect("to walk", 0) == "was walking"


@pytest.mark.parametrize("pronoun_index,be_form", enumerate(BE_PAST_FORMS))
def test_non_be_verb_uses_matching_be_form(pronoun_index, be_form):
    assert conjugate_imperfect("to speak", pronoun_index) == f"{be_form} speaking"


@pytest.mark.parametrize("verb,gerund", list(DOUBLED_CONSONANT_GERUNDS.items()))
def test_doubled_consonant_gerunds(verb, gerund):
    assert conjugate_imperfect(f"to {verb}", 0) == f"was {gerund}"


def test_y_ending_verb_gerund():
    assert conjugate_imperfect("to study", 0) == "was studying"


def test_have_uses_gerund_not_had():
    assert conjugate_imperfect("to have", 0) == "was having"


def test_phrasal_verb_only_first_word_takes_gerund():
    assert conjugate_imperfect("to go out", 2) == "was going out"
    assert conjugate_imperfect("to look for", 0) == "was looking for"


def test_multi_translation_takes_first_slash_option():
    assert conjugate_imperfect("to get up/raise", 0) == "was getting up"

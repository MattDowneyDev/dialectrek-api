import pytest

from languages.english.imperative_rules import NOSOTROS_INDEX, conjugate_imperative


def test_nosotros_index_is_three():
    assert NOSOTROS_INDEX == 3


@pytest.mark.parametrize("pronoun_index", [0, 1, 2, 4, 5])
def test_affirmative_is_bare_verb_for_non_nosotros(pronoun_index):
    assert conjugate_imperative("to speak/talk", pronoun_index, "affirmative") == "speak"


@pytest.mark.parametrize("pronoun_index", [0, 1, 2, 4, 5])
def test_negative_uses_dont_for_non_nosotros(pronoun_index):
    assert conjugate_imperative("to speak/talk", pronoun_index, "negative") == "don't speak"


def test_nosotros_affirmative_uses_lets():
    assert conjugate_imperative("to speak/talk", 3, "affirmative") == "let's speak"


def test_nosotros_negative_uses_lets_not():
    assert conjugate_imperative("to speak/talk", 3, "negative") == "let's not speak"


def test_phrasal_verb_kept_whole():
    assert conjugate_imperative("to go out", 2, "affirmative") == "go out"
    assert conjugate_imperative("to go out", 5, "negative") == "don't go out"


def test_be_affirmative_and_negative():
    assert conjugate_imperative("to be", 1, "affirmative") == "be"
    assert conjugate_imperative("to be born", 1, "negative") == "don't be born"


def test_multi_translation_takes_first_slash_option():
    assert conjugate_imperative("to speak/talk", 1, "affirmative") == "speak"


def test_infinitive_without_to_prefix_still_works():
    assert conjugate_imperative("speak", 1, "affirmative") == "speak"

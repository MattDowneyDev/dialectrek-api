import pytest

from languages.english.conditional_rules import conjugate_conditional


@pytest.mark.parametrize("pronoun_index", range(6))
def test_would_never_varies_by_person(pronoun_index):
    assert conjugate_conditional("to eat", pronoun_index) == "would eat"


def test_phrasal_verb_kept_whole():
    assert conjugate_conditional("to go out", 2) == "would go out"


def test_be():
    assert conjugate_conditional("to be", 0) == "would be"


def test_be_able_to():
    assert conjugate_conditional("to be able to", 5) == "would be able to"


def test_multi_translation_takes_first_slash_option():
    assert conjugate_conditional("to get up/raise", 0) == "would get up"


def test_infinitive_without_to_prefix_still_works():
    assert conjugate_conditional("eat", 0) == "would eat"

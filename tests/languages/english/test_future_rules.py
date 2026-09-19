import pytest

from languages.english.future_rules import conjugate_future


@pytest.mark.parametrize("pronoun_index", range(6))
def test_will_never_varies_by_person(pronoun_index):
    assert conjugate_future("to eat", pronoun_index) == "will eat"


def test_phrasal_verb_kept_whole():
    assert conjugate_future("to go out", 2) == "will go out"


def test_be():
    assert conjugate_future("to be", 0) == "will be"


def test_be_able_to():
    assert conjugate_future("to be able to", 5) == "will be able to"


def test_multi_translation_takes_first_slash_option():
    assert conjugate_future("to get up/raise", 0) == "will get up"


def test_infinitive_without_to_prefix_still_works():
    assert conjugate_future("eat", 0) == "will eat"

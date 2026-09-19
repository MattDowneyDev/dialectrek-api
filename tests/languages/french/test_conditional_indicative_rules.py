import pytest

from languages.french.conditional_indicative_rules import (
    conjugate_conditional_indicative,
    is_irregular_conditional,
)
from languages.french.future_indicative_rules import IRREGULAR_FUTURE_STEMS, is_irregular_future


class TestRegularVerbs:
    def test_parler(self):
        expected = ["parlerais", "parlerais", "parlerait", "parlerions", "parleriez", "parleraient"]
        for pronoun_index, form in enumerate(expected):
            assert conjugate_conditional_indicative("parler", pronoun_index) == form

    def test_finir(self):
        assert conjugate_conditional_indicative("finir", 0) == "finirais"

    def test_attendre(self):
        assert conjugate_conditional_indicative("attendre", 0) == "attendrais"


class TestSharesFutureStem:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_FUTURE_STEMS))
    def test_every_irregular_future_stem_reused(self, verb):
        stem = IRREGULAR_FUTURE_STEMS[verb]
        assert conjugate_conditional_indicative(verb, 0) == stem + "ais"
        assert conjugate_conditional_indicative(verb, 3) == stem + "ions"

    def test_etre(self):
        assert conjugate_conditional_indicative("être", 0) == "serais"

    def test_avoir(self):
        assert conjugate_conditional_indicative("avoir", 0) == "aurais"

    def test_aller(self):
        assert conjugate_conditional_indicative("aller", 0) == "irais"

    def test_envoyer(self):
        assert conjugate_conditional_indicative("envoyer", 0) == "enverrais"

    def test_acheter_stem_change_carries_over(self):
        assert conjugate_conditional_indicative("acheter", 0) == "achèterais"


class TestReflexiveVerbs:
    def test_se_lever(self):
        assert conjugate_conditional_indicative("se lever", 0) == "me lèverais"
        assert conjugate_conditional_indicative("se lever", 3) == "nous lèverions"

    def test_s_habiller_elides_before_vowel_sound(self):
        assert conjugate_conditional_indicative("s'habiller", 0) == "m'habillerais"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_conditional_indicative("  Parler ", 0) == "parlerais"


def test_is_irregular_conditional_is_the_same_function_as_future():
    assert is_irregular_conditional is is_irregular_future


@pytest.mark.parametrize(
    "verb,expected",
    [("parler", False), ("être", True), ("acheter", True), ("essayer", True)],
)
def test_is_irregular_conditional_matches_future_classification(verb, expected):
    assert is_irregular_conditional(verb) is expected

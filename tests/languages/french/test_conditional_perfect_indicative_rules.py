import pytest

from languages.french.conditional_perfect_indicative_rules import (
    conjugate_conditional_perfect_indicative,
)
from languages.french.present_perfect_indicative_rules import ETRE_VERBS


class TestAvoirPath:
    def test_parler(self):
        assert conjugate_conditional_perfect_indicative("parler", 0) == "aurais parlé"
        assert conjugate_conditional_perfect_indicative("parler", 3) == "aurions parlé"


class TestEtrePath:
    @pytest.mark.parametrize("verb", sorted(ETRE_VERBS))
    def test_every_etre_verb_uses_conditional_of_etre(self, verb):
        assert conjugate_conditional_perfect_indicative(verb, 0).startswith("serais ")

    def test_aller(self):
        assert conjugate_conditional_perfect_indicative("aller", 0) == "serais allé"
        assert conjugate_conditional_perfect_indicative("aller", 3) == "serions allés"


class TestReflexiveVerbs:
    def test_se_lever_takes_etre(self):
        assert conjugate_conditional_perfect_indicative("se lever", 0) == "me serais levé"
        assert conjugate_conditional_perfect_indicative("se lever", 3) == "nous serions levés"

    def test_s_habiller_elision_depends_on_auxiliary(self):
        assert conjugate_conditional_perfect_indicative("s'habiller", 0) == "me serais habillé"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_conditional_perfect_indicative("  Parler ", 0) == "aurais parlé"

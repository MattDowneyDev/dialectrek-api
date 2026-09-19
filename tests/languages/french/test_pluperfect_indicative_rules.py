import pytest

from languages.french.pluperfect_indicative_rules import conjugate_pluperfect_indicative
from languages.french.present_perfect_indicative_rules import ETRE_VERBS


class TestAvoirPath:
    def test_parler(self):
        assert conjugate_pluperfect_indicative("parler", 0) == "avais parlé"
        assert conjugate_pluperfect_indicative("parler", 3) == "avions parlé"


class TestEtrePath:
    @pytest.mark.parametrize("verb", sorted(ETRE_VERBS))
    def test_every_etre_verb_uses_imperfect_of_etre(self, verb):
        assert conjugate_pluperfect_indicative(verb, 0).startswith("étais ")

    def test_aller(self):
        assert conjugate_pluperfect_indicative("aller", 0) == "étais allé"
        assert conjugate_pluperfect_indicative("aller", 3) == "étions allés"


class TestReflexiveVerbs:
    def test_se_lever_takes_etre(self):
        assert conjugate_pluperfect_indicative("se lever", 0) == "m'étais levé"
        assert conjugate_pluperfect_indicative("se lever", 3) == "nous étions levés"

    def test_s_habiller_elides_before_auxiliary_starting_with_vowel(self):
        assert conjugate_pluperfect_indicative("s'habiller", 0) == "m'étais habillé"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_pluperfect_indicative("  Parler ", 0) == "avais parlé"

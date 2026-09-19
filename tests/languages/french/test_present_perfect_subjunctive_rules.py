import pytest

from languages.french.present_perfect_subjunctive_rules import conjugate_present_perfect_subjunctive
from languages.french.present_perfect_indicative_rules import ETRE_VERBS


class TestAvoirPath:
    def test_parler(self):
        assert conjugate_present_perfect_subjunctive("parler", 0) == "aie parlé"
        assert conjugate_present_perfect_subjunctive("parler", 2) == "ait parlé"

    def test_participle_never_agrees_with_avoir(self):
        assert conjugate_present_perfect_subjunctive("parler", 3) == "ayons parlé"


class TestEtrePath:
    @pytest.mark.parametrize("verb", sorted(ETRE_VERBS))
    def test_every_etre_verb_uses_subjunctive_of_etre(self, verb):
        assert conjugate_present_perfect_subjunctive(verb, 0).startswith("sois ")

    def test_aller(self):
        assert conjugate_present_perfect_subjunctive("aller", 0) == "sois allé"
        assert conjugate_present_perfect_subjunctive("aller", 3) == "soyons allés"


class TestReflexiveVerbs:
    def test_se_lever_takes_etre(self):
        assert conjugate_present_perfect_subjunctive("se lever", 0) == "me sois levé"
        assert conjugate_present_perfect_subjunctive("se lever", 3) == "nous soyons levés"

    def test_s_habiller_elision_depends_on_auxiliary(self):
        assert conjugate_present_perfect_subjunctive("s'habiller", 0) == "me sois habillé"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_present_perfect_subjunctive("  Parler ", 0) == "aie parlé"

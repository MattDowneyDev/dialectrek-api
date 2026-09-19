import pytest

from languages.french.future_perfect_indicative_rules import conjugate_future_perfect_indicative
from languages.french.present_perfect_indicative_rules import ETRE_VERBS


class TestAvoirPath:
    def test_parler(self):
        assert conjugate_future_perfect_indicative("parler", 0) == "aurai parlé"
        assert conjugate_future_perfect_indicative("parler", 3) == "aurons parlé"

    def test_participle_never_agrees_with_avoir(self):
        assert conjugate_future_perfect_indicative("parler", 5) == "auront parlé"


class TestEtrePath:
    @pytest.mark.parametrize("verb", sorted(ETRE_VERBS))
    def test_every_etre_verb_uses_future_of_etre(self, verb):
        assert conjugate_future_perfect_indicative(verb, 0).startswith("serai ")

    def test_aller(self):
        assert conjugate_future_perfect_indicative("aller", 0) == "serai allé"
        assert conjugate_future_perfect_indicative("aller", 3) == "serons allés"


class TestReflexiveVerbs:
    def test_se_lever_takes_etre(self):
        assert conjugate_future_perfect_indicative("se lever", 0) == "me serai levé"
        assert conjugate_future_perfect_indicative("se lever", 3) == "nous serons levés"

    def test_s_habiller_elision_depends_on_auxiliary(self):
        assert conjugate_future_perfect_indicative("s'habiller", 0) == "me serai habillé"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_future_perfect_indicative("  Parler ", 0) == "aurai parlé"

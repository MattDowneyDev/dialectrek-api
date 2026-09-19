import pytest

from languages.french.future_indicative_rules import (
    IRREGULAR_FUTURE_STEMS,
    conjugate_future_indicative,
    future_stem,
    is_irregular_future,
)
from languages.french.present_indicative_rules import DOUBLING_VERBS, E_STEM_CHANGE_VERBS


class TestRegularVerbs:
    def test_er_verb(self):
        expected = ["parlerai", "parleras", "parlera", "parlerons", "parlerez", "parleront"]
        for pronoun_index, form in enumerate(expected):
            assert conjugate_future_indicative("parler", pronoun_index) == form

    def test_ir_verb_stem_is_the_bare_infinitive(self):
        assert future_stem("finir") == "finir"
        assert conjugate_future_indicative("finir", 0) == "finirai"

    def test_re_verb_drops_final_e(self):
        assert future_stem("attendre") == "attendr"
        assert conjugate_future_indicative("attendre", 0) == "attendrai"

    def test_re_verb_holds_even_for_present_tense_irregulars(self):
        assert conjugate_future_indicative("mettre", 0) == "mettrai"
        assert conjugate_future_indicative("prendre", 0) == "prendrai"
        assert conjugate_future_indicative("connaître", 0) == "connaîtrai"

    def test_dormir_type_verb_is_regular_in_future(self):
        assert conjugate_future_indicative("dormir", 0) == "dormirai"

    def test_invalid_infinitive_ending_raises(self):
        with pytest.raises(ValueError):
            future_stem("parl")


class TestIrregularFutureStems:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_FUTURE_STEMS))
    def test_every_irregular_stem_used(self, verb):
        stem = IRREGULAR_FUTURE_STEMS[verb]
        assert future_stem(verb) == stem
        assert conjugate_future_indicative(verb, 0) == stem + "ai"
        assert conjugate_future_indicative(verb, 3) == stem + "ons"

    def test_etre(self):
        assert conjugate_future_indicative("être", 0) == "serai"

    def test_avoir(self):
        assert conjugate_future_indicative("avoir", 0) == "aurai"

    def test_aller(self):
        assert conjugate_future_indicative("aller", 0) == "irai"

    def test_envoyer_is_irregular_unlike_present(self):
        assert conjugate_future_indicative("envoyer", 0) == "enverrai"


class TestErStemChangesCarryToEveryPerson:
    @pytest.mark.parametrize("verb", sorted(DOUBLING_VERBS))
    def test_doubling_verbs(self, verb):
        stem = verb[:-2]
        doubled = stem + stem[-1]
        assert future_stem(verb) == doubled + "er"

    def test_appeler(self):
        assert conjugate_future_indicative("appeler", 3) == "appellerons"

    @pytest.mark.parametrize("verb", sorted(E_STEM_CHANGE_VERBS))
    def test_e_stem_change_verbs(self, verb):
        form = conjugate_future_indicative(verb, 3)
        assert "è" in form

    def test_acheter(self):
        assert conjugate_future_indicative("acheter", 0) == "achèterai"
        assert conjugate_future_indicative("acheter", 3) == "achèterons"

    def test_y_stem_verb_changes_to_i_everywhere(self):
        assert conjugate_future_indicative("essayer", 0) == "essaierai"
        assert conjugate_future_indicative("essayer", 3) == "essaierons"

    def test_preferer_keeps_e_acute_in_future(self):
        # E_ACUTE_STEM_CHANGE_VERBS aren't in future_stem's special-cased
        # sets -- tradition keeps the "é" here, unlike the present tense
        assert future_stem("préférer") == "préférer"
        assert conjugate_future_indicative("préférer", 0) == "préférerai"


class TestReflexiveVerbs:
    def test_se_lever(self):
        assert conjugate_future_indicative("se lever", 0) == "me lèverai"
        assert conjugate_future_indicative("se lever", 3) == "nous lèverons"

    def test_s_habiller_elides_before_vowel_sound(self):
        assert conjugate_future_indicative("s'habiller", 0) == "m'habillerai"
        assert conjugate_future_indicative("s'habiller", 2) == "s'habillera"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_future_indicative("  Parler ", 0) == "parlerai"


class TestIsIrregularFuture:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_FUTURE_STEMS))
    def test_irregular_stem_verbs_flagged(self, verb):
        assert is_irregular_future(verb) is True

    @pytest.mark.parametrize("verb", sorted(DOUBLING_VERBS))
    def test_doubling_verbs_flagged(self, verb):
        assert is_irregular_future(verb) is True

    @pytest.mark.parametrize("verb", sorted(E_STEM_CHANGE_VERBS))
    def test_e_stem_change_verbs_flagged(self, verb):
        assert is_irregular_future(verb) is True

    def test_y_stem_verb_flagged(self):
        assert is_irregular_future("essayer") is True

    def test_e_acute_stem_change_verbs_not_flagged(self):
        # their future stem doesn't actually deviate from the regular rule
        assert is_irregular_future("préférer") is False

    @pytest.mark.parametrize("verb", ["parler", "finir", "attendre", "dormir"])
    def test_regular_verbs_not_flagged(self, verb):
        assert is_irregular_future(verb) is False

    def test_reflexive_irregularity_checks_base_verb(self):
        assert is_irregular_future("se lever") is True
        assert is_irregular_future("se reposer") is False

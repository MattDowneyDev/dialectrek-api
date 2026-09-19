import pytest

from languages.french.imperfect_indicative_rules import (
    conjugate_imperfect_indicative,
    imperfect_stem,
    is_irregular_imperfect,
)
from languages.french.present_indicative_rules import DORMIR_TYPE_VERBS, IRREGULAR_VERBS


class TestRegularVerbs:
    def test_parler(self):
        expected = ["parlais", "parlais", "parlait", "parlions", "parliez", "parlaient"]
        for pronoun_index, form in enumerate(expected):
            assert conjugate_imperfect_indicative("parler", pronoun_index) == form

    def test_finir(self):
        assert conjugate_imperfect_indicative("finir", 0) == "finissais"
        assert conjugate_imperfect_indicative("finir", 3) == "finissions"

    def test_attendre(self):
        assert conjugate_imperfect_indicative("attendre", 0) == "attendais"


class TestStemDerivedFromPresentNousForm:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_VERBS))
    def test_stem_matches_present_nous_form_minus_ons(self, verb):
        from languages.french.present_indicative_rules import conjugate_present_indicative

        nous_form = conjugate_present_indicative(verb, 3)
        if not nous_form.endswith("ons"):
            pytest.skip(f"{verb}'s nous form doesn't end in -ons")
        assert imperfect_stem(verb) == nous_form[:-3]

    def test_avoir(self):
        assert conjugate_imperfect_indicative("avoir", 0) == "avais"

    def test_faire(self):
        assert conjugate_imperfect_indicative("faire", 0) == "faisais"

    def test_aller(self):
        assert conjugate_imperfect_indicative("aller", 0) == "allais"

    def test_boire_uses_plural_present_stem(self):
        assert conjugate_imperfect_indicative("boire", 0) == "buvais"
        assert conjugate_imperfect_indicative("boire", 3) == "buvions"

    @pytest.mark.parametrize("verb", sorted(DORMIR_TYPE_VERBS))
    def test_dormir_type_verbs(self, verb):
        stem = verb[:-2]
        assert conjugate_imperfect_indicative(verb, 0) == stem + "ais"


class TestEtreIsMemorized:
    def test_etre_stem_is_et(self):
        assert imperfect_stem("être") == "ét"
        assert conjugate_imperfect_indicative("être", 0) == "étais"
        assert conjugate_imperfect_indicative("être", 3) == "étions"


class TestCerGerSpellingChanges:
    def test_cer_verb_takes_cedilla_outside_nous_vous(self):
        assert conjugate_imperfect_indicative("commencer", 0) == "commençais"
        assert conjugate_imperfect_indicative("commencer", 3) == "commencions"

    def test_ger_verb_keeps_soft_e_outside_nous_vous(self):
        assert conjugate_imperfect_indicative("manger", 0) == "mangeais"
        assert conjugate_imperfect_indicative("manger", 3) == "mangions"


class TestReflexiveVerbs:
    def test_se_lever_no_present_tense_stem_change_carries_over(self):
        # imperfect always builds on the plural stem, so acheter/lever-type
        # e->è changes never show up here even though they do in the present
        assert conjugate_imperfect_indicative("se lever", 0) == "me levais"
        assert conjugate_imperfect_indicative("se lever", 3) == "nous levions"

    def test_s_habiller_elides_before_vowel_sound(self):
        assert conjugate_imperfect_indicative("s'habiller", 0) == "m'habillais"
        assert conjugate_imperfect_indicative("s'habiller", 2) == "s'habillait"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_imperfect_indicative("  Parler ", 0) == "parlais"


class TestIsIrregularImperfect:
    def test_etre_is_the_only_irregular_verb(self):
        assert is_irregular_imperfect("être") is True

    @pytest.mark.parametrize("verb", ["avoir", "aller", "faire", "boire", "parler", "dormir"])
    def test_everything_else_is_regular(self, verb):
        assert is_irregular_imperfect(verb) is False

    def test_reflexive_irregularity_checks_base_verb(self):
        assert is_irregular_imperfect("se lever") is False

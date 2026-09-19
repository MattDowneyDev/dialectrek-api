import pytest

from languages.french.present_indicative_rules import (
    DORMIR_TYPE_VERBS,
    DOUBLING_VERBS,
    E_ACUTE_STEM_CHANGE_VERBS,
    E_STEM_CHANGE_VERBS,
    IRREGULAR_VERBS,
    conjugate_present_indicative,
    is_irregular_present,
)

REGULAR_ER = {
    "parler": ["parle", "parles", "parle", "parlons", "parlez", "parlent"],
}
REGULAR_IR = {
    "finir": ["finis", "finis", "finit", "finissons", "finissez", "finissent"],
}
REGULAR_RE = {
    "attendre": ["attends", "attends", "attend", "attendons", "attendez", "attendent"],
}


class TestRegularVerbs:
    @pytest.mark.parametrize("verb,forms", list(REGULAR_ER.items()) + list(REGULAR_IR.items()) + list(REGULAR_RE.items()))
    def test_all_six_forms(self, verb, forms):
        for pronoun_index, expected in enumerate(forms):
            assert conjugate_present_indicative(verb, pronoun_index) == expected

    def test_invalid_infinitive_ending_raises(self):
        with pytest.raises(ValueError):
            conjugate_present_indicative("parl", 0)


class TestIrregularVerbs:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_VERBS))
    def test_every_irregular_verb_matches_its_own_table(self, verb):
        for pronoun_index, expected in enumerate(IRREGULAR_VERBS[verb]):
            assert conjugate_present_indicative(verb, pronoun_index) == expected

    def test_etre(self):
        assert conjugate_present_indicative("être", 0) == "suis"
        assert conjugate_present_indicative("être", 3) == "sommes"
        assert conjugate_present_indicative("être", 5) == "sont"

    def test_avoir(self):
        assert conjugate_present_indicative("avoir", 0) == "ai"
        assert conjugate_present_indicative("avoir", 5) == "ont"

    def test_aller(self):
        assert conjugate_present_indicative("aller", 0) == "vais"
        assert conjugate_present_indicative("aller", 1) == "vas"
        assert conjugate_present_indicative("aller", 3) == "allons"

    def test_faire(self):
        assert conjugate_present_indicative("faire", 3) == "faisons"
        assert conjugate_present_indicative("faire", 5) == "font"

    def test_dire_vs_interdire_vous_form_differs(self):
        assert conjugate_present_indicative("dire", 4) == "dites"
        assert conjugate_present_indicative("interdire", 4) == "interdisez"

    def test_boire_stem_alternation(self):
        assert conjugate_present_indicative("boire", 0) == "bois"
        assert conjugate_present_indicative("boire", 3) == "buvons"
        assert conjugate_present_indicative("boire", 5) == "boivent"


class TestDormirTypeVerbs:
    @pytest.mark.parametrize("verb", sorted(DORMIR_TYPE_VERBS))
    def test_singular_drops_final_consonant(self, verb):
        stem = verb[:-3]
        assert conjugate_present_indicative(verb, 0) == stem + "s"
        assert conjugate_present_indicative(verb, 1) == stem + "s"
        assert conjugate_present_indicative(verb, 2) == stem + "t"

    @pytest.mark.parametrize("verb", sorted(DORMIR_TYPE_VERBS))
    def test_plural_is_regular(self, verb):
        stem = verb[:-2]
        assert conjugate_present_indicative(verb, 3) == stem + "ons"
        assert conjugate_present_indicative(verb, 4) == stem + "ez"
        assert conjugate_present_indicative(verb, 5) == stem + "ent"

    def test_dormir_known_forms(self):
        assert conjugate_present_indicative("dormir", 0) == "dors"
        assert conjugate_present_indicative("dormir", 2) == "dort"
        assert conjugate_present_indicative("dormir", 3) == "dormons"

    def test_partir_known_forms(self):
        assert conjugate_present_indicative("partir", 0) == "pars"
        assert conjugate_present_indicative("partir", 3) == "partons"


class TestEStemChangeVerbs:
    @pytest.mark.parametrize("verb", sorted(E_STEM_CHANGE_VERBS))
    def test_e_becomes_e_grave_outside_nous_vous(self, verb):
        form = conjugate_present_indicative(verb, 0)
        assert "è" in form
        # nous/vous keep the plain "e"
        nous_form = conjugate_present_indicative(verb, 3)
        assert "è" not in nous_form

    def test_acheter(self):
        assert conjugate_present_indicative("acheter", 0) == "achète"
        assert conjugate_present_indicative("acheter", 3) == "achetons"

    def test_lever(self):
        assert conjugate_present_indicative("lever", 0) == "lève"
        assert conjugate_present_indicative("lever", 5) == "lèvent"

    def test_peser(self):
        assert conjugate_present_indicative("peser", 0) == "pèse"

    def test_promener(self):
        assert conjugate_present_indicative("promener", 0) == "promène"
        assert conjugate_present_indicative("promener", 3) == "promenons"


class TestEAcuteStemChangeVerbs:
    @pytest.mark.parametrize("verb", sorted(E_ACUTE_STEM_CHANGE_VERBS))
    def test_e_acute_becomes_e_grave_outside_nous_vous(self, verb):
        form = conjugate_present_indicative(verb, 0)
        assert "è" in form
        nous_form = conjugate_present_indicative(verb, 3)
        assert "é" in nous_form

    def test_preferer(self):
        assert conjugate_present_indicative("préférer", 0) == "préfère"
        assert conjugate_present_indicative("préférer", 3) == "préférons"

    def test_proteger_nous_form_keeps_soft_g(self):
        assert conjugate_present_indicative("protéger", 0) == "protège"
        assert conjugate_present_indicative("protéger", 3) == "protégeons"


class TestDoublingVerbs:
    def test_appeler(self):
        assert conjugate_present_indicative("appeler", 0) == "appelle"
        assert conjugate_present_indicative("appeler", 3) == "appelons"

    def test_rappeler(self):
        assert conjugate_present_indicative("rappeler", 5) == "rappellent"


class TestCerGerSpellingChanges:
    def test_cer_verb_takes_cedilla_in_nous_form(self):
        assert conjugate_present_indicative("commencer", 3) == "commençons"
        assert conjugate_present_indicative("commencer", 0) == "commence"

    def test_ger_verb_keeps_soft_e_in_nous_form(self):
        assert conjugate_present_indicative("manger", 3) == "mangeons"
        assert conjugate_present_indicative("manger", 0) == "mange"


class TestYStemVerbs:
    def test_y_becomes_i_outside_nous_vous(self):
        assert conjugate_present_indicative("essayer", 0) == "essaie"
        assert conjugate_present_indicative("essayer", 3) == "essayons"
        assert conjugate_present_indicative("essayer", 4) == "essayez"


class TestReflexiveVerbs:
    def test_se_lever_elision_by_pronoun(self):
        assert conjugate_present_indicative("se lever", 0) == "me lève"
        assert conjugate_present_indicative("se lever", 1) == "te lèves"
        assert conjugate_present_indicative("se lever", 2) == "se lève"
        assert conjugate_present_indicative("se lever", 3) == "nous levons"
        assert conjugate_present_indicative("se lever", 4) == "vous levez"
        assert conjugate_present_indicative("se lever", 5) == "se lèvent"

    def test_s_habiller_elides_before_vowel_sound(self):
        assert conjugate_present_indicative("s'habiller", 0) == "m'habille"
        assert conjugate_present_indicative("s'habiller", 1) == "t'habilles"
        assert conjugate_present_indicative("s'habiller", 2) == "s'habille"
        assert conjugate_present_indicative("s'habiller", 5) == "s'habillent"

    def test_se_reposer_regular_verb(self):
        assert conjugate_present_indicative("se reposer", 3) == "nous reposons"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_present_indicative("  Parler  ", 0) == "parle"


class TestIsIrregularPresent:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_VERBS))
    def test_irregular_verbs_flagged(self, verb):
        assert is_irregular_present(verb) is True

    @pytest.mark.parametrize("verb", sorted(DORMIR_TYPE_VERBS))
    def test_dormir_type_flagged(self, verb):
        assert is_irregular_present(verb) is True

    @pytest.mark.parametrize("verb", sorted(E_STEM_CHANGE_VERBS))
    def test_e_stem_change_flagged(self, verb):
        assert is_irregular_present(verb) is True

    @pytest.mark.parametrize("verb", sorted(E_ACUTE_STEM_CHANGE_VERBS))
    def test_e_acute_stem_change_flagged(self, verb):
        assert is_irregular_present(verb) is True

    @pytest.mark.parametrize("verb", sorted(DOUBLING_VERBS))
    def test_doubling_verbs_flagged(self, verb):
        assert is_irregular_present(verb) is True

    def test_y_stem_verb_flagged(self):
        assert is_irregular_present("essayer") is True
        assert is_irregular_present("envoyer") is True

    @pytest.mark.parametrize("verb", ["parler", "finir", "attendre", "regarder"])
    def test_regular_verbs_not_flagged(self, verb):
        assert is_irregular_present(verb) is False

    def test_reflexive_irregularity_checks_base_verb(self):
        assert is_irregular_present("se lever") is True
        assert is_irregular_present("se reposer") is False

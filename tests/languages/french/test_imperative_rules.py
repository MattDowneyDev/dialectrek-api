import pytest

from languages.french.imperative_rules import (
    IRREGULAR_IMPERATIVE,
    OUVRIR_TYPE_VERBS,
    VALID_INDICES,
    conjugate_imperative,
)


class TestInvalidPronounIndices:
    @pytest.mark.parametrize("pronoun_index", [0, 2, 5])
    def test_je_il_ils_are_rejected(self, pronoun_index):
        with pytest.raises(ValueError):
            conjugate_imperative("parler", pronoun_index, "affirmative")

    def test_valid_indices_are_tu_nous_vous(self):
        assert VALID_INDICES == (1, 3, 4)


class TestRegularErVerbsDropTuS:
    def test_parler(self):
        assert conjugate_imperative("parler", 1, "affirmative") == "parle"
        assert conjugate_imperative("parler", 3, "affirmative") == "parlons"
        assert conjugate_imperative("parler", 4, "affirmative") == "parlez"

    def test_aller_is_irregular_in_present_but_still_drops_the_s(self):
        assert conjugate_imperative("aller", 1, "affirmative") == "va"


class TestRegularIrReVerbsKeepTuS:
    def test_finir(self):
        assert conjugate_imperative("finir", 1, "affirmative") == "finis"
        assert conjugate_imperative("finir", 3, "affirmative") == "finissons"

    def test_attendre(self):
        assert conjugate_imperative("attendre", 1, "affirmative") == "attends"


class TestOuvrirTypeVerbsDropTuSLikeAnErVerb:
    @pytest.mark.parametrize("verb", sorted(OUVRIR_TYPE_VERBS))
    def test_tu_form_drops_s(self, verb):
        form = conjugate_imperative(verb, 1, "affirmative")
        assert not form.endswith("s")

    def test_ouvrir(self):
        assert conjugate_imperative("ouvrir", 1, "affirmative") == "ouvre"
        assert conjugate_imperative("ouvrir", 3, "affirmative") == "ouvrons"


class TestIrregularImperativeVerbs:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_IMPERATIVE))
    def test_every_irregular_verb_matches_its_own_table(self, verb):
        tu, nous, vous = IRREGULAR_IMPERATIVE[verb]
        assert conjugate_imperative(verb, 1, "affirmative") == tu
        assert conjugate_imperative(verb, 3, "affirmative") == nous
        assert conjugate_imperative(verb, 4, "affirmative") == vous

    def test_etre(self):
        assert conjugate_imperative("être", 1, "affirmative") == "sois"

    def test_avoir(self):
        assert conjugate_imperative("avoir", 1, "affirmative") == "aie"

    def test_savoir(self):
        assert conjugate_imperative("savoir", 1, "affirmative") == "sache"

    def test_vouloir(self):
        assert conjugate_imperative("vouloir", 4, "affirmative") == "veuillez"


class TestNegativePolarity:
    def test_consonant_initial_verb_uses_ne(self):
        assert conjugate_imperative("parler", 1, "negative") == "ne parle pas"

    def test_vowel_initial_verb_elides_to_n_apostrophe(self):
        assert conjugate_imperative("ouvrir", 1, "negative") == "n'ouvre pas"

    def test_aller(self):
        assert conjugate_imperative("aller", 1, "negative") == "ne va pas"


class TestReflexiveVerbs:
    def test_affirmative_pronoun_follows_with_hyphen(self):
        assert conjugate_imperative("se lever", 1, "affirmative") == "lève-toi"
        assert conjugate_imperative("se lever", 3, "affirmative") == "levons-nous"
        assert conjugate_imperative("se lever", 4, "affirmative") == "levez-vous"

    def test_negative_pronoun_stays_in_front_with_elision(self):
        assert conjugate_imperative("se lever", 1, "negative") == "ne te lève pas"

    def test_s_inquieter_negative_elides_te_to_t_apostrophe(self):
        assert conjugate_imperative("s'inquiéter", 1, "negative") == "ne t'inquiète pas"

    def test_s_inquieter_affirmative(self):
        assert conjugate_imperative("s'inquiéter", 1, "affirmative") == "inquiète-toi"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_imperative("  Parler ", 1, "affirmative") == "parle"

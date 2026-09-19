import pytest

from languages.french.present_subjunctive_rules import (
    FULLY_IRREGULAR_SUBJUNCTIVE,
    IRREGULAR_SUBJUNCTIVE_STEMS,
    conjugate_present_subjunctive,
)


class TestRegularVerbs:
    def test_parler(self):
        expected = ["parle", "parles", "parle", "parlions", "parliez", "parlent"]
        for pronoun_index, form in enumerate(expected):
            assert conjugate_present_subjunctive("parler", pronoun_index) == form

    def test_finir(self):
        assert conjugate_present_subjunctive("finir", 0) == "finisse"
        assert conjugate_present_subjunctive("finir", 3) == "finissions"

    def test_attendre(self):
        assert conjugate_present_subjunctive("attendre", 0) == "attende"
        assert conjugate_present_subjunctive("attendre", 5) == "attendent"


class TestStemChangingVerbsInheritPresentIndicativeSplit:
    def test_boire_alternates_stem(self):
        assert conjugate_present_subjunctive("boire", 0) == "boive"
        assert conjugate_present_subjunctive("boire", 3) == "buvions"
        assert conjugate_present_subjunctive("boire", 5) == "boivent"

    def test_acheter_keeps_e_grave_outside_nous_vous(self):
        assert conjugate_present_subjunctive("acheter", 0) == "achète"
        assert conjugate_present_subjunctive("acheter", 3) == "achetions"

    def test_venir(self):
        assert conjugate_present_subjunctive("venir", 0) == "vienne"
        assert conjugate_present_subjunctive("venir", 3) == "venions"


class TestFullyIrregularSubjunctive:
    @pytest.mark.parametrize("verb", sorted(FULLY_IRREGULAR_SUBJUNCTIVE))
    def test_every_fully_irregular_verb_matches_its_own_table(self, verb):
        for pronoun_index, expected in enumerate(FULLY_IRREGULAR_SUBJUNCTIVE[verb]):
            assert conjugate_present_subjunctive(verb, pronoun_index) == expected

    def test_etre(self):
        assert conjugate_present_subjunctive("être", 0) == "sois"
        assert conjugate_present_subjunctive("être", 3) == "soyons"

    def test_avoir_il_form_is_ait_not_aie(self):
        assert conjugate_present_subjunctive("avoir", 2) == "ait"
        assert conjugate_present_subjunctive("avoir", 0) == "aie"


class TestIrregularStemVerbs:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_SUBJUNCTIVE_STEMS))
    def test_singular_and_plural_stems_applied(self, verb):
        singular_stem, plural_stem = IRREGULAR_SUBJUNCTIVE_STEMS[verb]
        assert conjugate_present_subjunctive(verb, 0) == singular_stem + "e"
        assert conjugate_present_subjunctive(verb, 3) == plural_stem + "ions"
        assert conjugate_present_subjunctive(verb, 5) == singular_stem + "ent"

    def test_faire(self):
        assert conjugate_present_subjunctive("faire", 0) == "fasse"
        assert conjugate_present_subjunctive("faire", 3) == "fassions"

    def test_aller_has_different_singular_and_plural_stems(self):
        assert conjugate_present_subjunctive("aller", 0) == "aille"
        assert conjugate_present_subjunctive("aller", 3) == "allions"

    def test_vouloir_has_different_singular_and_plural_stems(self):
        assert conjugate_present_subjunctive("vouloir", 0) == "veuille"
        assert conjugate_present_subjunctive("vouloir", 3) == "voulions"

    def test_savoir(self):
        assert conjugate_present_subjunctive("savoir", 0) == "sache"
        assert conjugate_present_subjunctive("savoir", 3) == "sachions"

    def test_pouvoir(self):
        assert conjugate_present_subjunctive("pouvoir", 0) == "puisse"
        assert conjugate_present_subjunctive("pouvoir", 3) == "puissions"


class TestReflexiveVerbs:
    def test_se_lever_elision_by_pronoun(self):
        assert conjugate_present_subjunctive("se lever", 0) == "me lève"
        assert conjugate_present_subjunctive("se lever", 3) == "nous levions"

    def test_s_habiller_elides_before_vowel_sound(self):
        assert conjugate_present_subjunctive("s'habiller", 0) == "m'habille"
        assert conjugate_present_subjunctive("s'habiller", 2) == "s'habille"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_present_subjunctive("  Parler ", 0) == "parle"

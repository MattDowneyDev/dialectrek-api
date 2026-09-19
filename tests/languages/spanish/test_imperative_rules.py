import pytest

from languages.spanish.imperative_rules import (
    IRREGULAR_TU_AFFIRMATIVE,
    conjugate_imperative,
)


class TestAffirmativeRegularVerb:
    @pytest.mark.parametrize(
        "pronoun_index,expected",
        [
            (1, "habla"),
            (2, "hable"),
            (3, "hablemos"),
            (4, "hablad"),
            (5, "hablen"),
        ],
    )
    def test_regular_affirmative_forms(self, pronoun_index, expected):
        assert conjugate_imperative("hablar", pronoun_index, "affirmative") == expected


class TestNegativeRegularVerb:
    @pytest.mark.parametrize(
        "pronoun_index,expected",
        [
            (1, "no hables"),
            (2, "no hable"),
            (3, "no hablemos"),
            (4, "no habléis"),
            (5, "no hablen"),
        ],
    )
    def test_negative_forms_are_always_the_present_subjunctive(self, pronoun_index, expected):
        assert conjugate_imperative("hablar", pronoun_index, "negative") == expected


class TestTuAffirmativeIrregulars:
    @pytest.mark.parametrize("verb,expected", IRREGULAR_TU_AFFIRMATIVE.items())
    def test_shortened_tu_form_matches_expected(self, verb, expected):
        assert conjugate_imperative(verb, 1, "affirmative") == expected

    def test_tu_negative_is_unaffected_by_the_shortened_form(self):
        # "ten" (affirmative) vs "no tengas" (negative) come from entirely
        # different tenses -- they don't share a stem.
        assert conjugate_imperative("tener", 1, "affirmative") == "ten"
        assert conjugate_imperative("tener", 1, "negative") == "no tengas"

    def test_non_irregular_verb_uses_present_indicative_usted_form(self):
        assert conjugate_imperative("hablar", 1, "affirmative") == "habla"
        assert conjugate_imperative("dormir", 1, "affirmative") == "duerme"
        assert conjugate_imperative("pensar", 1, "affirmative") == "piensa"


class TestNosotrosIrIrregular:
    def test_ir_nosotros_affirmative_is_vamos_not_vayamos(self):
        assert conjugate_imperative("ir", 3, "affirmative") == "vamos"

    def test_ir_nosotros_negative_is_regular_subjunctive_vayamos(self):
        assert conjugate_imperative("ir", 3, "negative") == "no vayamos"

    def test_other_verbs_use_subjunctive_nosotros_normally(self):
        assert conjugate_imperative("hablar", 3, "affirmative") == "hablemos"
        assert conjugate_imperative("tener", 3, "affirmative") == "tengamos"


class TestVosotrosAffirmative:
    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("hablar", "hablad"),
            ("comer", "comed"),
            ("vivir", "vivid"),
            ("ir", "id"),
            ("tener", "tened"),
            ("oír", "oíd"),
        ],
    )
    def test_vosotros_affirmative_is_infinitive_with_r_replaced_by_d(self, verb, expected):
        assert conjugate_imperative(verb, 4, "affirmative") == expected

    def test_vosotros_affirmative_has_no_irregulars(self):
        assert conjugate_imperative("decir", 4, "affirmative") == "decid"
        assert conjugate_imperative("ser", 4, "affirmative") == "sed"

    def test_vosotros_negative_is_regular_subjunctive(self):
        assert conjugate_imperative("hablar", 4, "negative") == "no habléis"

    def test_vosotros_affirmative_requires_r_ending(self):
        with pytest.raises(ValueError):
            conjugate_imperative("hablax", 4, "affirmative")


class TestUstedUstedesAffirmative:
    def test_usted_and_ustedes_use_present_subjunctive(self):
        assert conjugate_imperative("tener", 2, "affirmative") == "tenga"
        assert conjugate_imperative("tener", 5, "affirmative") == "tengan"
        assert conjugate_imperative("seguir", 2, "affirmative") == "siga"
        assert conjugate_imperative("volver", 2, "affirmative") == "vuelva"


class TestStemChangingAndIrregularVerbsFromSmokeTest:
    @pytest.mark.parametrize(
        "verb,pronoun_index,polarity,expected",
        [
            ("mantener", 1, "affirmative", "mantén"),
            ("suponer", 1, "affirmative", "supón"),
            ("decir", 1, "affirmative", "di"),
            ("hacer", 1, "affirmative", "haz"),
            ("ir", 1, "affirmative", "ve"),
            ("ir", 1, "negative", "no vayas"),
            ("poner", 1, "affirmative", "pon"),
            ("salir", 1, "affirmative", "sal"),
            ("ser", 1, "affirmative", "sé"),
            ("ser", 1, "negative", "no seas"),
            ("venir", 1, "affirmative", "ven"),
            ("haber", 1, "affirmative", "he"),
            ("estar", 1, "affirmative", "está"),
            ("dar", 1, "affirmative", "da"),
            ("oír", 1, "affirmative", "oye"),
            ("pedir", 1, "affirmative", "pide"),
        ],
    )
    def test_smoke_cases(self, verb, pronoun_index, polarity, expected):
        assert conjugate_imperative(verb, pronoun_index, polarity) == expected


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_imperative("  HABLAR  ", 1, "affirmative") == "habla"

    def test_no_yo_form_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_imperative("hablar", 0, "affirmative")

    def test_no_yo_form_raises_regardless_of_polarity(self):
        with pytest.raises(ValueError):
            conjugate_imperative("hablar", 0, "negative")

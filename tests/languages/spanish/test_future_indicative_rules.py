import pytest

from languages.spanish.conditional_indicative_rules import IRREGULAR_STEMS
from languages.spanish.future_indicative_rules import conjugate_future_indicative

IRREGULAR_FORMS = {
    "decir": ["diré", "dirás", "dirá", "diremos", "diréis", "dirán"],
    "hacer": ["haré", "harás", "hará", "haremos", "haréis", "harán"],
    "poder": ["podré", "podrás", "podrá", "podremos", "podréis", "podrán"],
    "poner": ["pondré", "pondrás", "pondrá", "pondremos", "pondréis", "pondrán"],
    "querer": ["querré", "querrás", "querrá", "querremos", "querréis", "querrán"],
    "saber": ["sabré", "sabrás", "sabrá", "sabremos", "sabréis", "sabrán"],
    "salir": ["saldré", "saldrás", "saldrá", "saldremos", "saldréis", "saldrán"],
    "tener": ["tendré", "tendrás", "tendrá", "tendremos", "tendréis", "tendrán"],
    "valer": ["valdré", "valdrás", "valdrá", "valdremos", "valdréis", "valdrán"],
    "venir": ["vendré", "vendrás", "vendrá", "vendremos", "vendréis", "vendrán"],
    "caber": ["cabré", "cabrás", "cabrá", "cabremos", "cabréis", "cabrán"],
    "haber": ["habré", "habrás", "habrá", "habremos", "habréis", "habrán"],
    "mantener": ["mantendré", "mantendrás", "mantendrá", "mantendremos", "mantendréis", "mantendrán"],
    "suponer": ["supondré", "supondrás", "supondrá", "supondremos", "supondréis", "supondrán"],
}


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablaré", "hablarás", "hablará", "hablaremos", "hablaréis", "hablarán"]),
            ("comer", ["comeré", "comerás", "comerá", "comeremos", "comeréis", "comerán"]),
            ("vivir", ["viviré", "vivirás", "vivirá", "viviremos", "viviréis", "vivirán"]),
        ],
    )
    def test_regular_conjugation_all_persons(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_future_indicative(verb, i) == expected


class TestIrregularStemVerbs:
    @pytest.mark.parametrize("verb", IRREGULAR_STEMS)
    def test_irregular_stem_verb_matches_expected_forms(self, verb):
        expected = IRREGULAR_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_future_indicative(verb, i) == form

    def test_reuses_conditional_modules_stem_table(self):
        from languages.spanish.future_indicative_rules import IRREGULAR_STEMS as future_stems

        assert future_stems is IRREGULAR_STEMS


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_future_indicative("  HABLAR  ", 0) == "hablaré"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_future_indicative("hablx", 0)

    def test_irregular_stem_verb_bypasses_ending_validation(self):
        assert conjugate_future_indicative("tener", 0) == "tendré"

import pytest

from languages.spanish.conditional_indicative_rules import (
    IRREGULAR_STEMS,
    conjugate_conditional_indicative,
)

IRREGULAR_FORMS = {
    "decir": ["diría", "dirías", "diría", "diríamos", "diríais", "dirían"],
    "hacer": ["haría", "harías", "haría", "haríamos", "haríais", "harían"],
    "poder": ["podría", "podrías", "podría", "podríamos", "podríais", "podrían"],
    "poner": ["pondría", "pondrías", "pondría", "pondríamos", "pondríais", "pondrían"],
    "querer": ["querría", "querrías", "querría", "querríamos", "querríais", "querrían"],
    "saber": ["sabría", "sabrías", "sabría", "sabríamos", "sabríais", "sabrían"],
    "salir": ["saldría", "saldrías", "saldría", "saldríamos", "saldríais", "saldrían"],
    "tener": ["tendría", "tendrías", "tendría", "tendríamos", "tendríais", "tendrían"],
    "valer": ["valdría", "valdrías", "valdría", "valdríamos", "valdríais", "valdrían"],
    "venir": ["vendría", "vendrías", "vendría", "vendríamos", "vendríais", "vendrían"],
    "caber": ["cabría", "cabrías", "cabría", "cabríamos", "cabríais", "cabrían"],
    "haber": ["habría", "habrías", "habría", "habríamos", "habríais", "habrían"],
    "mantener": ["mantendría", "mantendrías", "mantendría", "mantendríamos", "mantendríais", "mantendrían"],
    "suponer": ["supondría", "supondrías", "supondría", "supondríamos", "supondríais", "supondrían"],
}


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablaría", "hablarías", "hablaría", "hablaríamos", "hablaríais", "hablarían"]),
            ("comer", ["comería", "comerías", "comería", "comeríamos", "comeríais", "comerían"]),
            ("vivir", ["viviría", "vivirías", "viviría", "viviríamos", "viviríais", "vivirían"]),
        ],
    )
    def test_regular_conjugation_all_persons(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_conditional_indicative(verb, i) == expected


class TestIrregularStemVerbs:
    @pytest.mark.parametrize("verb", IRREGULAR_STEMS)
    def test_irregular_stem_verb_matches_expected_forms(self, verb):
        expected = IRREGULAR_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_conditional_indicative(verb, i) == form


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_conditional_indicative("  HABLAR  ", 0) == "hablaría"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_conditional_indicative("hablx", 0)

    def test_irregular_stem_verb_bypasses_ending_validation(self):
        assert conjugate_conditional_indicative("tener", 0) == "tendría"

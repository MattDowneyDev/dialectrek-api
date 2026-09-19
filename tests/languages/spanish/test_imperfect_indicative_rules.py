import pytest

from languages.spanish.imperfect_indicative_rules import (
    IRREGULAR_VERBS,
    conjugate_imperfect_indicative,
)


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablaba", "hablabas", "hablaba", "hablábamos", "hablabais", "hablaban"]),
            ("comer", ["comía", "comías", "comía", "comíamos", "comíais", "comían"]),
            ("vivir", ["vivía", "vivías", "vivía", "vivíamos", "vivíais", "vivían"]),
        ],
    )
    def test_regular_conjugation_all_persons(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_imperfect_indicative(verb, i) == expected


class TestFullyIrregularVerbs:
    @pytest.mark.parametrize("verb,forms", IRREGULAR_VERBS.items())
    def test_irregular_verb_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_imperfect_indicative(verb, i) == expected


class TestNoStemChangesOrSpellingShifts:
    def test_present_tense_stem_changers_stay_fully_regular_here(self):
        assert conjugate_imperfect_indicative("pensar", 0) == "pensaba"
        assert conjugate_imperfect_indicative("dormir", 5) == "dormían"
        assert conjugate_imperfect_indicative("pedir", 0) == "pedía"

    def test_car_gar_zar_verbs_stay_fully_regular_here(self):
        assert conjugate_imperfect_indicative("buscar", 0) == "buscaba"
        assert conjugate_imperfect_indicative("llegar", 0) == "llegaba"
        assert conjugate_imperfect_indicative("empezar", 0) == "empezaba"


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_imperfect_indicative("  HABLAR  ", 0) == "hablaba"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_imperfect_indicative("hablx", 0)

    def test_irregular_verb_bypasses_ending_validation(self):
        assert conjugate_imperfect_indicative("ir", 0) == "iba"

    def test_accented_ir_infinitive_normalizes_like_regular_ir(self):
        assert conjugate_imperfect_indicative("oír", 0) == "oía"
        assert conjugate_imperfect_indicative("oír", 3) == "oíamos"

import pytest

from languages.spanish.participle_rules import (
    IRREGULAR_PARTICIPLES,
    conjugate_past_participle,
)


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("hablar", "hablado"),
            ("comer", "comido"),
            ("vivir", "vivido"),
            ("pensar", "pensado"),
            ("dormir", "dormido"),
        ],
    )
    def test_regular_participle(self, verb, expected):
        assert conjugate_past_participle(verb) == expected


class TestIrregularParticiples:
    @pytest.mark.parametrize("verb,expected", IRREGULAR_PARTICIPLES.items())
    def test_irregular_participle_matches_expected_form(self, verb, expected):
        assert conjugate_past_participle(verb) == expected


class TestAccentedVowelStemParticiples:
    # er/-ir verbs with a stem ending in a STRONG vowel (a/e/o) need the
    # accent to keep the "i" of "-ido" its own syllable.
    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("caer", "caído"),
            ("creer", "creído"),
            ("leer", "leído"),
            ("oír", "oído"),
            ("traer", "traído"),
            ("poseer", "poseído"),
        ],
    )
    def test_accented_ido_for_vowel_stem(self, verb, expected):
        assert conjugate_past_participle(verb) == expected

    def test_gu_qu_stem_does_not_get_the_accent(self):
        # the "u" in seguir/-guir stems is silent, not a real vowel, so
        # no hiatus and no accent: seguido, not "seguído"
        assert conjugate_past_participle("seguir") == "seguido"
        assert conjugate_past_participle("conseguir") == "conseguido"


class TestWeakVowelStemParticiples:
    # -uir verbs (construir, destruir, huir, ...) have a stem ending in
    # "u", a weak vowel that forms a diphthong with the following "i"
    # rather than a hiatus -- correct spelling is "construido", not
    # "construído" (compare: "leído" IS correct because "le" ends in the
    # strong vowel "e").
    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("construir", "construido"),
            ("destruir", "destruido"),
            ("incluir", "incluido"),
            ("influir", "influido"),
            ("huir", "huido"),
            ("concluir", "concluido"),
        ],
    )
    def test_uir_verb_participle_has_no_accent(self, verb, expected):
        assert conjugate_past_participle(verb) == expected


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_past_participle("  HABLAR  ") == "hablado"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_past_participle("hablx")

    def test_irregular_verb_bypasses_ending_validation(self):
        assert conjugate_past_participle("decir") == "dicho"

    def test_accented_ir_infinitive_normalizes_like_regular_ir(self):
        assert conjugate_past_participle("oír") == "oído"

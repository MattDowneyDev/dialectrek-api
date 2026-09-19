import pytest

from languages.spanish.imperfect_subjunctive_rules import (
    add_stress_accent,
    conjugate_imperfect_subjunctive,
    get_preterite_ellos_stem,
)
from languages.spanish.preterite_indicative_rules import conjugate_preterite_indicative


def real_preterite_lookup(verb):
    return conjugate_preterite_indicative(verb, 5)


class TestRaFormWithRealPreteriteLookup:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablara", "hablaras", "hablara", "habláramos", "hablarais", "hablaran"]),
            ("comer", ["comiera", "comieras", "comiera", "comiéramos", "comierais", "comieran"]),
            ("vivir", ["viviera", "vivieras", "viviera", "viviéramos", "vivierais", "vivieran"]),
            ("tener", ["tuviera", "tuvieras", "tuviera", "tuviéramos", "tuvierais", "tuvieran"]),
            ("decir", ["dijera", "dijeras", "dijera", "dijéramos", "dijerais", "dijeran"]),
            ("dormir", ["durmiera", "durmieras", "durmiera", "durmiéramos", "durmierais", "durmieran"]),
            ("ser", ["fuera", "fueras", "fuera", "fuéramos", "fuerais", "fueran"]),
        ],
    )
    def test_ra_form_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert (
                conjugate_imperfect_subjunctive(verb, i, form="ra", preterite_lookup=real_preterite_lookup)
                == expected
            )


class TestSeFormWithRealPreteriteLookup:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablase", "hablases", "hablase", "hablásemos", "hablaseis", "hablasen"]),
            ("tener", ["tuviese", "tuvieses", "tuviese", "tuviésemos", "tuvieseis", "tuviesen"]),
        ],
    )
    def test_se_form_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert (
                conjugate_imperfect_subjunctive(verb, i, form="se", preterite_lookup=real_preterite_lookup)
                == expected
            )

    def test_default_form_is_ra(self):
        assert conjugate_imperfect_subjunctive("hablar", 0, preterite_lookup=real_preterite_lookup) == "hablara"


class TestStubbedPreteriteLookup:
    def test_stem_is_derived_purely_from_the_supplied_ellos_form(self):
        assert (
            conjugate_imperfect_subjunctive(
                "whatever", 0, preterite_lookup=lambda v: "zapron"
            )
            == "zapra"
        )

    def test_nosotros_form_accents_the_stem_regardless_of_lookup_source(self):
        assert (
            conjugate_imperfect_subjunctive(
                "whatever", 3, preterite_lookup=lambda v: "hablaron"
            )
            == "habláramos"
        )

    def test_malformed_preterite_form_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_imperfect_subjunctive("hablar", 0, preterite_lookup=lambda v: "nope")

    def test_missing_preterite_lookup_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_imperfect_subjunctive("hablar", 0)

    def test_lookup_receives_the_normalized_verb(self):
        seen = []

        def lookup(verb):
            seen.append(verb)
            return "hablaron"

        conjugate_imperfect_subjunctive("  HABLAR  ", 0, preterite_lookup=lookup)
        assert seen == ["hablar"]


class TestHelperFunctions:
    def test_get_preterite_ellos_stem_strips_ron(self):
        assert get_preterite_ellos_stem("hablar", "hablaron") == "habla"

    def test_get_preterite_ellos_stem_rejects_form_without_ron_suffix(self):
        with pytest.raises(ValueError):
            get_preterite_ellos_stem("hablar", "hablo")

    @pytest.mark.parametrize(
        "stem,expected",
        [
            ("habla", "hablá"),
            ("tuvie", "tuvié"),
            ("dije", "dijé"),
        ],
    )
    def test_add_stress_accent_accents_last_vowel(self, stem, expected):
        assert add_stress_accent(stem) == expected

    def test_add_stress_accent_empty_stem_returns_unchanged(self):
        assert add_stress_accent("") == ""

    def test_add_stress_accent_non_vowel_ending_returns_unchanged(self):
        assert add_stress_accent("xyz") == "xyz"

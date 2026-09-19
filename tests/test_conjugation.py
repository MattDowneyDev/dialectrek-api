"""Tests for the tense/mood dispatch layer in conjugation.py.

These deliberately test *routing* (does the right combination of mood/tense
pick the right underlying conjugator, and does irregularity classification
delegate to the right rule set) rather than re-verifying that any given
conjugated form is linguistically correct -- that belongs to each
languages/<lang>/*_rules.py module's own tests.
"""

import pytest
from fastapi import HTTPException

import conjugation as c
from languages.english.conditional_perfect_rules import conjugate_conditional_perfect
from languages.english.conditional_rules import conjugate_conditional
from languages.english.future_perfect_rules import conjugate_future_perfect
from languages.english.future_rules import conjugate_future
from languages.english.imperfect_indicative_rules import conjugate_imperfect
from languages.english.past_perfect_rules import conjugate_past_perfect
from languages.english.present_indicative_rules import conjugate_present
from languages.english.present_perfect_rules import conjugate_present_perfect
from languages.english.preterite_indicative_rules import conjugate_past
from languages.french.conditional_indicative_rules import (
    conjugate_conditional_indicative as fr_conditional,
)
from languages.french.present_indicative_rules import (
    conjugate_present_indicative as fr_present,
    is_irregular_present as fr_is_present_irregular,
)
from languages.spanish.conditional_indicative_rules import IRREGULAR_STEMS as ES_CONDITIONAL_IRREGULAR
from languages.spanish.imperfect_indicative_rules import IRREGULAR_VERBS as ES_IMPERFECT_IRREGULAR
from languages.spanish.imperfect_subjunctive_rules import conjugate_imperfect_subjunctive
from languages.spanish.participle_rules import IRREGULAR_PARTICIPLES as ES_IRREGULAR_PARTICIPLES
from languages.spanish.present_indicative_rules import (
    IRREGULAR_VERBS as ES_PRESENT_IRREGULAR,
    STEM_CHANGES as ES_STEM_CHANGES,
    conjugate_present_indicative,
)
from languages.spanish.present_subjunctive_rules import (
    IRREGULAR_SUBJUNCTIVE,
    SUBJUNCTIVE_STEM_OVERRIDES,
    conjugate_present_subjunctive,
)
from languages.spanish.preterite_indicative_rules import conjugate_preterite_indicative

REGULAR_VERB = "hablar"


class TestSpanishDispatch:
    @pytest.mark.parametrize(
        "tense,expected_fn",
        [
            ("preterite", conjugate_preterite_indicative),
        ],
    )
    def test_indicative_only_tense_dispatches_correctly(self, tense, expected_fn):
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 1, "indicative", tense) == expected_fn(
            REGULAR_VERB, 1
        )

    @pytest.mark.parametrize(
        "tense",
        ["preterite", "conditional", "conditional_perfect", "future", "future_perfect", "preterite_perfect"],
    )
    def test_indicative_only_tense_rejects_subjunctive(self, tense):
        with pytest.raises(HTTPException) as exc_info:
            c.conjugate_by_tense_mood(REGULAR_VERB, 1, "subjunctive", tense)
        assert exc_info.value.status_code == 422

    def test_present_indicative_dispatch(self):
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 0, "indicative", "present") == (
            conjugate_present_indicative(REGULAR_VERB, 0)
        )

    def test_present_subjunctive_dispatch(self):
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 0, "subjunctive", "present") == (
            conjugate_present_subjunctive(REGULAR_VERB, 0)
        )

    def test_imperfect_indicative_dispatch(self):
        from languages.spanish.imperfect_indicative_rules import conjugate_imperfect_indicative

        assert c.conjugate_by_tense_mood(REGULAR_VERB, 2, "indicative", "imperfect") == (
            conjugate_imperfect_indicative(REGULAR_VERB, 2)
        )

    def test_imperfect_subjunctive_dispatch_uses_preterite_ellos_stem(self):
        expected = conjugate_imperfect_subjunctive(
            REGULAR_VERB, 3, form="ra", preterite_lookup=c.preterite_ellos
        )
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 3, "subjunctive", "imperfect") == expected

    def test_perfect_indicative_vs_subjunctive_dispatch(self):
        from languages.spanish.present_perfect_indicative_rules import (
            conjugate_present_perfect_indicative,
        )
        from languages.spanish.present_perfect_subjunctive_rules import (
            conjugate_present_perfect_subjunctive,
        )

        assert c.conjugate_by_tense_mood(REGULAR_VERB, 0, "indicative", "perfect") == (
            conjugate_present_perfect_indicative(REGULAR_VERB, 0)
        )
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 0, "subjunctive", "perfect") == (
            conjugate_present_perfect_subjunctive(REGULAR_VERB, 0)
        )

    def test_pluperfect_indicative_vs_subjunctive_dispatch(self):
        from languages.spanish.pluperfect_indicative_rules import conjugate_pluperfect_indicative
        from languages.spanish.pluperfect_subjunctive_rules import conjugate_pluperfect_subjunctive

        assert c.conjugate_by_tense_mood(REGULAR_VERB, 0, "indicative", "pluperfect") == (
            conjugate_pluperfect_indicative(REGULAR_VERB, 0)
        )
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 0, "subjunctive", "pluperfect") == (
            conjugate_pluperfect_subjunctive(REGULAR_VERB, 0, form="ra")
        )

    def test_imperative_dispatch(self):
        from languages.spanish.imperative_rules import conjugate_imperative

        assert c.conjugate_by_tense_mood(REGULAR_VERB, 1, "indicative", "imperative") == (
            conjugate_imperative(REGULAR_VERB, 1, "affirmative")
        )
        assert c.conjugate_by_tense_mood(REGULAR_VERB, 1, "indicative", "imperative", "negative") == (
            conjugate_imperative(REGULAR_VERB, 1, "negative")
        )

    def test_subjunctive_ra_se_alt_form_only_applies_to_ra_se_tenses(self):
        assert c.subjunctive_ra_se_alt_form(REGULAR_VERB, 0, "indicative", "present") is None
        assert c.subjunctive_ra_se_alt_form(REGULAR_VERB, 0, "subjunctive", "present") is None

        expected_imperfect = conjugate_imperfect_subjunctive(
            REGULAR_VERB, 0, form="se", preterite_lookup=c.preterite_ellos
        )
        assert c.subjunctive_ra_se_alt_form(REGULAR_VERB, 0, "subjunctive", "imperfect") == expected_imperfect

        from languages.spanish.pluperfect_subjunctive_rules import conjugate_pluperfect_subjunctive

        expected_pluperfect = conjugate_pluperfect_subjunctive(REGULAR_VERB, 0, form="se")
        assert (
            c.subjunctive_ra_se_alt_form(REGULAR_VERB, 0, "subjunctive", "pluperfect")
            == expected_pluperfect
        )

    @pytest.mark.parametrize(
        "verb,mood,tense,expected",
        [
            # preterite irregularity families
            ("hablar", "indicative", "preterite", False),
            ("tener", "indicative", "preterite", True),  # IRREGULAR_VERBS
            # imperfect subjunctive inherits preterite's classification
            ("tener", "subjunctive", "imperfect", True),
            ("hablar", "subjunctive", "imperfect", False),
            # imperfect indicative has its own tiny irregular set
            ("ir", "indicative", "imperfect", True),
            ("hablar", "indicative", "imperfect", False),
            # future/conditional share one irregular-stem set
            ("tener", "indicative", "future", True),
            ("hablar", "indicative", "future", False),
            ("tener", "indicative", "conditional", True),
            # compound tenses key off participle irregularity
            ("hablar", "indicative", "perfect", False),
            # present indicative/subjunctive
            ("hablar", "indicative", "present", False),
            ("tener", "indicative", "present", True),
            ("hablar", "subjunctive", "present", False),
        ],
    )
    def test_is_irregular_classification(self, verb, mood, tense, expected):
        assert c.is_irregular(verb, mood, tense) is expected

    def test_is_irregular_imperfect_indicative_uses_its_own_set(self):
        for verb in ES_IMPERFECT_IRREGULAR:
            assert c.is_irregular(verb, "indicative", "imperfect") is True

    def test_is_irregular_future_conditional_use_shared_stem_set(self):
        for verb in ES_CONDITIONAL_IRREGULAR:
            assert c.is_irregular(verb, "indicative", "future") is True
            assert c.is_irregular(verb, "indicative", "conditional") is True

    @pytest.mark.parametrize("tense", ["perfect", "conditional_perfect", "future_perfect", "preterite_perfect", "pluperfect"])
    def test_is_irregular_compound_tenses_use_participle_irregularity(self, tense):
        for verb in ES_IRREGULAR_PARTICIPLES:
            assert c.is_irregular(verb, "indicative", tense) is True
        assert c.is_irregular("hablar", "indicative", tense) is False

    def test_is_irregular_imperative_inherits_subjunctive_classification(self):
        for verb in list(IRREGULAR_SUBJUNCTIVE) + list(SUBJUNCTIVE_STEM_OVERRIDES) + list(ES_STEM_CHANGES):
            assert c.is_irregular(verb, "indicative", "imperative") is True
        assert c.is_irregular("hablar", "indicative", "imperative") is False

    def test_is_irregular_subjunctive_mood_falls_back_to_subjunctive_set(self):
        for verb in IRREGULAR_SUBJUNCTIVE:
            assert c.is_irregular(verb, "subjunctive", "present") is True

    def test_is_irregular_default_present_indicative_set(self):
        for verb in ES_PRESENT_IRREGULAR:
            assert c.is_irregular(verb, "indicative", "present") is True
        for verb in ES_STEM_CHANGES:
            assert c.is_irregular(verb, "indicative", "present") is True


class TestEnglishDispatch:
    @pytest.mark.parametrize(
        "tense,expected_fn",
        [
            ("conditional_perfect", conjugate_conditional_perfect),
            ("conditional", conjugate_conditional),
            ("future_perfect", conjugate_future_perfect),
            ("future", conjugate_future),
            ("preterite_perfect", conjugate_past_perfect),
            ("pluperfect", conjugate_past_perfect),
            ("preterite", conjugate_past),
            ("imperfect", conjugate_imperfect),
            ("perfect", conjugate_present_perfect),
            ("present", conjugate_present),
            ("some_unmapped_tense", conjugate_present),
        ],
    )
    def test_conjugate_english_dispatches_by_tense(self, tense, expected_fn):
        assert c.conjugate_english("to speak", 1, tense) == expected_fn("to speak", 1)

    def test_conjugate_english_imperative_uses_polarity(self):
        from languages.english.imperative_rules import conjugate_imperative

        assert c.conjugate_english("to speak", 1, "imperative", "affirmative") == (
            conjugate_imperative("to speak", 1, "affirmative")
        )
        assert c.conjugate_english("to speak", 1, "imperative", "negative") == (
            conjugate_imperative("to speak", 1, "negative")
        )


class TestFrenchDispatch:
    def test_conjugate_french_indicative_dispatch(self):
        assert c.conjugate_french("parler", 0, "indicative", "present") == fr_present("parler", 0)
        assert c.conjugate_french("parler", 0, "indicative", "conditional") == fr_conditional(
            "parler", 0
        )

    def test_conjugate_french_subjunctive_present_dispatch(self):
        from languages.french.present_subjunctive_rules import conjugate_present_subjunctive

        assert c.conjugate_french("parler", 0, "subjunctive", "present") == (
            conjugate_present_subjunctive("parler", 0)
        )

    def test_conjugate_french_imperative_uses_polarity(self):
        from languages.french.imperative_rules import conjugate_imperative

        assert c.conjugate_french("parler", 1, "indicative", "imperative", "affirmative") == (
            conjugate_imperative("parler", 1, "affirmative")
        )
        assert c.conjugate_french("parler", 1, "indicative", "imperative", "negative") == (
            conjugate_imperative("parler", 1, "negative")
        )

    def test_conjugate_french_unsupported_tense_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            c.conjugate_french("parler", 0, "indicative", "preterite")
        assert exc_info.value.status_code == 422

    def test_conjugate_french_unsupported_subjunctive_tense_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            c.conjugate_french("parler", 0, "subjunctive", "imperfect")
        assert exc_info.value.status_code == 422

    def test_is_irregular_french_present_and_imperative_share_present_stem(self):
        for verb in ["etre", "être", "parler"]:
            assert c.is_irregular_french(verb, "indicative", "present") == fr_is_present_irregular(verb)
            assert c.is_irregular_french(verb, "indicative", "imperative") == fr_is_present_irregular(
                verb
            )

    def test_is_irregular_french_subjunctive_uses_present_stem_too(self):
        assert c.is_irregular_french("parler", "subjunctive", "present") == fr_is_present_irregular(
            "parler"
        )

    @pytest.mark.parametrize("tense", ["perfect", "pluperfect"])
    def test_is_irregular_french_compound_uses_participle_irregularity(self, tense):
        from languages.french.participle_rules import is_irregular_participle

        for verb in ["parler", "être", "avoir", "finir"]:
            assert c.is_irregular_french(verb, "indicative", tense) == is_irregular_participle(verb)

    @pytest.mark.parametrize("tense", ["future", "future_perfect"])
    def test_is_irregular_french_future_uses_future_irregularity(self, tense):
        from languages.french.future_indicative_rules import is_irregular_future

        for verb in ["parler", "être", "avoir", "aller"]:
            assert c.is_irregular_french(verb, "indicative", tense) == is_irregular_future(verb)

    @pytest.mark.parametrize("tense", ["conditional", "conditional_perfect"])
    def test_is_irregular_french_conditional_uses_conditional_irregularity(self, tense):
        from languages.french.conditional_indicative_rules import is_irregular_conditional

        for verb in ["parler", "être", "avoir", "aller"]:
            assert c.is_irregular_french(verb, "indicative", tense) == is_irregular_conditional(verb)

    def test_no_subjunctive_alt_form_always_none(self):
        assert c.no_subjunctive_alt_form("parler", 0, "subjunctive", "present") is None
        assert c.no_subjunctive_alt_form("parler", 0, "indicative", "imperfect") is None


def test_preterite_ellos_matches_direct_call():
    assert c.preterite_ellos("hablar") == conjugate_preterite_indicative("hablar", 5)

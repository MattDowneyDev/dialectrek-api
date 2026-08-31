"""Tense/mood dispatch layer: routes a (mood, tense) pair to the right
per-tense conjugator function for each language, and classifies verbs as
regular/irregular for a given (mood, tense). Keeps main.py to just routes.
"""

from typing import Callable, Literal

from fastapi import HTTPException

from languages.spanish.present_indicative_rules import (
    IRREGULAR_VERBS,
    STEM_CHANGES,
    PRONOUNS,
    conjugate_present_indicative,
)
from languages.spanish.present_subjunctive_rules import (
    IRREGULAR_SUBJUNCTIVE,
    SUBJUNCTIVE_STEM_OVERRIDES,
    conjugate_present_subjunctive,
)
from languages.spanish.preterite_indicative_rules import (
    IRREGULAR_VERBS as PRETERITE_IRREGULAR_VERBS,
    STRONG_STEMS as PRETERITE_STRONG_STEMS,
    IR_STEM_CHANGES as PRETERITE_IR_STEM_CHANGES,
    I_TO_Y_VERBS as PRETERITE_I_TO_Y_VERBS,
    conjugate_preterite_indicative,
)
from languages.spanish.imperfect_indicative_rules import (
    IRREGULAR_VERBS as IMPERFECT_IRREGULAR_VERBS,
    conjugate_imperfect_indicative,
)
from languages.spanish.conditional_indicative_rules import (
    IRREGULAR_STEMS as CONDITIONAL_IRREGULAR_STEMS,
    conjugate_conditional_indicative,
)
from languages.spanish.conditional_perfect_indicative_rules import (
    conjugate_conditional_perfect_indicative,
)
from languages.spanish.future_indicative_rules import conjugate_future_indicative
from languages.spanish.future_perfect_indicative_rules import conjugate_future_perfect_indicative
from languages.spanish.imperative_rules import conjugate_imperative as conjugate_imperative_spanish
from languages.spanish.imperfect_subjunctive_rules import conjugate_imperfect_subjunctive
from languages.spanish.participle_rules import IRREGULAR_PARTICIPLES
from languages.spanish.present_perfect_indicative_rules import conjugate_present_perfect_indicative
from languages.spanish.present_perfect_subjunctive_rules import conjugate_present_perfect_subjunctive
from languages.spanish.preterite_perfect_indicative_rules import conjugate_preterite_perfect_indicative
from languages.spanish.pluperfect_indicative_rules import conjugate_pluperfect_indicative
from languages.spanish.pluperfect_subjunctive_rules import conjugate_pluperfect_subjunctive
from languages.english.present_indicative_rules import conjugate_present
from languages.english.preterite_indicative_rules import conjugate_past
from languages.english.imperfect_indicative_rules import conjugate_imperfect
from languages.english.present_perfect_rules import conjugate_present_perfect
from languages.english.conditional_rules import conjugate_conditional
from languages.english.conditional_perfect_rules import conjugate_conditional_perfect
from languages.english.future_rules import conjugate_future
from languages.english.future_perfect_rules import conjugate_future_perfect
from languages.english.past_perfect_rules import conjugate_past_perfect
from languages.english.imperative_rules import conjugate_imperative as conjugate_imperative_english
from languages.french.conditional_indicative_rules import (
    conjugate_conditional_indicative as conjugate_french_conditional_indicative,
    is_irregular_conditional as is_french_conditional_irregular,
)
from languages.french.conditional_perfect_indicative_rules import (
    conjugate_conditional_perfect_indicative as conjugate_french_conditional_perfect_indicative,
)
from languages.french.future_indicative_rules import (
    conjugate_future_indicative as conjugate_french_future_indicative,
    is_irregular_future as is_french_future_irregular,
)
from languages.french.future_perfect_indicative_rules import (
    conjugate_future_perfect_indicative as conjugate_french_future_perfect_indicative,
)
from languages.french.imperative_rules import conjugate_imperative as conjugate_imperative_french
from languages.french.imperfect_indicative_rules import (
    conjugate_imperfect_indicative as conjugate_french_imperfect_indicative,
    is_irregular_imperfect as is_french_imperfect_irregular,
)
from languages.french.participle_rules import is_irregular_participle as is_french_participle_irregular
from languages.french.pluperfect_indicative_rules import (
    conjugate_pluperfect_indicative as conjugate_french_pluperfect_indicative,
)
from languages.french.present_indicative_rules import (
    conjugate_present_indicative as conjugate_french_present_indicative,
    is_irregular_present as is_french_present_irregular,
)
from languages.french.present_perfect_indicative_rules import (
    conjugate_present_perfect_indicative as conjugate_french_present_perfect_indicative,
)
from languages.french.present_perfect_subjunctive_rules import (
    conjugate_present_perfect_subjunctive as conjugate_french_present_perfect_subjunctive,
)
from languages.french.present_subjunctive_rules import (
    conjugate_present_subjunctive as conjugate_french_present_subjunctive,
)

Mood = Literal["indicative", "subjunctive"]
Polarity = Literal["affirmative", "negative"]
Tense = Literal[
    "present", "preterite", "imperfect", "perfect", "future", "future_perfect",
    "conditional", "conditional_perfect", "preterite_perfect", "pluperfect",
    "imperative",
]

# Present tense only pronoun labels, matching conjugator.PRONOUNS index order
PRONOUNS_ENGLISH = ["I", "you", "he/she/you", "we", "you all", "they/you all"]

# Indices into PRONOUNS/PRONOUNS_ENGLISH used when vosotros is excluded
NON_VOSOTROS_INDICES = [0, 1, 2, 3, 5]
ALL_INDICES = [0, 1, 2, 3, 4, 5]

# The imperative has no "yo" form -- you can't command yourself -- so
# it uses its own index lists (and its own pronoun labels below) that
# exclude index 0 entirely.
IMPERATIVE_INDICES = [1, 2, 3, 4, 5]
IMPERATIVE_NON_VOSOTROS_INDICES = [1, 2, 3, 5]

# Imperative-specific pronoun labels: "el/ella/usted" and "ellos/ustedes"
# collapse to their "you" reading only, since a command can't be
# addressed to "he/she/they". Index 0 is a placeholder, never used.
IMPERATIVE_PRONOUNS_SPANISH = ["", "tú", "usted", "nosotros", "vosotros", "ustedes"]
IMPERATIVE_PRONOUNS_ENGLISH = ["", "you", "you (formal)", "let's", "you all", "you all (formal)"]

# French only has tu/nous/vous commands -- no "usted"-style formal
# third person the way Spanish has, so indices 2 and 5 are placeholders
# here too, alongside 0.
FRENCH_IMPERATIVE_INDICES = [1, 3, 4]
FRENCH_IMPERATIVE_PRONOUNS = ["", "tu", "", "nous", "vous", ""]
FRENCH_IMPERATIVE_PRONOUNS_ENGLISH = ["", "you", "", "let's", "you all", ""]

# Tenses that only exist in the indicative mood: routing is a plain
# tense -> conjugator lookup, and asking for the subjunctive of one of
# these is a 422.
INDICATIVE_ONLY_CONJUGATORS: dict[Tense, Callable[[str, int], str]] = {
    "preterite": conjugate_preterite_indicative,
    "conditional": conjugate_conditional_indicative,
    "conditional_perfect": conjugate_conditional_perfect_indicative,
    "future": conjugate_future_indicative,
    "future_perfect": conjugate_future_perfect_indicative,
    "preterite_perfect": conjugate_preterite_perfect_indicative,
}

# Every English tense also reduces to a plain tense -> conjugator lookup
# (English doesn't distinguish mood the way Spanish does). Falls back to
# conjugate_present for "present" and any other unlisted tense.
ENGLISH_CONJUGATORS: dict[Tense, Callable[[str, int], str]] = {
    "conditional_perfect": conjugate_conditional_perfect,
    "conditional": conjugate_conditional,
    "future_perfect": conjugate_future_perfect,
    "future": conjugate_future,
    "preterite_perfect": conjugate_past_perfect,
    "pluperfect": conjugate_past_perfect,
    "preterite": conjugate_past,
    "imperfect": conjugate_imperfect,
    "perfect": conjugate_present_perfect,
}


def preterite_ellos(verb: str) -> str:
    return conjugate_preterite_indicative(verb, 5)


def _is_preterite_irregular(verb: str) -> bool:
    return (
        verb in PRETERITE_IRREGULAR_VERBS
        or verb in PRETERITE_STRONG_STEMS
        or verb in PRETERITE_IR_STEM_CHANGES
        or verb in PRETERITE_I_TO_Y_VERBS
    )


def _is_subjunctive_irregular(verb: str) -> bool:
    return (
        verb in IRREGULAR_SUBJUNCTIVE
        or verb in SUBJUNCTIVE_STEM_OVERRIDES
        or verb in STEM_CHANGES
    )


def is_irregular(verb: str, mood: Mood, tense: Tense) -> bool:
    # The imperfect subjunctive stem is derived directly from the
    # preterite ellos/ustedes form, so it inherits preterite's
    # irregularity classification exactly.
    if tense == "preterite" or (tense == "imperfect" and mood == "subjunctive"):
        return _is_preterite_irregular(verb)
    if tense == "imperfect":
        return verb in IMPERFECT_IRREGULAR_VERBS
    if tense in ("conditional", "future"):
        # Future and conditional build on the exact same modified stem
        # for their irregulars (tener -> tendr-, hacer -> har-, ...).
        return verb in CONDITIONAL_IRREGULAR_STEMS
    if tense in (
        "perfect", "conditional_perfect", "future_perfect", "preterite_perfect", "pluperfect",
    ):
        # haber itself doesn't vary by verb in any of these compounds --
        # "hube"/"había"/"hubiera" are each fixed regardless of the main
        # verb -- so what makes one of these forms "irregular" here is an
        # irregular participle.
        return verb in IRREGULAR_PARTICIPLES
    if tense == "imperative":
        # Every imperative form except affirmative-tu is either a direct
        # present-subjunctive form or "no" + one, so it inherits that
        # tense's irregularity classification exactly. Affirmative-tu's
        # own irregulars (decir, hacer, ir, ...) are already covered by
        # this same set, so no separate check is needed for them.
        return _is_subjunctive_irregular(verb)
    if mood == "subjunctive":
        return _is_subjunctive_irregular(verb)
    return verb in IRREGULAR_VERBS or verb in STEM_CHANGES


def conjugate_by_tense_mood(
    verb: str, pronoun_index: int, mood: Mood, tense: Tense, polarity: Polarity = "affirmative",
) -> str:
    if tense == "imperative":
        return conjugate_imperative_spanish(verb, pronoun_index, polarity)
    if tense in INDICATIVE_ONLY_CONJUGATORS:
        if mood == "subjunctive":
            display_tense = tense.replace("_", " ").capitalize()
            raise HTTPException(
                status_code=422,
                detail=f"{display_tense} subjunctive is not supported.",
            )
        return INDICATIVE_ONLY_CONJUGATORS[tense](verb, pronoun_index)
    if tense == "imperfect":
        if mood == "subjunctive":
            return conjugate_imperfect_subjunctive(
                verb, pronoun_index, form="ra", preterite_lookup=preterite_ellos,
            )
        return conjugate_imperfect_indicative(verb, pronoun_index)
    if tense == "perfect":
        if mood == "subjunctive":
            return conjugate_present_perfect_subjunctive(verb, pronoun_index)
        return conjugate_present_perfect_indicative(verb, pronoun_index)
    if tense == "pluperfect":
        if mood == "subjunctive":
            return conjugate_pluperfect_subjunctive(verb, pronoun_index, form="ra")
        return conjugate_pluperfect_indicative(verb, pronoun_index)
    if mood == "subjunctive":
        return conjugate_present_subjunctive(verb, pronoun_index)
    return conjugate_present_indicative(verb, pronoun_index)


def subjunctive_ra_se_alt_form(verb: str, pronoun_index: int, mood: Mood, tense: Tense) -> str | None:
    """The '-se' spelling, equally correct alongside the '-ra' form
    returned by conjugate_by_tense_mood. Only applies to the two
    subjunctive tenses built on the '-ra'/'-se' stem (imperfect and
    pluperfect subjunctive) -- every other tense/mood combination has
    just one spelling."""
    if tense == "imperfect" and mood == "subjunctive":
        return conjugate_imperfect_subjunctive(
            verb, pronoun_index, form="se", preterite_lookup=preterite_ellos,
        )
    if tense == "pluperfect" and mood == "subjunctive":
        return conjugate_pluperfect_subjunctive(verb, pronoun_index, form="se")
    return None


def conjugate_english(
    infinitive_english: str, pronoun_index: int, tense: Tense, polarity: Polarity = "affirmative",
) -> str:
    if tense == "imperative":
        return conjugate_imperative_english(infinitive_english, pronoun_index, polarity)
    conjugator = ENGLISH_CONJUGATORS.get(tense, conjugate_present)
    return conjugator(infinitive_english, pronoun_index)


# French doesn't have every tense built out yet -- anything not in
# here 422s instead. Conditional has no subjunctive form in French at
# all, so it only ever shows up in the indicative dict.
FRENCH_INDICATIVE_CONJUGATORS: dict[Tense, Callable[[str, int], str]] = {
    "present": conjugate_french_present_indicative,
    "imperfect": conjugate_french_imperfect_indicative,
    "perfect": conjugate_french_present_perfect_indicative,
    "pluperfect": conjugate_french_pluperfect_indicative,
    "future": conjugate_french_future_indicative,
    "future_perfect": conjugate_french_future_perfect_indicative,
    "conditional": conjugate_french_conditional_indicative,
    "conditional_perfect": conjugate_french_conditional_perfect_indicative,
}

FRENCH_SUBJUNCTIVE_CONJUGATORS: dict[Tense, Callable[[str, int], str]] = {
    "present": conjugate_french_present_subjunctive,
    "perfect": conjugate_french_present_perfect_subjunctive,
}


def conjugate_french(
    verb: str, pronoun_index: int, mood: Mood, tense: Tense, polarity: Polarity = "affirmative",
) -> str:
    if tense == "imperative":
        return conjugate_imperative_french(verb, pronoun_index, polarity)

    conjugators = FRENCH_SUBJUNCTIVE_CONJUGATORS if mood == "subjunctive" else FRENCH_INDICATIVE_CONJUGATORS
    if tense not in conjugators:
        display_tense = tense.replace("_", " ").capitalize()
        display_mood = "" if mood == "indicative" else " subjunctive"
        raise HTTPException(
            status_code=422,
            detail=f"{display_tense}{display_mood} is not supported for French yet.",
        )
    return conjugators[tense](verb, pronoun_index)


def is_irregular_french(verb: str, mood: Mood, tense: Tense) -> bool:
    if tense in ("imperfect",):
        return is_french_imperfect_irregular(verb)
    if tense in ("perfect", "pluperfect"):
        return is_french_participle_irregular(verb)
    if tense in ("future", "future_perfect"):
        return is_french_future_irregular(verb)
    if tense in ("conditional", "conditional_perfect"):
        return is_french_conditional_irregular(verb)
    # present, imperative, and the subjunctive tenses all key off the
    # same present-tense irregularity -- that's the stem everything
    # else here is built from
    return is_french_present_irregular(verb)


def no_subjunctive_alt_form(verb: str, pronoun_index: int, mood: Mood, tense: Tense) -> str | None:
    """French has no tense with two equally-correct spellings the way
    Spanish's '-ra'/'-se' subjunctive does, so this always returns None."""
    return None

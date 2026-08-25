import json
import random
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
from languages.english.present_indicative_rules import conjugate_present
from languages.english.preterite_indicative_rules import conjugate_past
from languages.english.conditional_rules import conjugate_conditional
from languages.english.conditional_perfect_rules import conjugate_conditional_perfect
from languages.english.future_rules import conjugate_future
from languages.english.future_perfect_rules import conjugate_future_perfect
from languages.english.imperative_rules import conjugate_imperative as conjugate_imperative_english

Mood = Literal["indicative", "subjunctive"]
Polarity = Literal["affirmative", "negative"]
Tense = Literal[
    "present", "preterite", "imperfect", "perfect", "future", "future_perfect",
    "conditional", "conditional_perfect", "imperative",
]

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # TODO: add the production frontend URL here once it's deployed on Vercel.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

VERBS_FILE = "./languages/spanish/verbs.json"

# Present tense only pronoun labels, matching conjugator.PRONOUNS index order
PRONOUNS_ENGLISH = ["I", "you", "he/she/you (usted)", "we", "you all (vosotros)", "they/you all (ustedes)"]

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
IMPERATIVE_PRONOUNS_ENGLISH = ["", "you", "you (usted)", "let's", "you all (vosotros)", "you all (ustedes)"]


def load_verbs():
    with open(VERBS_FILE, encoding="utf-8") as f:
        return json.load(f)


def preterite_ellos(verb: str) -> str:
    return conjugate_preterite_indicative(verb, 5)


def is_irregular(verb: str, mood: Mood, tense: Tense) -> bool:
    # The imperfect subjunctive stem is derived directly from the
    # preterite ellos/ustedes form, so it inherits preterite's
    # irregularity classification exactly.
    if tense == "preterite" or (tense == "imperfect" and mood == "subjunctive"):
        return (
            verb in PRETERITE_IRREGULAR_VERBS
            or verb in PRETERITE_STRONG_STEMS
            or verb in PRETERITE_IR_STEM_CHANGES
            or verb in PRETERITE_I_TO_Y_VERBS
        )
    if tense == "imperfect":
        return verb in IMPERFECT_IRREGULAR_VERBS
    if tense in ("conditional", "future"):
        # Future and conditional build on the exact same modified stem
        # for their irregulars (tener -> tendr-, hacer -> har-, ...).
        return verb in CONDITIONAL_IRREGULAR_STEMS
    if tense in ("perfect", "conditional_perfect", "future_perfect"):
        # haber itself doesn't vary by verb, so what makes a perfect-tense
        # form "irregular" here is an irregular participle.
        return verb in IRREGULAR_PARTICIPLES
    if tense == "imperative":
        # Every imperative form except affirmative-tu is either a direct
        # present-subjunctive form or "no" + one, so it inherits that
        # tense's irregularity classification exactly. Affirmative-tu's
        # own irregulars (decir, hacer, ir, ...) are already covered by
        # this same set, so no separate check is needed for them.
        return (
            verb in IRREGULAR_SUBJUNCTIVE
            or verb in SUBJUNCTIVE_STEM_OVERRIDES
            or verb in STEM_CHANGES
        )
    if mood == "subjunctive":
        return (
            verb in IRREGULAR_SUBJUNCTIVE
            or verb in SUBJUNCTIVE_STEM_OVERRIDES
            or verb in STEM_CHANGES
        )
    return verb in IRREGULAR_VERBS or verb in STEM_CHANGES


def conjugate_by_tense_mood(
    verb: str, pronoun_index: int, mood: Mood, tense: Tense, polarity: Polarity = "affirmative",
) -> str:
    if tense == "imperative":
        return conjugate_imperative_spanish(verb, pronoun_index, polarity)
    if tense == "preterite":
        if mood == "subjunctive":
            raise HTTPException(
                status_code=422,
                detail="Preterite subjunctive is not supported.",
            )
        return conjugate_preterite_indicative(verb, pronoun_index)
    if tense == "conditional":
        if mood == "subjunctive":
            raise HTTPException(
                status_code=422,
                detail="Conditional subjunctive is not supported.",
            )
        return conjugate_conditional_indicative(verb, pronoun_index)
    if tense == "conditional_perfect":
        if mood == "subjunctive":
            raise HTTPException(
                status_code=422,
                detail="Conditional perfect subjunctive is not supported.",
            )
        return conjugate_conditional_perfect_indicative(verb, pronoun_index)
    if tense == "future":
        if mood == "subjunctive":
            raise HTTPException(
                status_code=422,
                detail="Future subjunctive is not supported.",
            )
        return conjugate_future_indicative(verb, pronoun_index)
    if tense == "future_perfect":
        if mood == "subjunctive":
            raise HTTPException(
                status_code=422,
                detail="Future perfect subjunctive is not supported.",
            )
        return conjugate_future_perfect_indicative(verb, pronoun_index)
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
    if mood == "subjunctive":
        return conjugate_present_subjunctive(verb, pronoun_index)
    return conjugate_present_indicative(verb, pronoun_index)


def imperfect_subjunctive_alt_form(verb: str, pronoun_index: int, mood: Mood, tense: Tense) -> str | None:
    """The '-se' spelling, equally correct alongside the '-ra' form
    returned by conjugate_by_tense_mood. Only applies to imperfect
    subjunctive -- every other tense/mood combination has one spelling."""
    if tense == "imperfect" and mood == "subjunctive":
        return conjugate_imperfect_subjunctive(
            verb, pronoun_index, form="se", preterite_lookup=preterite_ellos,
        )
    return None


def conjugate_english(
    infinitive_english: str, pronoun_index: int, tense: Tense, polarity: Polarity = "affirmative",
) -> str:
    if tense == "imperative":
        return conjugate_imperative_english(infinitive_english, pronoun_index, polarity)
    if tense == "conditional_perfect":
        return conjugate_conditional_perfect(infinitive_english, pronoun_index)
    if tense == "conditional":
        return conjugate_conditional(infinitive_english, pronoun_index)
    if tense == "future_perfect":
        return conjugate_future_perfect(infinitive_english, pronoun_index)
    if tense == "future":
        return conjugate_future(infinitive_english, pronoun_index)
    if tense in ("preterite", "imperfect", "perfect"):
        return conjugate_past(infinitive_english, pronoun_index)
    return conjugate_present(infinitive_english, pronoun_index)


@app.get("/get-all-verbs")
def get_all_verbs():
    verbs = load_verbs()
    verbs_list = [[verb["spanish"], verb["english"]] for verb in verbs]
    verbs_list.sort()
    return verbs_list


@app.get("/get-verb-conjugation")
def get_verb_conjugation(verb: str, mood: Mood = "indicative", tense: Tense = "present"):
    verbs = load_verbs()
    verb_entry = next((v for v in verbs if v["spanish"] == verb), None)

    if verb_entry is None:
        raise HTTPException(status_code=404, detail=f"Verb '{verb}' not found")

    if tense == "imperative":
        # The imperative has no single "mood"-like axis the way other
        # tenses do -- affirmative and negative are both worth seeing
        # side by side on the same row, so this shape carries both
        # instead of picking one via a query parameter.
        conjugations = [
            {
                "pronoun_spanish": IMPERATIVE_PRONOUNS_SPANISH[i],
                "pronoun_english": IMPERATIVE_PRONOUNS_ENGLISH[i],
                "form_spanish_affirmative": conjugate_imperative_spanish(verb_entry["spanish"], i, "affirmative"),
                "form_spanish_negative": conjugate_imperative_spanish(verb_entry["spanish"], i, "negative"),
                "form_english_affirmative": conjugate_imperative_english(verb_entry["english"], i, "affirmative"),
                "form_english_negative": conjugate_imperative_english(verb_entry["english"], i, "negative"),
            }
            for i in IMPERATIVE_INDICES
        ]
    else:
        conjugations = [
            {
                "pronoun_spanish": PRONOUNS[i],
                "pronoun_english": PRONOUNS_ENGLISH[i],
                "form_spanish": conjugate_by_tense_mood(verb_entry["spanish"], i, mood, tense),
                "form_spanish_alt": imperfect_subjunctive_alt_form(verb_entry["spanish"], i, mood, tense),
                "form_english": conjugate_english(verb_entry["english"], i, tense),
            }
            for i in ALL_INDICES
        ]

    return {
        "infinitive_spanish": verb_entry["spanish"],
        "infinitive_english": verb_entry["english"],
        "mood_english": mood,
        "tense_english": tense,
        "conjugations": conjugations,
    }


@app.get("/get-random-verb-conjugation")
def get_random_verb_conjugation(
    use_irregular: bool,
    use_vosotros: bool,
    mood: Mood = "indicative",
    tense: Tense = "present",
    polarity: Polarity = "affirmative",
):
    verbs = load_verbs()

    if not use_irregular:
        verbs = [verb for verb in verbs if not is_irregular(verb["spanish"], mood, tense)]

    verb = random.choice(verbs)
    if tense == "imperative":
        pronoun_index = random.choice(IMPERATIVE_INDICES if use_vosotros else IMPERATIVE_NON_VOSOTROS_INDICES)
        pronoun_spanish = IMPERATIVE_PRONOUNS_SPANISH[pronoun_index]
        pronoun_english = IMPERATIVE_PRONOUNS_ENGLISH[pronoun_index]
    else:
        pronoun_index = random.choice(ALL_INDICES if use_vosotros else NON_VOSOTROS_INDICES)
        pronoun_spanish = PRONOUNS[pronoun_index]
        pronoun_english = PRONOUNS_ENGLISH[pronoun_index]

    form_spanish = conjugate_by_tense_mood(verb["spanish"], pronoun_index, mood, tense, polarity)
    form_spanish_alt = imperfect_subjunctive_alt_form(verb["spanish"], pronoun_index, mood, tense)
    form_english = conjugate_english(verb["english"], pronoun_index, tense, polarity)

    return [{
        "infinitive_spanish": verb["spanish"],
        "infinitive_english": verb["english"],
        "mood_english": mood,
        "mood_spanish": "subjuntivo" if mood == "subjunctive" else "indicativo",
        "tense_english": tense,
        "tense_spanish": {
            "preterite": "pretérito",
            "imperfect": "imperfecto",
            "perfect": "perfecto",
            "future": "futuro",
            "future_perfect": "futuro perfecto",
            "conditional": "condicional",
            "conditional_perfect": "condicional perfecto",
            "imperative": "imperativo",
        }.get(tense, "presente"),
        "polarity_english": polarity,
        "polarity_spanish": "negativo" if polarity == "negative" else "afirmativo",
        "pronoun_spanish": pronoun_spanish,
        "pronoun_english": pronoun_english,
        "form_spanish": form_spanish,
        "form_spanish_alt": form_spanish_alt,
        "form_english": form_english,
    }]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

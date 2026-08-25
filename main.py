import json
import random
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from languages.spanish.present_indicative_rules import IRREGULAR_VERBS, STEM_CHANGES, PRONOUNS, conjugate
from languages.spanish.present_subjunctive_rules import (
    IRREGULAR_SUBJUNCTIVE,
    SUBJUNCTIVE_STEM_OVERRIDES,
    conjugate_subjunctive,
)
from languages.spanish.preterite_indicative_rules import (
    IRREGULAR_VERBS as PRETERITE_IRREGULAR_VERBS,
    STRONG_STEMS as PRETERITE_STRONG_STEMS,
    IR_STEM_CHANGES as PRETERITE_IR_STEM_CHANGES,
    I_TO_Y_VERBS as PRETERITE_I_TO_Y_VERBS,
    conjugate_preterite,
)
from languages.english.present_indicative_rules import conjugate_present
from languages.english.preterite_indicative_rules import conjugate_past

Mood = Literal["indicative", "subjunctive"]
Tense = Literal["present", "preterite"]

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


def load_verbs():
    with open(VERBS_FILE, encoding="utf-8") as f:
        return json.load(f)


def is_irregular(verb: str, mood: Mood, tense: Tense) -> bool:
    if tense == "preterite":
        return (
            verb in PRETERITE_IRREGULAR_VERBS
            or verb in PRETERITE_STRONG_STEMS
            or verb in PRETERITE_IR_STEM_CHANGES
            or verb in PRETERITE_I_TO_Y_VERBS
        )
    if mood == "subjunctive":
        return (
            verb in IRREGULAR_SUBJUNCTIVE
            or verb in SUBJUNCTIVE_STEM_OVERRIDES
            or verb in STEM_CHANGES
        )
    return verb in IRREGULAR_VERBS or verb in STEM_CHANGES


def conjugate_by_tense_mood(verb: str, pronoun_index: int, mood: Mood, tense: Tense) -> str:
    if tense == "preterite":
        if mood == "subjunctive":
            raise HTTPException(
                status_code=422,
                detail="Preterite subjunctive is not supported.",
            )
        return conjugate_preterite(verb, pronoun_index)
    if mood == "subjunctive":
        return conjugate_subjunctive(verb, pronoun_index)
    return conjugate(verb, pronoun_index)


def conjugate_english(infinitive_english: str, pronoun_index: int, tense: Tense) -> str:
    if tense == "preterite":
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

    conjugations = [
        {
            "pronoun_spanish": PRONOUNS[i],
            "pronoun_english": PRONOUNS_ENGLISH[i],
            "form_spanish": conjugate_by_tense_mood(verb_entry["spanish"], i, mood, tense),
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
):
    verbs = load_verbs()

    if not use_irregular:
        verbs = [verb for verb in verbs if not is_irregular(verb["spanish"], mood, tense)]

    verb = random.choice(verbs)
    pronoun_index = random.choice(ALL_INDICES if use_vosotros else NON_VOSOTROS_INDICES)

    form_spanish = conjugate_by_tense_mood(verb["spanish"], pronoun_index, mood, tense)
    form_english = conjugate_english(verb["english"], pronoun_index, tense)

    return [{
        "infinitive_spanish": verb["spanish"],
        "infinitive_english": verb["english"],
        "mood_english": mood,
        "mood_spanish": "subjuntivo" if mood == "subjunctive" else "indicativo",
        "tense_english": tense,
        "tense_spanish": "pretérito" if tense == "preterite" else "presente",
        "pronoun_spanish": PRONOUNS[pronoun_index],
        "pronoun_english": PRONOUNS_ENGLISH[pronoun_index],
        "form_spanish": form_spanish,
        "form_english": form_english,
    }]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

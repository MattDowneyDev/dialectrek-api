import json
import random
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from conjugation import (
    ALL_INDICES,
    IMPERATIVE_INDICES,
    IMPERATIVE_NON_VOSOTROS_INDICES,
    IMPERATIVE_PRONOUNS_ENGLISH,
    IMPERATIVE_PRONOUNS_SPANISH,
    NON_VOSOTROS_INDICES,
    PRONOUNS,
    PRONOUNS_ENGLISH,
    Mood,
    Polarity,
    Tense,
    conjugate_by_tense_mood,
    conjugate_english,
    conjugate_imperative_english,
    conjugate_imperative_spanish,
    is_irregular,
    subjunctive_ra_se_alt_form,
)
from models import (
    ImperativeVerbConjugationResponse,
    RandomConjugationRow,
    VerbConjugationResponse,
)

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


def load_verbs():
    with open(VERBS_FILE, encoding="utf-8") as f:
        return json.load(f)


@app.get("/get-all-verbs", response_model=list[tuple[str, str]])
def get_all_verbs():
    verbs = load_verbs()
    verbs_list = [[verb["spanish"], verb["english"]] for verb in verbs]
    verbs_list.sort()
    return verbs_list


@app.get(
    "/get-verb-conjugation",
    response_model=Union[VerbConjugationResponse, ImperativeVerbConjugationResponse],
)
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
                "form_spanish_alt": subjunctive_ra_se_alt_form(verb_entry["spanish"], i, mood, tense),
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


@app.get("/get-random-verb-conjugation", response_model=list[RandomConjugationRow])
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
    form_spanish_alt = subjunctive_ra_se_alt_form(verb["spanish"], pronoun_index, mood, tense)
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
            "preterite_perfect": "pretérito anterior",
            "pluperfect": "pluscuamperfecto",
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

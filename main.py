import json
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from languages.spanish.rules import IRREGULAR_VERBS, STEM_CHANGES, PRONOUNS, conjugate

app = FastAPI()

origins = [
    "http://localhost:3000",
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


def is_irregular(verb: str) -> bool:
    return verb in IRREGULAR_VERBS or verb in STEM_CHANGES


def conjugate_english(infinitive_english: str, pronoun_index: int) -> str:
    """Naive present-tense English conjugation, used only for display."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]
    if pronoun_index != 2:
        return base
    if base.endswith(("o", "ch", "sh", "x", "z", "s")):
        return base + "es"
    if base.endswith("y") and base[-2:-1] not in "aeiou":
        return base[:-1] + "ies"
    return base + "s"


@app.get("/get-all-verbs")
def get_all_verbs():
    verbs = load_verbs()
    verbs_list = [[verb["spanish"], verb["english"]] for verb in verbs]
    verbs_list.sort()
    return verbs_list


@app.get("/get-random-verb-conjugation")
def get_random_verb_conjugation(use_irregular: bool, use_vosotros: bool):
    verbs = load_verbs()

    if not use_irregular:
        verbs = [verb for verb in verbs if not is_irregular(verb["spanish"])]

    verb = random.choice(verbs)
    pronoun_index = random.choice(ALL_INDICES if use_vosotros else NON_VOSOTROS_INDICES)

    form_spanish = conjugate(verb["spanish"], pronoun_index)
    form_english = conjugate_english(verb["english"], pronoun_index)

    return [{
        "infinitive_spanish": verb["spanish"],
        "infinitive_english": verb["english"],
        "mood_english": "indicative",
        "mood_spanish": "indicativo",
        "tense_english": "present",
        "tense_spanish": "presente",
        "pronoun_spanish": PRONOUNS[pronoun_index],
        "pronoun_english": PRONOUNS_ENGLISH[pronoun_index],
        "form_spanish": form_spanish,
        "form_english": form_english,
    }]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

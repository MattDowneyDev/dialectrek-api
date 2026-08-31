import json
import random
import unicodedata
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from conjugation import Mood, Polarity, Tense
from languages.registry import LanguageConfig, get_language
from models import (
    ImperativeVerbConjugationResponse,
    RandomConjugationRow,
    RandomWord,
    VerbConjugationResponse,
)

app = FastAPI(title="DialecTrek API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://dialectrek.com",
    "https://www.dialectrek.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def alphabetic_sort_key(word: str) -> tuple[str, str]:
    # plain code-point sort puts accented letters (e.g. é) after z, so fold
    # accents to their base letter for ordering and keep the original as a
    # tiebreaker
    folded = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode("ascii")
    return (folded.lower(), word)


def load_verbs(config: LanguageConfig):
    with open(config.verbs_file, encoding="utf-8") as f:
        return json.load(f)


def load_words(config: LanguageConfig):
    with open(config.words_file, encoding="utf-8") as f:
        return json.load(f)


@app.get("/{language}/get-all-verbs", response_model=list[tuple[str, str]])
def get_all_verbs(language: str):
    config = get_language(language)
    if not config.has_verbs:
        raise HTTPException(status_code=404, detail=f"Verbs not available yet for '{language}'")
    verbs = load_verbs(config)
    verbs_list = [[verb[config.target_key], verb[config.source_key]] for verb in verbs]
    verbs_list.sort(key=lambda pair: alphabetic_sort_key(pair[0]))
    return verbs_list


@app.get(
    "/{language}/get-verb-conjugation",
    response_model=Union[VerbConjugationResponse, ImperativeVerbConjugationResponse],
)
def get_verb_conjugation(
    language: str, verb: str, mood: Mood = "indicative", tense: Tense = "present"
):
    config = get_language(language)
    if not config.has_verbs:
        raise HTTPException(status_code=404, detail=f"Verbs not available yet for '{language}'")
    verbs = load_verbs(config)
    verb_entry = next((v for v in verbs if v[config.target_key] == verb), None)

    if verb_entry is None:
        raise HTTPException(status_code=404, detail=f"Verb '{verb}' not found")

    if tense == "imperative":
        # The imperative has no single "mood"-like axis the way other
        # tenses do -- affirmative and negative are both worth seeing
        # side by side on the same row, so this shape carries both
        # instead of picking one via a query parameter.
        conjugations = [
            {
                "pronoun_target": config.imperative_pronouns[i],
                "pronoun_english": config.imperative_pronouns_english[i],
                "form_target_affirmative": config.conjugate_imperative(
                    verb_entry[config.target_key], i, "affirmative"
                ),
                "form_target_negative": config.conjugate_imperative(
                    verb_entry[config.target_key], i, "negative"
                ),
                "form_english_affirmative": config.conjugate_imperative_english(
                    verb_entry[config.source_key], i, "affirmative"
                ),
                "form_english_negative": config.conjugate_imperative_english(
                    verb_entry[config.source_key], i, "negative"
                ),
            }
            for i in config.imperative_indices
        ]
    else:
        conjugations = [
            {
                "pronoun_target": config.pronouns[i],
                "pronoun_english": config.pronouns_english[i],
                "form_target": config.conjugate(verb_entry[config.target_key], i, mood, tense),
                "form_target_alt": config.subjunctive_alt_form(
                    verb_entry[config.target_key], i, mood, tense
                ),
                "form_english": config.conjugate_english(verb_entry[config.source_key], i, tense),
            }
            for i in config.all_indices
        ]

    return {
        "infinitive_target": verb_entry[config.target_key],
        "infinitive_english": verb_entry[config.source_key],
        "mood": mood,
        "tense": tense,
        "conjugations": conjugations,
    }


@app.get("/{language}/get-random-verb-conjugation", response_model=list[RandomConjugationRow])
def get_random_verb_conjugation(
    language: str,
    use_irregular: bool,
    # only Spanish's setup wizard asks the vosotros question and sends
    # this -- everyone else needs a default here or their requests 422
    use_regional_variant: bool = False,
    mood: Mood = "indicative",
    tense: Tense = "present",
    polarity: Polarity = "affirmative",
):
    config = get_language(language)
    if not config.has_verbs:
        raise HTTPException(status_code=404, detail=f"Verbs not available yet for '{language}'")
    verbs = load_verbs(config)

    if not use_irregular:
        verbs = [
            verb for verb in verbs if not config.is_irregular(verb[config.target_key], mood, tense)
        ]

    verb = random.choice(verbs)
    if tense == "imperative":
        pronoun_index = random.choice(
            config.imperative_indices
            if use_regional_variant
            else config.imperative_non_regional_indices
        )
        pronoun_target = config.imperative_pronouns[pronoun_index]
        pronoun_english = config.imperative_pronouns_english[pronoun_index]
    else:
        pronoun_index = random.choice(
            config.all_indices if use_regional_variant else config.non_regional_indices
        )
        pronoun_target = config.pronouns[pronoun_index]
        pronoun_english = config.pronouns_english[pronoun_index]

    form_target = config.conjugate(verb[config.target_key], pronoun_index, mood, tense, polarity)
    form_target_alt = config.subjunctive_alt_form(verb[config.target_key], pronoun_index, mood, tense)
    form_english = config.conjugate_english(verb[config.source_key], pronoun_index, tense, polarity)

    return [{
        "infinitive_target": verb[config.target_key],
        "infinitive_english": verb[config.source_key],
        "mood": mood,
        "tense": tense,
        "polarity": polarity,
        "pronoun_target": pronoun_target,
        "pronoun_english": pronoun_english,
        "form_target": form_target,
        "form_target_alt": form_target_alt,
        "form_english": form_english,
    }]


@app.get("/{language}/get-word-categories", response_model=list[str])
def get_word_categories(language: str):
    config = get_language(language)
    words = load_words(config)
    return sorted({word["category"] for word in words})


@app.get("/{language}/get-random-word", response_model=RandomWord)
def get_random_word(language: str, category: str | None = None):
    config = get_language(language)
    words = load_words(config)
    if category is not None:
        words = [word for word in words if word["category"] == category]
        if not words:
            raise HTTPException(status_code=404, detail="No words found for category")
    word = random.choice(words)

    return {
        "rank": word["rank"],
        "word_target": word[config.target_key],
        "word_english": word[config.source_key],
        "category": word["category"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

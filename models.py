from typing import Optional

from pydantic import BaseModel

from conjugation import Mood, Polarity, Tense


class ConjugationRow(BaseModel):
    pronoun_target: str
    pronoun_english: str
    form_target: str
    form_target_alt: Optional[str]
    form_english: str


class ImperativeConjugationRow(BaseModel):
    pronoun_target: str
    pronoun_english: str
    form_target_affirmative: str
    form_target_negative: str
    form_english_affirmative: str
    form_english_negative: str


class VerbConjugationResponse(BaseModel):
    infinitive_target: str
    infinitive_english: str
    mood: Mood
    tense: Tense
    conjugations: list[ConjugationRow]


class ImperativeVerbConjugationResponse(BaseModel):
    infinitive_target: str
    infinitive_english: str
    mood: Mood
    tense: Tense
    conjugations: list[ImperativeConjugationRow]


class RandomConjugationRow(BaseModel):
    infinitive_target: str
    infinitive_english: str
    mood: Mood
    tense: Tense
    polarity: Polarity
    pronoun_target: str
    pronoun_english: str
    form_target: str
    form_target_alt: Optional[str]
    form_english: str

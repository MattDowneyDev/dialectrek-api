from typing import Optional

from pydantic import BaseModel

from conjugation import Mood, Polarity, Tense


class RandomVerbCriteria(BaseModel):
    use_irregular: bool
    use_vosotros: bool


class ConjugationRow(BaseModel):
    pronoun_spanish: str
    pronoun_english: str
    form_spanish: str
    form_spanish_alt: Optional[str]
    form_english: str


class ImperativeConjugationRow(BaseModel):
    pronoun_spanish: str
    pronoun_english: str
    form_spanish_affirmative: str
    form_spanish_negative: str
    form_english_affirmative: str
    form_english_negative: str


class VerbConjugationResponse(BaseModel):
    infinitive_spanish: str
    infinitive_english: str
    mood_english: Mood
    tense_english: Tense
    conjugations: list[ConjugationRow]


class ImperativeVerbConjugationResponse(BaseModel):
    infinitive_spanish: str
    infinitive_english: str
    mood_english: Mood
    tense_english: Tense
    conjugations: list[ImperativeConjugationRow]


class RandomConjugationRow(BaseModel):
    infinitive_spanish: str
    infinitive_english: str
    mood_english: Mood
    mood_spanish: str
    tense_english: Tense
    tense_spanish: str
    polarity_english: Polarity
    polarity_spanish: str
    pronoun_spanish: str
    pronoun_english: str
    form_spanish: str
    form_spanish_alt: Optional[str]
    form_english: str

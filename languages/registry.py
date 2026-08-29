"""Per-language configuration registry. main.py resolves a `{language}`
path segment to a LanguageConfig here instead of hardcoding a single
target language's engine, constants, and verb data.

Adding a new target language later means adding one LanguageConfig
entry to LANGUAGES (plus its own languages/<name>/ engine + verbs.json)
-- no changes to main.py's route handlers themselves.
"""

from dataclasses import dataclass
from typing import Callable, Optional

from fastapi import HTTPException

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


@dataclass
class LanguageConfig:
    code: str
    verbs_file: str
    words_file: str
    target_key: str
    source_key: str
    pronouns: list[str]
    pronouns_english: list[str]
    imperative_pronouns: list[str]
    imperative_pronouns_english: list[str]
    all_indices: list[int]
    non_regional_indices: list[int]
    imperative_indices: list[int]
    imperative_non_regional_indices: list[int]
    conjugate: Callable[[str, int, Mood, Tense, Polarity], str]
    conjugate_imperative: Callable[[str, int, Polarity], str]
    conjugate_english: Callable[[str, int, Tense, Polarity], str]
    conjugate_imperative_english: Callable[[str, int, Polarity], str]
    is_irregular: Callable[[str, Mood, Tense], bool]
    subjunctive_alt_form: Callable[[str, int, Mood, Tense], Optional[str]]


LANGUAGES: dict[str, LanguageConfig] = {
    "es": LanguageConfig(
        code="es",
        verbs_file="./languages/spanish/verbs.json",
        words_file="./languages/spanish/words.json",
        target_key="spanish",
        source_key="english",
        pronouns=PRONOUNS,
        pronouns_english=PRONOUNS_ENGLISH,
        imperative_pronouns=IMPERATIVE_PRONOUNS_SPANISH,
        imperative_pronouns_english=IMPERATIVE_PRONOUNS_ENGLISH,
        all_indices=ALL_INDICES,
        non_regional_indices=NON_VOSOTROS_INDICES,
        imperative_indices=IMPERATIVE_INDICES,
        imperative_non_regional_indices=IMPERATIVE_NON_VOSOTROS_INDICES,
        conjugate=conjugate_by_tense_mood,
        conjugate_imperative=conjugate_imperative_spanish,
        conjugate_english=conjugate_english,
        conjugate_imperative_english=conjugate_imperative_english,
        is_irregular=is_irregular,
        subjunctive_alt_form=subjunctive_ra_se_alt_form,
    ),
}


def get_language(code: str) -> LanguageConfig:
    config = LANGUAGES.get(code)
    if config is None:
        raise HTTPException(status_code=404, detail=f"Unsupported language '{code}'")
    return config

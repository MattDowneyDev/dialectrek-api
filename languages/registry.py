"""Per-language configuration registry. main.py resolves a `{language}`
path segment to a LanguageConfig here instead of hardcoding a single
target language's engine, constants, and verb data.

Adding a new target language later means adding one LanguageConfig
entry to LANGUAGES (plus its own languages/<name>/ engine + verbs.json)
-- no changes to main.py's route handlers themselves.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

from fastapi import HTTPException

from conjugation import (
    ALL_INDICES,
    FRENCH_IMPERATIVE_INDICES,
    FRENCH_IMPERATIVE_PRONOUNS,
    FRENCH_IMPERATIVE_PRONOUNS_ENGLISH,
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
    conjugate_french,
    conjugate_imperative_english,
    conjugate_imperative_french,
    conjugate_imperative_spanish,
    is_irregular,
    is_irregular_french,
    no_subjunctive_alt_form,
    subjunctive_ra_se_alt_form,
)
from languages.french.common import (
    PRONOUNS as FRENCH_PRONOUNS,
    PRONOUNS_ENGLISH as FRENCH_PRONOUNS_ENGLISH,
)


@dataclass
class LanguageConfig:
    code: str
    words_file: str
    target_key: str
    source_key: str
    # Verb conjugation isn't built out for every language yet (each one
    # needs its own rule engine, see conjugation.py) -- a language with
    # only `words_file` set supports flashcards but not the verbs/conjugate
    # routes, which check `has_verbs` before touching the fields below.
    verbs_file: Optional[str] = None
    pronouns: list[str] = field(default_factory=list)
    pronouns_english: list[str] = field(default_factory=list)
    imperative_pronouns: list[str] = field(default_factory=list)
    imperative_pronouns_english: list[str] = field(default_factory=list)
    all_indices: list[int] = field(default_factory=list)
    non_regional_indices: list[int] = field(default_factory=list)
    imperative_indices: list[int] = field(default_factory=list)
    imperative_non_regional_indices: list[int] = field(default_factory=list)
    conjugate: Optional[Callable[[str, int, Mood, Tense, Polarity], str]] = None
    conjugate_imperative: Optional[Callable[[str, int, Polarity], str]] = None
    conjugate_english: Optional[Callable[[str, int, Tense, Polarity], str]] = None
    conjugate_imperative_english: Optional[Callable[[str, int, Polarity], str]] = None
    is_irregular: Optional[Callable[[str, Mood, Tense], bool]] = None
    subjunctive_alt_form: Optional[Callable[[str, int, Mood, Tense], Optional[str]]] = None

    @property
    def has_verbs(self) -> bool:
        return self.verbs_file is not None


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
    "fr": LanguageConfig(
        code="fr",
        verbs_file="./languages/french/verbs.json",
        words_file="./languages/french/words.json",
        target_key="french",
        source_key="english",
        pronouns=FRENCH_PRONOUNS,
        pronouns_english=FRENCH_PRONOUNS_ENGLISH,
        imperative_pronouns=FRENCH_IMPERATIVE_PRONOUNS,
        imperative_pronouns_english=FRENCH_IMPERATIVE_PRONOUNS_ENGLISH,
        all_indices=ALL_INDICES,
        non_regional_indices=ALL_INDICES,
        imperative_indices=FRENCH_IMPERATIVE_INDICES,
        imperative_non_regional_indices=FRENCH_IMPERATIVE_INDICES,
        conjugate=conjugate_french,
        conjugate_imperative=conjugate_imperative_french,
        conjugate_english=conjugate_english,
        conjugate_imperative_english=conjugate_imperative_english,
        is_irregular=is_irregular_french,
        subjunctive_alt_form=no_subjunctive_alt_form,
    ),
}


def get_language(code: str) -> LanguageConfig:
    config = LANGUAGES.get(code)
    if config is None:
        raise HTTPException(status_code=404, detail=f"Unsupported language '{code}'")
    return config

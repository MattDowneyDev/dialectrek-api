import pytest
from pydantic import ValidationError

from models import (
    ConjugationRow,
    ImperativeConjugationRow,
    ImperativeVerbConjugationResponse,
    RandomConjugationRow,
    RandomWord,
    VerbConjugationResponse,
)

VALID_ROW = dict(
    pronoun_target="yo",
    pronoun_english="I",
    form_target="hablo",
    form_target_alt=None,
    form_english="speak",
)


def test_conjugation_row_accepts_none_for_optional_alt_form():
    row = ConjugationRow(**VALID_ROW)
    assert row.form_target_alt is None


def test_conjugation_row_requires_all_non_optional_fields():
    incomplete = {k: v for k, v in VALID_ROW.items() if k != "form_target"}
    with pytest.raises(ValidationError):
        ConjugationRow(**incomplete)


def test_verb_conjugation_response_validates_mood_and_tense_literals():
    response = VerbConjugationResponse(
        infinitive_target="hablar",
        infinitive_english="to speak",
        mood="indicative",
        tense="present",
        conjugations=[ConjugationRow(**VALID_ROW)],
    )
    assert response.mood == "indicative"
    assert response.conjugations[0].pronoun_target == "yo"


def test_verb_conjugation_response_rejects_invalid_mood():
    with pytest.raises(ValidationError):
        VerbConjugationResponse(
            infinitive_target="hablar",
            infinitive_english="to speak",
            mood="not-a-real-mood",
            tense="present",
            conjugations=[],
        )


def test_imperative_conjugation_row_requires_affirmative_and_negative_forms():
    row = ImperativeConjugationRow(
        pronoun_target="tú",
        pronoun_english="you",
        form_target_affirmative="habla",
        form_target_negative="no hables",
        form_english_affirmative="speak",
        form_english_negative="don't speak",
    )
    assert row.form_target_affirmative == "habla"

    incomplete = {
        "pronoun_target": "tú",
        "pronoun_english": "you",
        "form_target_affirmative": "habla",
    }
    with pytest.raises(ValidationError):
        ImperativeConjugationRow(**incomplete)


def test_imperative_verb_conjugation_response():
    response = ImperativeVerbConjugationResponse(
        infinitive_target="hablar",
        infinitive_english="to speak",
        mood="indicative",
        tense="imperative",
        conjugations=[],
    )
    assert response.conjugations == []


def test_random_word_requires_int_rank():
    with pytest.raises(ValidationError):
        RandomWord(rank="not-an-int", word_target="hola", word_english="hello", category="greeting")

    word = RandomWord(rank=1, word_target="hola", word_english="hello", category="greeting")
    assert word.rank == 1


def test_random_conjugation_row_validates_polarity_literal():
    row = RandomConjugationRow(
        infinitive_target="hablar",
        infinitive_english="to speak",
        mood="indicative",
        tense="present",
        polarity="affirmative",
        **VALID_ROW,
    )
    assert row.polarity == "affirmative"

    with pytest.raises(ValidationError):
        RandomConjugationRow(
            infinitive_target="hablar",
            infinitive_english="to speak",
            mood="indicative",
            tense="present",
            polarity="not-a-polarity",
            **VALID_ROW,
        )

import pytest
from fastapi import HTTPException

from languages.registry import LANGUAGES, get_language


def test_get_language_returns_matching_config():
    assert get_language("es") is LANGUAGES["es"]
    assert get_language("fr") is LANGUAGES["fr"]


def test_get_language_unsupported_code_raises_404():
    with pytest.raises(HTTPException) as exc_info:
        get_language("de")
    assert exc_info.value.status_code == 404


def test_has_verbs_reflects_verbs_file_presence():
    assert LANGUAGES["es"].has_verbs is True
    assert LANGUAGES["fr"].has_verbs is True


@pytest.mark.parametrize("code", ["es", "fr"])
def test_language_config_callables_are_wired_and_runnable(code):
    config = LANGUAGES[code]
    verb = "hablar" if code == "es" else "parler"
    infinitive_english = "to speak"

    assert isinstance(config.conjugate(verb, 0, "indicative", "present"), str)
    assert isinstance(config.conjugate_imperative(verb, 1, "affirmative"), str)
    assert isinstance(config.conjugate_english(infinitive_english, 0, "present"), str)
    assert isinstance(config.conjugate_imperative_english(infinitive_english, 1, "affirmative"), str)
    assert isinstance(config.is_irregular(verb, "indicative", "present"), bool)
    # subjunctive_alt_form may legitimately return None (French always does)
    config.subjunctive_alt_form(verb, 0, "subjunctive", "present")


def test_spanish_and_french_pronoun_index_lists_are_configured():
    es = LANGUAGES["es"]
    fr = LANGUAGES["fr"]

    assert es.all_indices == [0, 1, 2, 3, 4, 5]
    assert es.non_regional_indices == [0, 1, 2, 3, 5]  # excludes vosotros
    assert fr.non_regional_indices == fr.all_indices  # French has no vosotros distinction

    assert 0 not in es.imperative_indices  # no "yo" command form
    assert 0 not in fr.imperative_indices

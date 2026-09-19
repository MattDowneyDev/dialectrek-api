import pytest

from languages.spanish.common import (
    PRONOUNS,
    PRESENT_STEM_CHANGE_MAP,
    PRESENT_STEM_CHANGES,
    apply_present_stem_change,
    replace_last,
)


def test_pronouns_has_six_entries_in_conjugation_order():
    assert PRONOUNS == ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ustedes"]


class TestReplaceLast:
    def test_replaces_last_occurrence_only(self):
        assert replace_last("hablar", "a", "e") == "habler"

    def test_no_match_returns_stem_unchanged(self):
        assert replace_last("xyz", "a", "b") == "xyz"

    def test_replacement_can_be_multiple_characters(self):
        assert replace_last("pens", "e", "ie") == "piens"

    def test_empty_stem_returns_unchanged(self):
        assert replace_last("", "a", "b") == ""


class TestApplyPresentStemChange:
    @pytest.mark.parametrize(
        "change_type,stem,expected",
        [
            ("e_ie", "pens", "piens"),
            ("o_ue", "cont", "cuent"),
            ("e_i", "ped", "pid"),
            ("u_ue", "jug", "jueg"),
        ],
    )
    def test_applies_correct_vowel_swap(self, change_type, stem, expected):
        assert apply_present_stem_change(stem, change_type) == expected

    def test_uses_the_shared_change_map(self):
        for change_type, (old, new) in PRESENT_STEM_CHANGE_MAP.items():
            stem = f"x{old}y"
            assert apply_present_stem_change(stem, change_type) == f"x{new}y"


def test_present_stem_changes_only_uses_known_change_types():
    for verb, change_type in PRESENT_STEM_CHANGES.items():
        assert change_type in PRESENT_STEM_CHANGE_MAP

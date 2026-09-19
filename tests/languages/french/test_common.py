import pytest

from languages.french.common import (
    ELIDABLE_STARTS,
    PRONOUNS,
    PRONOUNS_ENGLISH,
    REFLEXIVE_PRONOUNS,
    reflexive_pronoun,
    replace_last,
    strip_reflexive,
)


def test_pronoun_lists_are_aligned_and_six_long():
    assert len(PRONOUNS) == 6
    assert len(PRONOUNS_ENGLISH) == 6
    assert len(REFLEXIVE_PRONOUNS) == 6


class TestReplaceLast:
    def test_replaces_rightmost_occurrence_only(self):
        assert replace_last("achetachet", "e", "è") == "achetachèt"

    def test_single_occurrence(self):
        assert replace_last("lev", "e", "è") == "lèv"

    def test_no_occurrence_returns_unchanged(self):
        assert replace_last("boiv", "e", "è") == "boiv"

    def test_multi_char_old_and_new(self):
        assert replace_last("interpret", "et", "èt") == "interprèt"


class TestStripReflexive:
    @pytest.mark.parametrize(
        "verb,expected_base",
        [
            ("se lever", "lever"),
            ("se reposer", "reposer"),
            ("se réveiller", "réveiller"),
            ("s'habiller", "habiller"),
            ("s'inquiéter", "inquiéter"),
        ],
    )
    def test_strips_reflexive_marker(self, verb, expected_base):
        assert strip_reflexive(verb) == (expected_base, True)

    @pytest.mark.parametrize("verb", ["parler", "finir", "attendre", "être"])
    def test_non_reflexive_passes_through_unchanged(self, verb):
        assert strip_reflexive(verb) == (verb, False)


class TestReflexivePronoun:
    @pytest.mark.parametrize("pronoun_index,form", [(0, "lève"), (1, "lèves"), (2, "lève")])
    def test_me_te_se_stay_unelided_before_consonant(self, pronoun_index, form):
        result = reflexive_pronoun(pronoun_index, form)
        assert result[-1] == " "
        assert "'" not in result

    @pytest.mark.parametrize(
        "pronoun_index,expected_prefix",
        [(0, "m'"), (1, "t'"), (2, "s'"), (5, "s'")],
    )
    def test_me_te_se_elide_before_vowel(self, pronoun_index, expected_prefix):
        assert reflexive_pronoun(pronoun_index, "habille") == expected_prefix

    def test_elides_before_mute_h(self):
        assert reflexive_pronoun(0, "habitue") == "m'"

    @pytest.mark.parametrize("letter", sorted(ELIDABLE_STARTS))
    def test_elides_before_every_registered_vowel_sound(self, letter):
        assert reflexive_pronoun(0, letter + "x") == "m'"

    def test_nous_and_vous_never_elide(self):
        assert reflexive_pronoun(3, "habillons") == "nous "
        assert reflexive_pronoun(4, "habillez") == "vous "

    def test_uppercase_conjugated_form_still_checked_case_insensitively(self):
        assert reflexive_pronoun(0, "Habille") == "m'"

import pytest

from languages.english.present_indicative_rules import (
    BE_PRESENT_FORMS,
    IRREGULAR_THIRD_PERSON,
    conjugate_present,
    conjugate_third_person_word,
)


class TestConjugateThirdPersonWord:
    @pytest.mark.parametrize("verb,expected", list(IRREGULAR_THIRD_PERSON.items()))
    def test_irregular_third_person_dict(self, verb, expected):
        assert conjugate_third_person_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("go", "goes"),
            ("do", "does"),
            ("watch", "watches"),
            ("wash", "washes"),
            ("fix", "fixes"),
            ("buzz", "buzzes"),
            ("kiss", "kisses"),
        ],
    )
    def test_es_ending_after_sibilant_or_o(self, verb, expected):
        assert conjugate_third_person_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("study", "studies"),
            ("try", "tries"),
            ("carry", "carries"),
        ],
    )
    def test_y_to_ies_after_consonant(self, verb, expected):
        assert conjugate_third_person_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("play", "plays"),
            ("stay", "stays"),
        ],
    )
    def test_y_after_vowel_just_adds_s(self, verb, expected):
        assert conjugate_third_person_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("walk", "walks"),
            ("eat", "eats"),
            ("speak", "speaks"),
            ("take", "takes"),
        ],
    )
    def test_default_adds_s(self, verb, expected):
        assert conjugate_third_person_word(verb) == expected


class TestConjugatePresent:
    @pytest.mark.parametrize("pronoun_index,expected", enumerate(BE_PRESENT_FORMS))
    def test_be_varies_by_every_person(self, pronoun_index, expected):
        assert conjugate_present("to be", pronoun_index) == expected

    def test_be_able_to_composes_rest(self):
        assert conjugate_present("to be able to", 0) == "am able to"
        assert conjugate_present("to be able to", 2) == "is able to"
        assert conjugate_present("to be able to", 5) == "are able to"

    def test_be_born(self):
        assert conjugate_present("to be born", 0) == "am born"
        assert conjugate_present("to be born", 2) == "is born"

    @pytest.mark.parametrize("pronoun_index", [0, 1, 3, 4, 5])
    def test_non_third_person_returns_bare_infinitive(self, pronoun_index):
        assert conjugate_present("to eat", pronoun_index) == "eat"
        assert conjugate_present("to go out", pronoun_index) == "go out"

    def test_third_person_singular_regular_verb(self):
        assert conjugate_present("to eat", 2) == "eats"

    def test_third_person_singular_irregular_have(self):
        assert conjugate_present("to have", 2) == "has"

    def test_third_person_singular_go_and_do(self):
        assert conjugate_present("to go", 2) == "goes"
        assert conjugate_present("to do", 2) == "does"

    def test_third_person_singular_y_ending(self):
        assert conjugate_present("to study", 2) == "studies"

    def test_phrasal_verb_only_conjugates_first_word(self):
        assert conjugate_present("to go out", 2) == "goes out"
        assert conjugate_present("to look for", 2) == "looks for"
        assert conjugate_present("to ask for", 2) == "asks for"
        assert conjugate_present("to take out", 2) == "takes out"
        assert conjugate_present("to turn out", 2) == "turns out"

    def test_multi_translation_takes_first_slash_option(self):
        assert conjugate_present("to get up/raise", 2) == "gets up"
        assert conjugate_present("to get up/raise", 0) == "get up"

    def test_infinitive_without_to_prefix_still_works(self):
        assert conjugate_present("eat", 2) == "eats"

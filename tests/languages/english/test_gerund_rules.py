import pytest

from languages.english.gerund_rules import (
    BE_GERUND,
    DOUBLED_CONSONANT_GERUNDS,
    conjugate_gerund_word,
)


class TestConjugateGerundWord:
    def test_be_is_irregular(self):
        assert conjugate_gerund_word("be") == BE_GERUND == "being"

    @pytest.mark.parametrize("verb,expected", list(DOUBLED_CONSONANT_GERUNDS.items()))
    def test_doubled_consonant_dict(self, verb, expected):
        assert conjugate_gerund_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("see", "seeing"),
            ("agree", "agreeing"),
        ],
    )
    def test_double_e_ending_not_treated_as_silent_e(self, verb, expected):
        assert conjugate_gerund_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("die", "dying"),
            ("lie", "lying"),
            ("tie", "tying"),
        ],
    )
    def test_ie_ending_becomes_ying(self, verb, expected):
        assert conjugate_gerund_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("write", "writing"),
            ("come", "coming"),
            ("have", "having"),
            ("give", "giving"),
            ("lose", "losing"),
            ("take", "taking"),
        ],
    )
    def test_silent_e_dropped(self, verb, expected):
        assert conjugate_gerund_word(verb) == expected

    @pytest.mark.parametrize(
        "verb,expected",
        [
            ("walk", "walking"),
            ("study", "studying"),
            ("bring", "bringing"),
            ("do", "doing"),
            ("fall", "falling"),
            ("find", "finding"),
            ("go", "going"),
            ("hear", "hearing"),
            ("know", "knowing"),
            ("pay", "paying"),
            ("read", "reading"),
            ("say", "saying"),
            ("speak", "speaking"),
            ("understand", "understanding"),
        ],
    )
    def test_default_adds_ing(self, verb, expected):
        assert conjugate_gerund_word(verb) == expected

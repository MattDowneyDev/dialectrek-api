import pytest

from languages.spanish.present_perfect_indicative_rules import (
    conjugate_present_perfect_indicative,
)


class TestRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "he hablado"),
            ("comer", 1, "has comido"),
            ("vivir", 2, "ha vivido"),
            ("hacer", 3, "hemos hecho"),
            ("decir", 4, "habéis dicho"),
            ("ver", 5, "han visto"),
            ("volver", 0, "he vuelto"),
            ("leer", 0, "he leído"),
        ],
    )
    def test_present_perfect_form(self, verb, pronoun_index, expected):
        assert conjugate_present_perfect_indicative(verb, pronoun_index) == expected

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_present_perfect_indicative("hablar", i) for i in range(6)]
        assert forms == [
            "he hablado",
            "has hablado",
            "ha hablado",
            "hemos hablado",
            "habéis hablado",
            "han hablado",
        ]

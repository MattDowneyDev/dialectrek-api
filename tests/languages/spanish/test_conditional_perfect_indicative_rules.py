import pytest

from languages.spanish.conditional_perfect_indicative_rules import (
    conjugate_conditional_perfect_indicative,
)


class TestRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "habría hablado"),
            ("comer", 1, "habrías comido"),
            ("vivir", 2, "habría vivido"),
            ("hacer", 3, "habríamos hecho"),
            ("decir", 4, "habríais dicho"),
            ("ver", 5, "habrían visto"),
            ("volver", 0, "habría vuelto"),
            ("suponer", 0, "habría supuesto"),
        ],
    )
    def test_conditional_perfect_form(self, verb, pronoun_index, expected):
        assert conjugate_conditional_perfect_indicative(verb, pronoun_index) == expected

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_conditional_perfect_indicative("hablar", i) for i in range(6)]
        assert forms == [
            "habría hablado",
            "habrías hablado",
            "habría hablado",
            "habríamos hablado",
            "habríais hablado",
            "habrían hablado",
        ]

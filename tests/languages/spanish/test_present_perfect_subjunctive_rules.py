import pytest

from languages.spanish.present_perfect_subjunctive_rules import (
    conjugate_present_perfect_subjunctive,
)


class TestRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "haya hablado"),
            ("comer", 1, "hayas comido"),
            ("vivir", 2, "haya vivido"),
            ("hacer", 3, "hayamos hecho"),
            ("decir", 4, "hayáis dicho"),
            ("ver", 5, "hayan visto"),
            ("volver", 0, "haya vuelto"),
            ("leer", 0, "haya leído"),
        ],
    )
    def test_present_perfect_subjunctive_form(self, verb, pronoun_index, expected):
        assert conjugate_present_perfect_subjunctive(verb, pronoun_index) == expected

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_present_perfect_subjunctive("hablar", i) for i in range(6)]
        assert forms == [
            "haya hablado",
            "hayas hablado",
            "haya hablado",
            "hayamos hablado",
            "hayáis hablado",
            "hayan hablado",
        ]

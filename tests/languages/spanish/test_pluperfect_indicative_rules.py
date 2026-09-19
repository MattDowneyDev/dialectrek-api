import pytest

from languages.spanish.pluperfect_indicative_rules import conjugate_pluperfect_indicative


class TestRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "había hablado"),
            ("comer", 1, "habías comido"),
            ("vivir", 2, "había vivido"),
            ("hacer", 3, "habíamos hecho"),
            ("decir", 4, "habíais dicho"),
            ("ver", 5, "habían visto"),
            ("volver", 0, "había vuelto"),
            ("suponer", 0, "había supuesto"),
        ],
    )
    def test_pluperfect_form(self, verb, pronoun_index, expected):
        assert conjugate_pluperfect_indicative(verb, pronoun_index) == expected

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_pluperfect_indicative("hablar", i) for i in range(6)]
        assert forms == [
            "había hablado",
            "habías hablado",
            "había hablado",
            "habíamos hablado",
            "habíais hablado",
            "habían hablado",
        ]

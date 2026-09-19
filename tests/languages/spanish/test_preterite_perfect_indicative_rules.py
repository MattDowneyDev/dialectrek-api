import pytest

from languages.spanish.preterite_perfect_indicative_rules import (
    conjugate_preterite_perfect_indicative,
)


class TestRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "hube hablado"),
            ("comer", 1, "hubiste comido"),
            ("vivir", 2, "hubo vivido"),
            ("hacer", 3, "hubimos hecho"),
            ("decir", 4, "hubisteis dicho"),
            ("ver", 5, "hubieron visto"),
            ("volver", 0, "hube vuelto"),
            ("suponer", 0, "hube supuesto"),
        ],
    )
    def test_preterite_perfect_form(self, verb, pronoun_index, expected):
        assert conjugate_preterite_perfect_indicative(verb, pronoun_index) == expected

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_preterite_perfect_indicative("hablar", i) for i in range(6)]
        assert forms == [
            "hube hablado",
            "hubiste hablado",
            "hubo hablado",
            "hubimos hablado",
            "hubisteis hablado",
            "hubieron hablado",
        ]

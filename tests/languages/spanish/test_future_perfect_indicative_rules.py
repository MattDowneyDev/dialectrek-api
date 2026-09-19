import pytest

from languages.spanish.future_perfect_indicative_rules import conjugate_future_perfect_indicative


class TestRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "habré hablado"),
            ("comer", 1, "habrás comido"),
            ("vivir", 2, "habrá vivido"),
            ("hacer", 3, "habremos hecho"),
            ("decir", 4, "habréis dicho"),
            ("ver", 5, "habrán visto"),
            ("volver", 0, "habré vuelto"),
            ("suponer", 0, "habré supuesto"),
        ],
    )
    def test_future_perfect_form(self, verb, pronoun_index, expected):
        assert conjugate_future_perfect_indicative(verb, pronoun_index) == expected

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_future_perfect_indicative("hablar", i) for i in range(6)]
        assert forms == [
            "habré hablado",
            "habrás hablado",
            "habrá hablado",
            "habremos hablado",
            "habréis hablado",
            "habrán hablado",
        ]

    def test_participle_stays_invariable_across_persons(self):
        participles = {
            conjugate_future_perfect_indicative("hablar", i).split(" ", 1)[1] for i in range(6)
        }
        assert participles == {"hablado"}

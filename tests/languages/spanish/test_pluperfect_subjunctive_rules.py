import pytest

from languages.spanish.pluperfect_subjunctive_rules import conjugate_pluperfect_subjunctive


class TestRaFormRegularAndIrregularParticiples:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "hubiera hablado"),
            ("comer", 1, "hubieras comido"),
            ("vivir", 2, "hubiera vivido"),
            ("hacer", 3, "hubiéramos hecho"),
            ("decir", 4, "hubierais dicho"),
            ("ver", 5, "hubieran visto"),
            ("volver", 0, "hubiera vuelto"),
            ("suponer", 0, "hubiera supuesto"),
        ],
    )
    def test_pluperfect_subjunctive_ra_form(self, verb, pronoun_index, expected):
        assert conjugate_pluperfect_subjunctive(verb, pronoun_index) == expected

    def test_default_form_is_ra(self):
        assert conjugate_pluperfect_subjunctive("hablar", 0) == conjugate_pluperfect_subjunctive(
            "hablar", 0, form="ra"
        )

    def test_auxiliary_conjugates_across_all_persons(self):
        forms = [conjugate_pluperfect_subjunctive("hablar", i) for i in range(6)]
        assert forms == [
            "hubiera hablado",
            "hubieras hablado",
            "hubiera hablado",
            "hubiéramos hablado",
            "hubierais hablado",
            "hubieran hablado",
        ]


class TestSeForm:
    @pytest.mark.parametrize(
        "verb,pronoun_index,expected",
        [
            ("hablar", 0, "hubiese hablado"),
            ("hacer", 3, "hubiésemos hecho"),
        ],
    )
    def test_pluperfect_subjunctive_se_form(self, verb, pronoun_index, expected):
        assert conjugate_pluperfect_subjunctive(verb, pronoun_index, form="se") == expected


class TestAuxiliaryStemIsAlwaysHaberDerived:
    def test_auxiliary_is_always_hubiera_regardless_of_main_verb_irregularity(self):
        for verb in ("hablar", "tener", "decir", "ir"):
            aux = conjugate_pluperfect_subjunctive(verb, 0).split(" ", 1)[0]
            assert aux == "hubiera"

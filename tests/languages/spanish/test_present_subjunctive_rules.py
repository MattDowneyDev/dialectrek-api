import pytest

from languages.spanish.present_indicative_rules import STEM_CHANGES
from languages.spanish.present_subjunctive_rules import (
    IRREGULAR_SUBJUNCTIVE,
    SUBJUNCTIVE_STEM_OVERRIDES,
    apply_secondary_change,
    apply_stem_change,
    conjugate_present_subjunctive,
    get_subjunctive_stem,
)

STEM_CHANGE_FORMS = {
    "pensar": ["piense", "pienses", "piense", "pensemos", "penséis", "piensen"],
    "querer": ["quiera", "quieras", "quiera", "queramos", "queráis", "quieran"],
    "empezar": ["empiece", "empieces", "empiece", "empecemos", "empecéis", "empiecen"],
    "entender": ["entienda", "entiendas", "entienda", "entendamos", "entendáis", "entiendan"],
    "comenzar": ["comience", "comiences", "comience", "comencemos", "comencéis", "comiencen"],
    "convertir": ["convierta", "conviertas", "convierta", "convirtamos", "convirtáis", "conviertan"],
    "perder": ["pierda", "pierdas", "pierda", "perdamos", "perdáis", "pierdan"],
    "sentir": ["sienta", "sientas", "sienta", "sintamos", "sintáis", "sientan"],
    "dormir": ["duerma", "duermas", "duerma", "durmamos", "durmáis", "duerman"],
    "poder": ["pueda", "puedas", "pueda", "podamos", "podáis", "puedan"],
    "volver": ["vuelva", "vuelvas", "vuelva", "volvamos", "volváis", "vuelvan"],
    "contar": ["cuente", "cuentes", "cuente", "contemos", "contéis", "cuenten"],
    "encontrar": ["encuentre", "encuentres", "encuentre", "encontremos", "encontréis", "encuentren"],
    "morir": ["muera", "mueras", "muera", "muramos", "muráis", "mueran"],
    "recordar": ["recuerde", "recuerdes", "recuerde", "recordemos", "recordéis", "recuerden"],
    "pedir": ["pida", "pidas", "pida", "pidamos", "pidáis", "pidan"],
    "servir": ["sirva", "sirvas", "sirva", "sirvamos", "sirváis", "sirvan"],
    "repetir": ["repita", "repitas", "repita", "repitamos", "repitáis", "repitan"],
    "seguir": ["siga", "sigas", "siga", "sigamos", "sigáis", "sigan"],
    "conseguir": ["consiga", "consigas", "consiga", "consigamos", "consigáis", "consigan"],
    "jugar": ["juegue", "juegues", "juegue", "juguemos", "juguéis", "jueguen"],
}

STEM_OVERRIDE_FORMS = {
    "ver": ["vea", "veas", "vea", "veamos", "veáis", "vean"],
    "tener": ["tenga", "tengas", "tenga", "tengamos", "tengáis", "tengan"],
    "hacer": ["haga", "hagas", "haga", "hagamos", "hagáis", "hagan"],
    "decir": ["diga", "digas", "diga", "digamos", "digáis", "digan"],
    "venir": ["venga", "vengas", "venga", "vengamos", "vengáis", "vengan"],
    "poner": ["ponga", "pongas", "ponga", "pongamos", "pongáis", "pongan"],
    "salir": ["salga", "salgas", "salga", "salgamos", "salgáis", "salgan"],
    "traer": ["traiga", "traigas", "traiga", "traigamos", "traigáis", "traigan"],
    "caer": ["caiga", "caigas", "caiga", "caigamos", "caigáis", "caigan"],
    "oír": ["oiga", "oigas", "oiga", "oigamos", "oigáis", "oigan"],
    "mantener": ["mantenga", "mantengas", "mantenga", "mantengamos", "mantengáis", "mantengan"],
    "suponer": ["suponga", "supongas", "suponga", "supongamos", "supongáis", "supongan"],
    "conocer": ["conozca", "conozcas", "conozca", "conozcamos", "conozcáis", "conozcan"],
    "conducir": ["conduzca", "conduzcas", "conduzca", "conduzcamos", "conduzcáis", "conduzcan"],
    "traducir": ["traduzca", "traduzcas", "traduzca", "traduzcamos", "traduzcáis", "traduzcan"],
}


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hable", "hables", "hable", "hablemos", "habléis", "hablen"]),
            ("comer", ["coma", "comas", "coma", "comamos", "comáis", "coman"]),
            ("vivir", ["viva", "vivas", "viva", "vivamos", "viváis", "vivan"]),
        ],
    )
    def test_regular_conjugation_all_persons(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_present_subjunctive(verb, i) == expected


class TestFullyIrregularSubjunctive:
    @pytest.mark.parametrize("verb,forms", IRREGULAR_SUBJUNCTIVE.items())
    def test_irregular_subjunctive_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_present_subjunctive(verb, i) == expected


class TestSubjunctiveStemOverrides:
    @pytest.mark.parametrize("verb", SUBJUNCTIVE_STEM_OVERRIDES)
    def test_override_stem_verb_matches_expected_forms(self, verb):
        expected = STEM_OVERRIDE_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_present_subjunctive(verb, i) == form


class TestStemChangingVerbs:
    @pytest.mark.parametrize("verb,change_type", STEM_CHANGES.items())
    def test_stem_change_verb_matches_expected_forms(self, verb, change_type):
        expected = STEM_CHANGE_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_present_subjunctive(verb, i) == form

    def test_ir_stem_changers_still_change_in_nosotros_vosotros(self):
        # unlike present indicative, -ir stem-changers get a (weaker)
        # change in nosotros/vosotros here too
        assert conjugate_present_subjunctive("dormir", 3) == "durmamos"
        assert conjugate_present_subjunctive("pedir", 3) == "pidamos"

    def test_ar_er_stem_changers_stay_regular_in_nosotros_vosotros(self):
        assert conjugate_present_subjunctive("pensar", 3) == "pensemos"
        assert conjugate_present_subjunctive("volver", 3) == "volvamos"

    def test_guir_verbs_drop_silent_u_in_every_form(self):
        for i in range(6):
            assert "gu" not in conjugate_present_subjunctive("seguir", i)


class TestGeneralSpellingFixups:
    @pytest.mark.parametrize(
        "verb,expected_first_form",
        [
            ("parecer", "parezca"),
            ("producir", "produzca"),
            ("dirigir", "dirija"),
            ("coger", "coja"),
        ],
    )
    def test_c_to_zc_and_g_to_j_apply_generally_not_just_overrides(self, verb, expected_first_form):
        assert conjugate_present_subjunctive(verb, 0) == expected_first_form

    def test_c_to_zc_applies_to_every_form_not_just_yo(self):
        assert conjugate_present_subjunctive("parecer", 3) == "parezcamos"


class TestOrthographicSpellingShifts:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("buscar", ["busque", "busques", "busque", "busquemos", "busquéis", "busquen"]),
            ("llegar", ["llegue", "llegues", "llegue", "lleguemos", "lleguéis", "lleguen"]),
            ("cruzar", ["cruce", "cruces", "cruce", "crucemos", "crucéis", "crucen"]),
        ],
    )
    def test_spelling_shift_applies_to_all_six_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_present_subjunctive(verb, i) == expected


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_present_subjunctive("  HABLAR  ", 0) == "hable"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_present_subjunctive("hablx", 0)

    def test_irregular_verb_bypasses_ending_validation(self):
        assert conjugate_present_subjunctive("ser", 0) == "sea"

    def test_accented_ir_infinitive_normalizes_like_regular_ir(self):
        assert conjugate_present_subjunctive("oír", 0) == "oiga"


class TestHelperFunctions:
    def test_apply_stem_change(self):
        assert apply_stem_change("pens", "e_ie") == "piens"

    def test_apply_secondary_change(self):
        assert apply_secondary_change("dorm", "o_ue") == "durm"

    def test_get_subjunctive_stem_uses_override_first(self):
        assert get_subjunctive_stem("tener", "ten", "er") == "teng"

    def test_get_subjunctive_stem_c_to_zc_after_vowel(self):
        assert get_subjunctive_stem("conocer", "conoc", "er") == "conozc"

    def test_get_subjunctive_stem_g_to_j_when_not_a_stem_changer(self):
        assert get_subjunctive_stem("dirigir", "dirig", "ir") == "dirij"

    def test_get_subjunctive_stem_falls_back_to_raw_stem(self):
        assert get_subjunctive_stem("hablar", "habl", "ar") == "habl"

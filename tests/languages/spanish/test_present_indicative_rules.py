import pytest

from languages.spanish.present_indicative_rules import (
    IRREGULAR_VERBS,
    STEM_CHANGES,
    conjugate_present_indicative,
)

STEM_CHANGE_FORMS = {
    "pensar": ["pienso", "piensas", "piensa", "pensamos", "pensáis", "piensan"],
    "querer": ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"],
    "empezar": ["empiezo", "empiezas", "empieza", "empezamos", "empezáis", "empiezan"],
    "entender": ["entiendo", "entiendes", "entiende", "entendemos", "entendéis", "entienden"],
    "comenzar": ["comienzo", "comienzas", "comienza", "comenzamos", "comenzáis", "comienzan"],
    "convertir": ["convierto", "conviertes", "convierte", "convertimos", "convertís", "convierten"],
    "perder": ["pierdo", "pierdes", "pierde", "perdemos", "perdéis", "pierden"],
    "sentir": ["siento", "sientes", "siente", "sentimos", "sentís", "sienten"],
    "dormir": ["duermo", "duermes", "duerme", "dormimos", "dormís", "duermen"],
    "poder": ["puedo", "puedes", "puede", "podemos", "podéis", "pueden"],
    "volver": ["vuelvo", "vuelves", "vuelve", "volvemos", "volvéis", "vuelven"],
    "contar": ["cuento", "cuentas", "cuenta", "contamos", "contáis", "cuentan"],
    "encontrar": ["encuentro", "encuentras", "encuentra", "encontramos", "encontráis", "encuentran"],
    "morir": ["muero", "mueres", "muere", "morimos", "morís", "mueren"],
    "recordar": ["recuerdo", "recuerdas", "recuerda", "recordamos", "recordáis", "recuerdan"],
    "pedir": ["pido", "pides", "pide", "pedimos", "pedís", "piden"],
    "servir": ["sirvo", "sirves", "sirve", "servimos", "servís", "sirven"],
    "repetir": ["repito", "repites", "repite", "repetimos", "repetís", "repiten"],
    "seguir": ["sigo", "sigues", "sigue", "seguimos", "seguís", "siguen"],
    "conseguir": ["consigo", "consigues", "consigue", "conseguimos", "conseguís", "consiguen"],
    "jugar": ["juego", "juegas", "juega", "jugamos", "jugáis", "juegan"],
}


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablo", "hablas", "habla", "hablamos", "habláis", "hablan"]),
            ("comer", ["como", "comes", "come", "comemos", "coméis", "comen"]),
            ("vivir", ["vivo", "vives", "vive", "vivimos", "vivís", "viven"]),
        ],
    )
    def test_regular_conjugation_all_persons(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_present_indicative(verb, i) == expected


class TestIrregularVerbs:
    @pytest.mark.parametrize("verb,forms", IRREGULAR_VERBS.items())
    def test_fully_irregular_verb_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_present_indicative(verb, i) == expected


class TestStemChangingVerbs:
    @pytest.mark.parametrize("verb,change_type", STEM_CHANGES.items())
    def test_stem_change_verb_matches_expected_forms(self, verb, change_type):
        expected = STEM_CHANGE_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_present_indicative(verb, i) == form

    def test_stem_change_does_not_apply_to_nosotros_or_vosotros(self):
        assert conjugate_present_indicative("pensar", 3) == "pensamos"
        assert conjugate_present_indicative("pensar", 4) == "pensáis"
        assert conjugate_present_indicative("dormir", 3) == "dormimos"
        assert conjugate_present_indicative("dormir", 4) == "dormís"


class TestYoFormSpellingFixups:
    @pytest.mark.parametrize(
        "verb,expected_yo",
        [
            ("conocer", "conozco"),
            ("conducir", "conduzco"),
            ("traducir", "traduzco"),
            ("parecer", "parezco"),
            ("dirigir", "dirijo"),
            ("coger", "cojo"),
            ("exigir", "exijo"),
        ],
    )
    def test_c_to_zc_and_g_to_j_yo_forms(self, verb, expected_yo):
        assert conjugate_present_indicative(verb, 0) == expected_yo

    def test_c_to_zc_only_applies_to_yo_form(self):
        assert conjugate_present_indicative("conocer", 1) == "conoces"
        assert conjugate_present_indicative("conocer", 2) == "conoce"

    def test_g_to_j_only_applies_to_yo_form(self):
        assert conjugate_present_indicative("dirigir", 1) == "diriges"
        assert conjugate_present_indicative("dirigir", 2) == "dirige"

    def test_guir_stem_change_drops_silent_u_in_yo_form(self):
        assert conjugate_present_indicative("seguir", 0) == "sigo"
        assert conjugate_present_indicative("conseguir", 0) == "consigo"

    def test_g_to_j_fixup_does_not_apply_when_verb_is_a_stem_changer(self):
        # seguir ends in -guir and is a STEM_CHANGES entry -- the general
        # g->j fallback must not also fire and double-mangle the stem.
        assert conjugate_present_indicative("seguir", 0) == "sigo"


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_present_indicative("  HABLAR  ", 0) == "hablo"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_present_indicative("hablx", 0)

    def test_irregular_verb_bypasses_ending_validation(self):
        assert conjugate_present_indicative("ser", 0) == "soy"

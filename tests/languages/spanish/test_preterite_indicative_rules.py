import pytest

from languages.spanish.preterite_indicative_rules import (
    IR_STEM_CHANGES,
    IRREGULAR_VERBS,
    I_TO_Y_VERBS,
    J_STEM_VERBS,
    STRONG_STEMS,
    apply_stem_change,
    conjugate_preterite_indicative,
)

IR_STEM_CHANGE_FORMS = {
    "pedir": ["pedí", "pediste", "pidió", "pedimos", "pedisteis", "pidieron"],
    "servir": ["serví", "serviste", "sirvió", "servimos", "servisteis", "sirvieron"],
    "repetir": ["repetí", "repetiste", "repitió", "repetimos", "repetisteis", "repitieron"],
    "seguir": ["seguí", "seguiste", "siguió", "seguimos", "seguisteis", "siguieron"],
    "conseguir": ["conseguí", "conseguiste", "consiguió", "conseguimos", "conseguisteis", "consiguieron"],
    "sentir": ["sentí", "sentiste", "sintió", "sentimos", "sentisteis", "sintieron"],
    "convertir": ["convertí", "convertiste", "convirtió", "convertimos", "convertisteis", "convirtieron"],
    "preferir": ["preferí", "preferiste", "prefirió", "preferimos", "preferisteis", "prefirieron"],
    "mentir": ["mentí", "mentiste", "mintió", "mentimos", "mentisteis", "mintieron"],
    "dormir": ["dormí", "dormiste", "durmió", "dormimos", "dormisteis", "durmieron"],
    "morir": ["morí", "moriste", "murió", "morimos", "moristeis", "murieron"],
}

STRONG_STEM_FORMS = {
    "tener": ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"],
    "mantener": ["mantuve", "mantuviste", "mantuvo", "mantuvimos", "mantuvisteis", "mantuvieron"],
    "estar": ["estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron"],
    "andar": ["anduve", "anduviste", "anduvo", "anduvimos", "anduvisteis", "anduvieron"],
    "haber": ["hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron"],
    "poder": ["pude", "pudiste", "pudo", "pudimos", "pudisteis", "pudieron"],
    "poner": ["puse", "pusiste", "puso", "pusimos", "pusisteis", "pusieron"],
    "suponer": ["supuse", "supusiste", "supuso", "supusimos", "supusisteis", "supusieron"],
    "saber": ["supe", "supiste", "supo", "supimos", "supisteis", "supieron"],
    "caber": ["cupe", "cupiste", "cupo", "cupimos", "cupisteis", "cupieron"],
    "hacer": ["hice", "hiciste", "hizo", "hicimos", "hicisteis", "hicieron"],
    "querer": ["quise", "quisiste", "quiso", "quisimos", "quisisteis", "quisieron"],
    "venir": ["vine", "viniste", "vino", "vinimos", "vinisteis", "vinieron"],
    "decir": ["dije", "dijiste", "dijo", "dijimos", "dijisteis", "dijeron"],
    "traer": ["traje", "trajiste", "trajo", "trajimos", "trajisteis", "trajeron"],
    "conducir": ["conduje", "condujiste", "condujo", "condujimos", "condujisteis", "condujeron"],
    "traducir": ["traduje", "tradujiste", "tradujo", "tradujimos", "tradujisteis", "tradujeron"],
    "producir": ["produje", "produjiste", "produjo", "produjimos", "produjisteis", "produjeron"],
}


class TestFullyRegularVerbs:
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("hablar", ["hablé", "hablaste", "habló", "hablamos", "hablasteis", "hablaron"]),
            ("comer", ["comí", "comiste", "comió", "comimos", "comisteis", "comieron"]),
            ("vivir", ["viví", "viviste", "vivió", "vivimos", "vivisteis", "vivieron"]),
        ],
    )
    def test_regular_conjugation_all_persons(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_preterite_indicative(verb, i) == expected


class TestFullyIrregularVerbs:
    @pytest.mark.parametrize("verb,forms", IRREGULAR_VERBS.items())
    def test_irregular_verb_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_preterite_indicative(verb, i) == expected

    def test_ser_and_ir_share_identical_forms(self):
        assert IRREGULAR_VERBS["ser"] == IRREGULAR_VERBS["ir"]


class TestStrongStemVerbs:
    @pytest.mark.parametrize("verb", STRONG_STEMS)
    def test_strong_stem_verb_matches_expected_forms(self, verb):
        expected = STRONG_STEM_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_preterite_indicative(verb, i) == form

    def test_hacer_has_c_to_z_spelling_change_in_third_person_singular(self):
        assert conjugate_preterite_indicative("hacer", 2) == "hizo"
        assert conjugate_preterite_indicative("hacer", 5) == "hicieron"

    @pytest.mark.parametrize("verb", J_STEM_VERBS)
    def test_j_stem_verbs_drop_the_i_in_third_person_plural(self, verb):
        assert not conjugate_preterite_indicative(verb, 5).endswith("ieron")
        assert conjugate_preterite_indicative(verb, 5).endswith("eron")


class TestIrStemChangingVerbs:
    @pytest.mark.parametrize("verb,change_type", IR_STEM_CHANGES.items())
    def test_ir_stem_changer_matches_expected_forms(self, verb, change_type):
        expected = IR_STEM_CHANGE_FORMS[verb]
        for i, form in enumerate(expected):
            assert conjugate_preterite_indicative(verb, i) == form

    def test_stem_change_only_applies_to_third_person_forms(self):
        assert conjugate_preterite_indicative("pedir", 0) == "pedí"
        assert conjugate_preterite_indicative("pedir", 1) == "pediste"
        assert conjugate_preterite_indicative("pedir", 3) == "pedimos"
        assert conjugate_preterite_indicative("pedir", 4) == "pedisteis"

    def test_ar_verbs_never_stem_change_in_preterite(self):
        assert conjugate_preterite_indicative("pensar", 2) == "pensó"
        assert conjugate_preterite_indicative("contar", 2) == "contó"


class TestIToYVerbsWithStrongVowelStem:
    # leer/creer/oír/caer -- stem ends in a strong vowel (a/e/o), which
    # genuinely does need the written accent on tú/nosotros/vosotros to
    # mark hiatus (leíste, not "leiste").
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("leer", ["leí", "leíste", "leyó", "leímos", "leísteis", "leyeron"]),
            ("creer", ["creí", "creíste", "creyó", "creímos", "creísteis", "creyeron"]),
            ("oír", ["oí", "oíste", "oyó", "oímos", "oísteis", "oyeron"]),
            ("caer", ["caí", "caíste", "cayó", "caímos", "caísteis", "cayeron"]),
        ],
    )
    def test_strong_vowel_stem_i_to_y_verb_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_preterite_indicative(verb, i) == expected


class TestIToYVerbsWithWeakVowelStem:
    # construir/destruir/incluir/influir have a stem ending in "u" (a weak
    # vowel), which forms a diphthong with the following "i" and takes no
    # written accent in tú/nosotros/vosotros ("construiste"/"construimos",
    # unlike the strong-vowel-stem group above).
    @pytest.mark.parametrize(
        "verb,forms",
        [
            ("construir", ["construí", "construiste", "construyó", "construimos", "construisteis", "construyeron"]),
            ("destruir", ["destruí", "destruiste", "destruyó", "destruimos", "destruisteis", "destruyeron"]),
            ("incluir", ["incluí", "incluiste", "incluyó", "incluimos", "incluisteis", "incluyeron"]),
            ("influir", ["influí", "influiste", "influyó", "influimos", "influisteis", "influyeron"]),
        ],
    )
    def test_weak_vowel_stem_i_to_y_verb_matches_expected_forms(self, verb, forms):
        for i, expected in enumerate(forms):
            assert conjugate_preterite_indicative(verb, i) == expected

    def test_third_person_forms_are_correct_regardless_of_the_bug(self):
        # the i->y swap in él/ellos forms isn't affected by the accent bug
        assert conjugate_preterite_indicative("construir", 2) == "construyó"
        assert conjugate_preterite_indicative("construir", 5) == "construyeron"


class TestSpellingShiftYoForm:
    @pytest.mark.parametrize(
        "verb,expected_yo",
        [
            ("buscar", "busqué"),
            ("llegar", "llegué"),
            ("empezar", "empecé"),
            ("cruzar", "crucé"),
        ],
    )
    def test_yo_form_spelling_shift(self, verb, expected_yo):
        assert conjugate_preterite_indicative(verb, 0) == expected_yo

    def test_spelling_shift_only_applies_to_yo_form(self):
        assert conjugate_preterite_indicative("buscar", 1) == "buscaste"
        assert conjugate_preterite_indicative("buscar", 2) == "buscó"


class TestNormalizationAndErrors:
    def test_strips_whitespace_and_lowercases(self):
        assert conjugate_preterite_indicative("  HABLAR  ", 0) == "hablé"

    def test_invalid_ending_raises_value_error(self):
        with pytest.raises(ValueError):
            conjugate_preterite_indicative("hablx", 0)

    def test_irregular_verb_bypasses_ending_validation(self):
        assert conjugate_preterite_indicative("ser", 0) == "fui"

    def test_accented_ir_infinitive_normalizes_like_regular_ir(self):
        assert conjugate_preterite_indicative("oír", 3) == "oímos"


class TestApplyStemChange:
    def test_e_i_change(self):
        assert apply_stem_change("ped", "e_i") == "pid"

    def test_o_u_change(self):
        assert apply_stem_change("dorm", "o_u") == "durm"

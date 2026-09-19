import pytest

from languages.french.present_perfect_indicative_rules import (
    AGREEMENT_ENDINGS,
    ETRE_VERBS,
    agreed_participle,
    conjugate_present_perfect_indicative,
)


class TestAvoirVerbs:
    def test_parler(self):
        assert conjugate_present_perfect_indicative("parler", 0) == "ai parlé"
        assert conjugate_present_perfect_indicative("parler", 3) == "avons parlé"

    def test_participle_never_agrees_with_avoir(self):
        assert conjugate_present_perfect_indicative("parler", 3) == "avons parlé"
        assert conjugate_present_perfect_indicative("parler", 5) == "ont parlé"

    def test_faire_irregular_participle(self):
        assert conjugate_present_perfect_indicative("faire", 0) == "ai fait"

    def test_passer_is_left_off_etre_verbs_and_uses_avoir(self):
        assert "passer" not in ETRE_VERBS
        assert conjugate_present_perfect_indicative("passer", 0) == "ai passé"


class TestEtreVerbs:
    @pytest.mark.parametrize("verb", sorted(ETRE_VERBS))
    def test_every_etre_verb_takes_etre_and_agrees_in_plural(self, verb):
        singular = conjugate_present_perfect_indicative(verb, 0)
        plural = conjugate_present_perfect_indicative(verb, 3)
        assert singular.startswith("suis ")
        assert plural.startswith("sommes ")
        assert plural.endswith("s")
        assert plural[:-1].endswith(singular.split(" ", 1)[1])

    def test_aller(self):
        assert conjugate_present_perfect_indicative("aller", 0) == "suis allé"
        assert conjugate_present_perfect_indicative("aller", 3) == "sommes allés"
        assert conjugate_present_perfect_indicative("aller", 5) == "sont allés"

    def test_naitre_irregular_participle_plus_etre(self):
        assert conjugate_present_perfect_indicative("naître", 0) == "suis né"
        assert conjugate_present_perfect_indicative("naître", 3) == "sommes nés"

    def test_singular_forms_have_no_agreement_s(self):
        for pronoun_index in (0, 1, 2):
            form = conjugate_present_perfect_indicative("aller", pronoun_index)
            assert form.endswith("allé")


class TestAgreedParticiple:
    def test_avoir_path_never_appends_s(self):
        for pronoun_index in range(6):
            assert agreed_participle("parler", pronoun_index, False) == "parlé"

    @pytest.mark.parametrize("pronoun_index", [0, 1, 2])
    def test_etre_singular_has_no_ending(self, pronoun_index):
        assert agreed_participle("aller", pronoun_index, True) == "allé"

    @pytest.mark.parametrize("pronoun_index", [3, 4, 5])
    def test_etre_plural_adds_s(self, pronoun_index):
        assert agreed_participle("aller", pronoun_index, True) == "allés"

    def test_agreement_endings_table_shape(self):
        assert AGREEMENT_ENDINGS == ["", "", "", "s", "s", "s"]


class TestReflexiveVerbsAlwaysTakeEtre:
    def test_se_lever_takes_etre_even_though_lever_takes_avoir(self):
        assert "lever" not in ETRE_VERBS
        assert conjugate_present_perfect_indicative("se lever", 0) == "me suis levé"
        assert conjugate_present_perfect_indicative("se lever", 3) == "nous sommes levés"

    def test_s_habiller_elision_depends_on_auxiliary_not_participle(self):
        # the reflexive pronoun sits in front of the auxiliary, so the
        # elision check looks at "suis"/"es" (consonant-initial), not at
        # the participle that follows
        assert conjugate_present_perfect_indicative("s'habiller", 0) == "me suis habillé"
        assert conjugate_present_perfect_indicative("s'habiller", 1) == "t'es habillé"

    def test_input_is_stripped_and_lowercased(self):
        assert conjugate_present_perfect_indicative("  Parler ", 0) == "ai parlé"

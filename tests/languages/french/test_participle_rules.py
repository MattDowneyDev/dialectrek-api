import pytest

from languages.french.participle_rules import (
    IRREGULAR_PARTICIPLES,
    conjugate_past_participle,
    is_irregular_participle,
)


class TestRegularVerbs:
    def test_er_verb(self):
        assert conjugate_past_participle("parler") == "parlé"

    def test_ir_verb(self):
        assert conjugate_past_participle("finir") == "fini"

    def test_dormir_type_verb_still_uses_regular_ir_pattern(self):
        assert conjugate_past_participle("dormir") == "dormi"

    def test_re_verb(self):
        assert conjugate_past_participle("attendre") == "attendu"

    def test_invalid_infinitive_ending_raises(self):
        with pytest.raises(ValueError):
            conjugate_past_participle("parl")


class TestIrregularParticiples:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_PARTICIPLES))
    def test_every_irregular_participle_matches_its_own_table(self, verb):
        assert conjugate_past_participle(verb) == IRREGULAR_PARTICIPLES[verb]

    def test_etre(self):
        assert conjugate_past_participle("être") == "été"

    def test_avoir(self):
        assert conjugate_past_participle("avoir") == "eu"

    def test_devoir_keeps_circumflex(self):
        assert conjugate_past_participle("devoir") == "dû"

    def test_mourir(self):
        assert conjugate_past_participle("mourir") == "mort"

    def test_ouvrir_is_irregular_despite_ir_ending(self):
        assert conjugate_past_participle("ouvrir") == "ouvert"

    def test_connaitre_family_member_is_covered(self):
        assert conjugate_past_participle("connaître") == "connu"


class TestIsIrregularParticiple:
    @pytest.mark.parametrize("verb", sorted(IRREGULAR_PARTICIPLES))
    def test_irregular_verbs_flagged(self, verb):
        assert is_irregular_participle(verb) is True

    @pytest.mark.parametrize("verb", ["parler", "finir", "attendre", "dormir"])
    def test_regular_verbs_not_flagged(self, verb):
        assert is_irregular_participle(verb) is False

    def test_reflexive_irregularity_checks_base_verb(self):
        assert is_irregular_participle("se lever") is False
        assert is_irregular_participle("s'appeler") is False

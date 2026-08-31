"""L'imparfait: parlais, parlais, parlait, parlions, parliez,
parlaient.

The imperfect stem is always the same one the present tense's "nous"
form is built on -- even for verbs that are a mess in the present.
avoir -> avons -> avais, faire -> faisons -> faisais, boire -> buvons
-> buvais. être is the one exception: "sommes" doesn't give us
anything to work with, so its stem ("ét-") just has to be memorized.

None of the present tense's je/tu/il/ils-only changes (acheter's e->è,
appeler's doubling, envoyer's y->i) show up here, since the imperfect
always builds on the plural stem those changes never touch. -cer/-ger
verbs are the one wrinkle that does carry over, and only for the
endings starting with "a" -- nous/vous take "i", which is already soft
enough ("nous commencions", not "commençions")."""

from languages.french.common import reflexive_pronoun, strip_reflexive
from languages.french.present_indicative_rules import (
    DORMIR_TYPE_VERBS,
    IRREGULAR_VERBS,
    conjugate_present_indicative,
)

IMPERFECT_ENDINGS = ["ais", "ais", "ait", "ions", "iez", "aient"]


def imperfect_stem(verb):
    if verb == "être":
        return "ét"
    if verb in IRREGULAR_VERBS or verb in DORMIR_TYPE_VERBS or verb.endswith(("ir", "re")):
        # "nous" always ends in "-ons" (être aside), no matter how
        # irregular the verb is otherwise, so just strip it off.
        return conjugate_present_indicative(verb, 3)[:-3]
    # regular -er verb, plain stem
    return verb[:-2]


def conjugate_imperfect_indicative(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)
    stem = imperfect_stem(base_verb)

    if pronoun_index in (0, 1, 2, 5):
        if base_verb.endswith("cer"):
            stem = stem[:-1] + "ç"
        elif base_verb.endswith("ger"):
            stem = stem + "e"

    conjugated = stem + IMPERFECT_ENDINGS[pronoun_index]
    if is_reflexive:
        return reflexive_pronoun(pronoun_index, conjugated) + conjugated
    return conjugated


def is_irregular_imperfect(verb):
    base_verb, _ = strip_reflexive(verb.strip().lower())
    return base_verb == "être"

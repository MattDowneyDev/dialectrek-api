"""Le subjonctif présent: que je parle, que tu parles, qu'il parle,
que nous parlions, que vous parliez, qu'ils parlent.

Most verbs have two stems here: je/tu/il/ils come from the present
tense's "ils" form minus "ent" (venir -> viennent -> vienn-), and
nous/vous come from the same stem the imperfect uses (venir -> ven-,
same as "nous venons" minus "ons"). For regular verbs those two stems
are identical, so it just looks like one stem with regular endings --
but stem-changing verbs like acheter or boire keep that same present-
tense split (achète.../achet-ions, boiv.../buv-ions).

être, avoir, faire, pouvoir, savoir, aller, and vouloir don't fit that
pattern at all and are just memorized. être and avoir are irregular
enough (aie/aies/AIT, not aie/aies/aie) that they get every form
spelled out; the rest just need their stem(s) memorized and slot
into the regular endings fine.
"""

from languages.french.common import reflexive_pronoun, strip_reflexive
from languages.french.imperfect_indicative_rules import imperfect_stem
from languages.french.present_indicative_rules import conjugate_present_indicative

SUBJUNCTIVE_ENDINGS = ["e", "es", "e", "ions", "iez", "ent"]

FULLY_IRREGULAR_SUBJUNCTIVE = {
    "être": ["sois", "sois", "soit", "soyons", "soyez", "soient"],
    "avoir": ["aie", "aies", "ait", "ayons", "ayez", "aient"],
}

# verb -> (je/tu/il/ils stem, nous/vous stem), for the handful of verbs
# whose subjunctive stem can't be derived from the present tense at all
IRREGULAR_SUBJUNCTIVE_STEMS = {
    "faire": ("fass", "fass"),
    "pouvoir": ("puiss", "puiss"),
    "savoir": ("sach", "sach"),
    "aller": ("aill", "all"),
    "vouloir": ("veuill", "voul"),
}


def _subjunctive_stems(verb):
    if verb in IRREGULAR_SUBJUNCTIVE_STEMS:
        return IRREGULAR_SUBJUNCTIVE_STEMS[verb]
    singular_stem = conjugate_present_indicative(verb, 5)[:-3]  # "ils", minus "ent"
    plural_stem = imperfect_stem(verb)
    return singular_stem, plural_stem


def conjugate_present_subjunctive(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)

    if base_verb in FULLY_IRREGULAR_SUBJUNCTIVE:
        conjugated = FULLY_IRREGULAR_SUBJUNCTIVE[base_verb][pronoun_index]
    else:
        singular_stem, plural_stem = _subjunctive_stems(base_verb)
        stem = plural_stem if pronoun_index in (3, 4) else singular_stem
        conjugated = stem + SUBJUNCTIVE_ENDINGS[pronoun_index]

    if is_reflexive:
        return reflexive_pronoun(pronoun_index, conjugated) + conjugated
    return conjugated

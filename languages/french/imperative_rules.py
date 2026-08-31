"""L'impératif only has three forms -- tu, nous, vous -- you can't
command yourself or a third person, so pronoun indices 0, 2, and 5
are never valid here.

Regular formation is just the matching present-tense form, tu included
-- except every "-er" verb (and ouvrir/offrir, which conjugate like
one) drops the tu form's final "s": "tu parles" -> "parle!". This is
true even for irregular "-er" verbs like aller: "tu vas" -> "va!".
être, avoir, savoir, and vouloir don't follow any of this and are just
memorized.

Reflexive verbs are the other wrinkle: the reflexive pronoun jumps
after the verb in the affirmative, with a hyphen, and "te" becomes
"toi" ("Lève-toi!"). In the negative it stays in its normal spot in
front, elision and all ("Ne te lève pas!" / "Ne t'inquiète pas!").
"""

from languages.french.common import ELIDABLE_STARTS, reflexive_pronoun, strip_reflexive
from languages.french.present_indicative_rules import conjugate_present_indicative

VALID_INDICES = (1, 3, 4)

IRREGULAR_IMPERATIVE = {
    "être": ["sois", "soyons", "soyez"],
    "avoir": ["aie", "ayons", "ayez"],
    "savoir": ["sache", "sachons", "sachez"],
    "vouloir": ["veuille", "veuillons", "veuillez"],
}

# -ir verbs that still drop the tu form's "s" like an "-er" verb would
OUVRIR_TYPE_VERBS = {"ouvrir", "offrir"}

# tu/nous/vous, in that order, matching IRREGULAR_IMPERATIVE's lists
_SLOT = {1: 0, 3: 1, 4: 2}

# "te" -> "toi" after the verb; nous/vous don't change
AFFIRMATIVE_REFLEXIVE_PRONOUNS = {1: "toi", 3: "nous", 4: "vous"}


def _base_form(base_verb, pronoun_index):
    if base_verb in IRREGULAR_IMPERATIVE:
        return IRREGULAR_IMPERATIVE[base_verb][_SLOT[pronoun_index]]

    present_form = conjugate_present_indicative(base_verb, pronoun_index)
    if pronoun_index == 1 and (base_verb.endswith("er") or base_verb in OUVRIR_TYPE_VERBS):
        return present_form[:-1]
    return present_form


def conjugate_imperative(verb, pronoun_index, polarity):
    verb = verb.strip().lower()
    if pronoun_index not in VALID_INDICES:
        raise ValueError("The French imperative only has tu/nous/vous forms.")

    base_verb, is_reflexive = strip_reflexive(verb)
    form = _base_form(base_verb, pronoun_index)

    if is_reflexive:
        if polarity == "negative":
            return f"ne {reflexive_pronoun(pronoun_index, form)}{form} pas"
        return f"{form}-{AFFIRMATIVE_REFLEXIVE_PRONOUNS[pronoun_index]}"

    if polarity == "negative":
        ne = "n'" if form[:1].lower() in ELIDABLE_STARTS else "ne "
        return f"{ne}{form} pas"
    return form

"""Le futur simple: parlerai, parleras, parlera, parlerons, parlerez,
parleront.

The endings (ai/as/a/ons/ez/ont) go straight onto the infinitive --
-re verbs just drop the final "e" (attendre -> attendrai). This holds
even for verbs that are a mess everywhere else: mettre -> mettrai,
prendre -> prendrai, connaître -> connaîtrai. Only a small set of
verbs has a genuinely irregular future stem (IRREGULAR_FUTURE_STEMS),
and it's not the same set as the present tense's irregulars -- envoyer
is regular in the present but irregular here ("enverr-"), and it's the
other way around for mettre/prendre/the dormir-type verbs.

For "-er" verbs, the present tense's je/tu/il/ils-only stem changes
(acheter's e->è, appeler's doubling, envoyer-family's y->i) carry over
to every person here, since the future ending picks up right where
those endings left off. The one exception is préférer's é->è change --
tradition keeps the é in the future ("préférerai")."""

from languages.french.common import reflexive_pronoun, replace_last, strip_reflexive
from languages.french.present_indicative_rules import DOUBLING_VERBS, E_STEM_CHANGE_VERBS

FUTURE_ENDINGS = ["ai", "as", "a", "ons", "ez", "ont"]

IRREGULAR_FUTURE_STEMS = {
    "être": "ser",
    "avoir": "aur",
    "faire": "fer",
    "aller": "ir",
    "devoir": "devr",
    "pouvoir": "pourr",
    "vouloir": "voudr",
    "savoir": "saur",
    "venir": "viendr",
    "devenir": "deviendr",
    "tenir": "tiendr",
    "voir": "verr",
    "envoyer": "enverr",
    "courir": "courr",
    "mourir": "mourr",
}


def future_stem(verb):
    if verb in IRREGULAR_FUTURE_STEMS:
        return IRREGULAR_FUTURE_STEMS[verb]

    ending = verb[-2:]
    if ending not in ("er", "ir", "re"):
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -er/-ir/-re)")

    if ending == "re":
        return verb[:-1]
    if ending == "ir":
        return verb

    stem = verb[:-2]
    if verb in DOUBLING_VERBS:
        stem = stem + stem[-1]
    elif verb in E_STEM_CHANGE_VERBS:
        stem = replace_last(stem, "e", "è")
    elif stem.endswith("y"):
        stem = stem[:-1] + "i"
    return stem + "er"


def conjugate_future_indicative(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)
    conjugated = future_stem(base_verb) + FUTURE_ENDINGS[pronoun_index]
    if is_reflexive:
        return reflexive_pronoun(pronoun_index, conjugated) + conjugated
    return conjugated


def is_irregular_future(verb):
    base_verb, _ = strip_reflexive(verb.strip().lower())
    return (
        base_verb in IRREGULAR_FUTURE_STEMS
        or base_verb in DOUBLING_VERBS
        or base_verb in E_STEM_CHANGE_VERBS
        or (base_verb.endswith("er") and base_verb[:-2].endswith("y"))
    )

"""Past participles, needed for the passé composé (avoir/être +
participle).

Regular verbs: -er -> -é (parlé), -ir -> -i (fini -- this still holds
for the dormir-type verbs even though their present tense is
irregular), -re -> -u (attendu). Everything else is memorized below,
including compounds like comprendre/apprendre off prendre -- a prefix
doesn't change whether the participle is irregular, just which verb
it belongs to.

When the auxiliary is être the participle agrees with the subject, but
since this app never tracks gender we just default to masculine
throughout (see AGREEMENT_ENDINGS in present_perfect_indicative_rules)."""

from languages.french.common import strip_reflexive

IRREGULAR_PARTICIPLES = {
    "être": "été",
    "avoir": "eu",
    "faire": "fait",
    "dire": "dit",
    "voir": "vu",
    "savoir": "su",
    "pouvoir": "pu",
    "vouloir": "voulu",
    "venir": "venu",
    "devenir": "devenu",
    "devoir": "dû",
    "prendre": "pris",
    "comprendre": "compris",
    "apprendre": "appris",
    "mettre": "mis",
    "promettre": "promis",
    "permettre": "permis",
    "tenir": "tenu",
    "suivre": "suivi",
    "connaître": "connu",
    "paraître": "paru",
    "écrire": "écrit",
    "croire": "cru",
    "lire": "lu",
    "vivre": "vécu",
    "ouvrir": "ouvert",
    "boire": "bu",
    "courir": "couru",
    "rire": "ri",
    "naître": "né",
    "mourir": "mort",
}


def conjugate_past_participle(verb):
    verb = verb.strip().lower()

    if verb in IRREGULAR_PARTICIPLES:
        return IRREGULAR_PARTICIPLES[verb]

    ending = verb[-2:]
    if ending not in ("er", "ir", "re"):
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -er/-ir/-re)")

    stem = verb[:-2]
    if ending == "er":
        return stem + "é"
    if ending == "ir":
        return stem + "i"
    return stem + "u"


def is_irregular_participle(verb):
    base_verb, _ = strip_reflexive(verb.strip().lower())
    return base_verb in IRREGULAR_PARTICIPLES

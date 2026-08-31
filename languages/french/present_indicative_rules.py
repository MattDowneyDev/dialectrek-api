from languages.french.common import (
    PRONOUNS,
    reflexive_pronoun,
    replace_last,
    strip_reflexive,
)

# Verb -> its 6 present-tense forms, in PRONOUNS order. Compounds built
# on an irregular base (comprendre/apprendre off prendre, promettre/
# permettre off mettre, devenir/revenir/soutenir off venir/tenir,
# poursuivre off suivre, paraître off connaître, réduire and friends
# off the "-uire" family) get their own entries too -- a prefix doesn't
# change which forms are irregular, just which verb they belong to.
IRREGULAR_VERBS = {
    "être": ["suis", "es", "est", "sommes", "êtes", "sont"],
    "avoir": ["ai", "as", "a", "avons", "avez", "ont"],
    "faire": ["fais", "fais", "fait", "faisons", "faites", "font"],
    "aller": ["vais", "vas", "va", "allons", "allez", "vont"],
    "dire": ["dis", "dis", "dit", "disons", "dites", "disent"],
    # unlike "dire" itself, its compounds take a regular "vous" form --
    # "interdisez", not "interdites"
    "interdire": ["interdis", "interdis", "interdit", "interdisons", "interdisez", "interdisent"],
    "voir": ["vois", "vois", "voit", "voyons", "voyez", "voient"],
    "savoir": ["sais", "sais", "sait", "savons", "savez", "savent"],
    "pouvoir": ["peux", "peux", "peut", "pouvons", "pouvez", "peuvent"],
    "vouloir": ["veux", "veux", "veut", "voulons", "voulez", "veulent"],
    "valoir": ["vaux", "vaux", "vaut", "valons", "valez", "valent"],
    "venir": ["viens", "viens", "vient", "venons", "venez", "viennent"],
    "devenir": ["deviens", "deviens", "devient", "devenons", "devenez", "deviennent"],
    "revenir": ["reviens", "reviens", "revient", "revenons", "revenez", "reviennent"],
    "souvenir": ["souviens", "souviens", "souvient", "souvenons", "souvenez", "souviennent"],
    "tenir": ["tiens", "tiens", "tient", "tenons", "tenez", "tiennent"],
    "soutenir": ["soutiens", "soutiens", "soutient", "soutenons", "soutenez", "soutiennent"],
    "devoir": ["dois", "dois", "doit", "devons", "devez", "doivent"],
    "recevoir": ["reçois", "reçois", "reçoit", "recevons", "recevez", "reçoivent"],
    "prendre": ["prends", "prends", "prend", "prenons", "prenez", "prennent"],
    "comprendre": ["comprends", "comprends", "comprend", "comprenons", "comprenez", "comprennent"],
    "apprendre": ["apprends", "apprends", "apprend", "apprenons", "apprenez", "apprennent"],
    "mettre": ["mets", "mets", "met", "mettons", "mettez", "mettent"],
    "promettre": ["promets", "promets", "promet", "promettons", "promettez", "promettent"],
    "permettre": ["permets", "permets", "permet", "permettons", "permettez", "permettent"],
    "combattre": ["combats", "combats", "combat", "combattons", "combattez", "combattent"],
    "écrire": ["écris", "écris", "écrit", "écrivons", "écrivez", "écrivent"],
    "croire": ["crois", "crois", "croit", "croyons", "croyez", "croient"],
    "lire": ["lis", "lis", "lit", "lisons", "lisez", "lisent"],
    "vivre": ["vis", "vis", "vit", "vivons", "vivez", "vivent"],
    "suivre": ["suis", "suis", "suit", "suivons", "suivez", "suivent"],
    "poursuivre": ["poursuis", "poursuis", "poursuit", "poursuivons", "poursuivez", "poursuivent"],
    "connaître": ["connais", "connais", "connaît", "connaissons", "connaissez", "connaissent"],
    "paraître": ["parais", "parais", "paraît", "paraissons", "paraissez", "paraissent"],
    "naître": ["nais", "nais", "naît", "naissons", "naissez", "naissent"],
    "mourir": ["meurs", "meurs", "meurt", "mourons", "mourez", "meurent"],
    "courir": ["cours", "cours", "court", "courons", "courez", "courent"],
    "rire": ["ris", "ris", "rit", "rions", "riez", "rient"],
    "boire": ["bois", "bois", "boit", "buvons", "buvez", "boivent"],
    # ouvrir/offrir take regular "-er" endings, not the usual
    # "-is/-is/-it/-issons/-issez/-issent" set
    "ouvrir": ["ouvre", "ouvres", "ouvre", "ouvrons", "ouvrez", "ouvrent"],
    "offrir": ["offre", "offres", "offre", "offrons", "offrez", "offrent"],
    # "-uire" family
    "traduire": ["traduis", "traduis", "traduit", "traduisons", "traduisez", "traduisent"],
    "produire": ["produis", "produis", "produit", "produisons", "produisez", "produisent"],
    "construire": ["construis", "construis", "construit", "construisons", "construisez", "construisent"],
    "détruire": ["détruis", "détruis", "détruit", "détruisons", "détruisez", "détruisent"],
    "réduire": ["réduis", "réduis", "réduit", "réduisons", "réduisez", "réduisent"],
    # "-indre" family
    "plaindre": ["plains", "plains", "plaint", "plaignons", "plaignez", "plaignent"],
    "peindre": ["peins", "peins", "peint", "peignons", "peignez", "peignent"],
    "éteindre": ["éteins", "éteins", "éteint", "éteignons", "éteignez", "éteignent"],
    "rejoindre": ["rejoins", "rejoins", "rejoint", "rejoignons", "rejoignez", "rejoignent"],
}

# "-ir" verbs that drop their stem's final consonant in the singular
# instead of the regular "-is/-is/-it" endings (dormir -> je dors, not
# "je dormis"). Plural is fully regular.
DORMIR_TYPE_VERBS = {"dormir", "sortir", "sentir", "mentir", "partir", "servir"}

# "-er" verbs whose mute "e" becomes "è" wherever that syllable gets
# the stress -- everywhere but nous/vous.
E_STEM_CHANGE_VERBS = {"acheter", "lever", "enlever", "peser", "promener"}

# same idea, but with "é" becoming "è" instead
E_ACUTE_STEM_CHANGE_VERBS = {
    "préférer", "espérer", "sécher", "précéder", "différer",
    "interpréter", "répéter", "protéger", "inquiéter",
}

# "-er" verbs that double their last consonant instead of adding an
# accent -- just have to know these, nothing predicts it (compare with
# "acheter" above, which looks the same but doesn't double).
DOUBLING_VERBS = {"appeler", "rappeler"}


def _conjugate_base(verb, pronoun_index):
    if verb in IRREGULAR_VERBS:
        return IRREGULAR_VERBS[verb][pronoun_index]

    if verb in DORMIR_TYPE_VERBS:
        if pronoun_index in (0, 1):
            return verb[:-3] + "s"
        if pronoun_index == 2:
            return verb[:-3] + "t"
        endings = ["", "", "", "ons", "ez", "ent"]
        return verb[:-2] + endings[pronoun_index]

    ending = verb[-2:]
    if ending not in ("er", "ir", "re"):
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -er/-ir/-re)")

    stem = verb[:-2]

    if ending == "er":
        if pronoun_index in (0, 1, 2, 5):
            if verb in DOUBLING_VERBS:
                stem = stem + stem[-1]
            elif verb in E_STEM_CHANGE_VERBS:
                stem = replace_last(stem, "e", "è")
            elif verb in E_ACUTE_STEM_CHANGE_VERBS:
                stem = replace_last(stem, "é", "è")
            elif stem.endswith("y"):
                stem = stem[:-1] + "i"
        elif pronoun_index == 3:
            if verb.endswith("cer"):
                stem = stem[:-1] + "ç"
            elif verb.endswith("ger"):
                stem = stem + "e"
        endings = ["e", "es", "e", "ons", "ez", "ent"]
        return stem + endings[pronoun_index]

    if ending == "ir":
        endings = ["is", "is", "it", "issons", "issez", "issent"]
        return stem + endings[pronoun_index]

    # "-re"
    endings = ["s", "s", "", "ons", "ez", "ent"]
    return stem + endings[pronoun_index]


def conjugate_present_indicative(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)
    conjugated = _conjugate_base(base_verb, pronoun_index)
    if is_reflexive:
        return reflexive_pronoun(pronoun_index, conjugated) + conjugated
    return conjugated


def is_irregular_present(verb):
    verb = verb.strip().lower()
    base_verb, _ = strip_reflexive(verb)
    return (
        base_verb in IRREGULAR_VERBS
        or base_verb in DORMIR_TYPE_VERBS
        or base_verb in E_STEM_CHANGE_VERBS
        or base_verb in E_ACUTE_STEM_CHANGE_VERBS
        or base_verb in DOUBLING_VERBS
        or (base_verb.endswith("er") and base_verb[:-2].endswith("y"))
    )

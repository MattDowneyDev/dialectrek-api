from languages.spanish.common import PRONOUNS, replace_last

# Regular preterite endings by infinitive ending.
# Note: -er and -ir verbs share IDENTICAL endings in the preterite
# (unlike present tense, where they only match in yo/tú/nosotros... wait,
# actually here they match completely).
REGULAR_ENDINGS = {
    "ar": ["é", "aste", "ó", "amos", "asteis", "aron"],
    "er": ["í", "iste", "ió", "imos", "isteis", "ieron"],
    "ir": ["í", "iste", "ió", "imos", "isteis", "ieron"],
}

# Orthographic spelling shifts -- ONLY affect the yo form in preterite
# (unlike subjunctive, where they affect every form).
# -car -> qué, -gar -> gué, -zar -> cé
SPELLING_SHIFTS_YO = {
    "car": ("c", "qu"),
    "gar": ("g", "gu"),
    "zar": ("z", "c"),
}

# -IR stem-changers (NOT -ar/-er -- those are always regular in preterite):
# change only in él/ella/usted and ellos/ustedes (indices 2 and 5),
# and it's a WEAKER version of the present-tense change: e->i, o->u.
IR_STEM_CHANGES = {
    "pedir": "e_i",
    "servir": "e_i",
    "repetir": "e_i",
    "seguir": "e_i",
    "conseguir": "e_i",
    "sentir": "e_i",
    "convertir": "e_i",
    "preferir": "e_i",
    "mentir": "e_i",
    "dormir": "o_u",
    "morir": "o_u",
}

STEM_CHANGE_MAP = {
    "e_i": ("e", "i"),
    "o_u": ("o", "u"),
}

# Verbs where an unstressed "i" between vowels becomes "y"
# (leer -> leyó/leyeron, creer -> creyó/creyeron, oír -> oyó/oyeron,
#  construir -> construyó/construyeron). Affects indices 2 and 5 only.
I_TO_Y_VERBS = {"leer", "creer", "oír", "construir", "destruir", "incluir", "influir", "caer"}

# "Strong stem" irregulars: these all share ONE special ending set
# (no accents, different vowel pattern) regardless of -ar/-er/-ir.
STRONG_PRETERITE_ENDINGS = ["e", "iste", "o", "imos", "isteis", "ieron"]

# verb -> irregular strong stem the endings above attach to
STRONG_STEMS = {
    "tener": "tuv",
    "mantener": "mantuv",
    "estar": "estuv",
    "andar": "anduv",
    "haber": "hub",
    "poder": "pud",
    "poner": "pus",
    "suponer": "supus",
    "saber": "sup",
    "caber": "cup",
    "hacer": "hic",       # note: 3rd person sing. becomes "hizo", handled below
    "querer": "quis",
    "venir": "vin",
    "decir": "dij",       # note: -j stem drops the "i" in ellos/ustedes ending
    "traer": "traj",      # same -j pattern
    "conducir": "conduj",
    "traducir": "traduj",
    "producir": "produj",
}

# Verbs whose strong stem ends in "j" drop the "i" from the -ieron ending
# (dijeron, not dijieron) and also from usted/ustedes irregular spots.
J_STEM_VERBS = {"decir", "traer", "conducir", "traducir", "producir"}

# Fully irregular / suppletive verbs (don't fit any pattern above)
IRREGULAR_VERBS = {
    "ser": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
    "ir": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],  # identical to ser!
    "dar": ["di", "diste", "dio", "dimos", "disteis", "dieron"],    # takes -er/-ir endings despite being -ar
    # ver's stem is just "v" (one letter), so the regular pattern's yo/él
    # forms -- normally accented to mark stress, e.g. "beb-í", "viv-ió" --
    # collapse to the monosyllables "ví"/"vió". Modern spelling doesn't
    # accent monosyllables (same reason "dio" and "fue" have no accent),
    # so the correct forms are "vi"/"vio".
    "ver": ["vi", "viste", "vio", "vimos", "visteis", "vieron"],
}


def apply_stem_change(stem, change_type):
    old, new = STEM_CHANGE_MAP[change_type]
    return replace_last(stem, old, new)


def conjugate_preterite_indicative(verb, pronoun_index):
    verb = verb.strip().lower()

    # 1. Fully irregular / suppletive verbs
    if verb in IRREGULAR_VERBS:
        return IRREGULAR_VERBS[verb][pronoun_index]

    ending = verb[-2:]
    if ending == "ír":
        # Accented -ír infinitives (oír, reír, ...) conjugate exactly like
        # -ir verbs -- the accent is just a stress mark on the infinitive.
        ending = "ir"
    if ending not in REGULAR_ENDINGS:
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")

    raw_stem = verb[:-2]

    # 2. Strong-stem irregulars (tener, estar, poder, decir, etc.)
    if verb in STRONG_STEMS:
        stem = STRONG_STEMS[verb]
        form = stem + STRONG_PRETERITE_ENDINGS[pronoun_index]
        if verb in J_STEM_VERBS and pronoun_index == 5:
            form = stem + "eron"  # dijeron, not dijieron
        if verb == "hacer" and pronoun_index == 2:
            form = "hizo"  # c -> z to preserve the "s" sound
        return form

    stem = raw_stem

    # 3. -ir stem-changers (weak change, only in él/ellos forms)
    if verb in IR_STEM_CHANGES and pronoun_index in (2, 5):
        stem = apply_stem_change(stem, IR_STEM_CHANGES[verb])

    # 4. i -> y spelling change between vowels (only in él/ellos forms)
    if verb in I_TO_Y_VERBS and pronoun_index in (2, 5):
        base_ending = REGULAR_ENDINGS[ending][pronoun_index]  # "ió" or "ieron"
        return stem + base_ending.replace("i", "y", 1)

    # 4b. Vowel-stem verbs (leer, caer, oír...) need an accent on the "i"
    # in tú/nosotros/vosotros to keep it a separate syllable -- leíste,
    # leímos, leísteis, not leiste, leimos, leisteis.
    if verb in I_TO_Y_VERBS and pronoun_index in (1, 3, 4):
        accented_endings = {1: "íste", 3: "ímos", 4: "ísteis"}
        return stem + accented_endings[pronoun_index]

    # 5. Orthographic spelling shift -- yo form only
    if pronoun_index == 0:
        verb_ending_3 = verb[-3:]
        if verb_ending_3 in SPELLING_SHIFTS_YO:
            old, new = SPELLING_SHIFTS_YO[verb_ending_3]
            if stem.endswith(old):
                stem = stem[:-1] + new

    # 6. Regular pattern
    return stem + REGULAR_ENDINGS[ending][pronoun_index]
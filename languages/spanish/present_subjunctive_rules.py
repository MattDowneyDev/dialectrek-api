from languages.spanish.common import (
    PRONOUNS,
    PRESENT_STEM_CHANGES as STEM_CHANGES,
    PRESENT_STEM_CHANGE_MAP as STEM_CHANGE_MAP,
    replace_last,
)

# Subjunctive endings are basically the "opposite" of indicative: -ar
# verbs get e-endings, -er/-ir verbs get a-endings. Applied to the
# subjunctive stem (see below), not the plain infinitive stem.
SUBJUNCTIVE_ENDINGS = {
    "ar": ["e", "es", "e", "emos", "éis", "en"],
    "er": ["a", "as", "a", "amos", "áis", "an"],
    "ir": ["a", "as", "a", "amos", "áis", "an"],
}

# The subjunctive stem is built from the yo form of the present
# indicative (drop the final -o), so any yo-irregularity carries
# through all six subjunctive forms, not just yo.
# verb -> irregular stem (yo indicative minus the final "o")
SUBJUNCTIVE_STEM_OVERRIDES = {
    # ver's yo present indicative is "veo" (keeps the stem vowel that
    # regular -er verbs drop), not "vo" -- without this override the
    # stem falls back to the infinitive-derived "v", giving you
    # "va/vas/va/...", which just looks like a piece of "ir" and isn't
    # a real form of ver at all.
    "ver": "ve",
    "tener": "teng",
    "hacer": "hag",
    "decir": "dig",
    "venir": "veng",
    "poner": "pong",
    "salir": "salg",
    "traer": "traig",
    "caer": "caig",
    "oír": "oig",
    "mantener": "manteng",
    "suponer": "supong",
    "conocer": "conozc",
    "conducir": "conduzc",
    "traducir": "traduzc",
}

# Stem-changing verbs: same primary change as indicative, applied to
# every form except nosotros/vosotros (indices 3 and 4). Verb list and
# vowel map are shared with present_indicative_rules (see common.py)
# -- both tenses classify these verbs identically.

# -ir stem-changers get a second, weaker change in nosotros/vosotros
# (indices 3, 4) instead of staying fully regular there.
# dormir -> durmamos/durmáis, pedir -> pidamos/pidáis, sentir -> sintamos/sintáis
SECONDARY_IR_CHANGE = {
    "e_ie": ("e", "i"),
    "o_ue": ("o", "u"),
    "e_i": ("e", "i"),  # already the same vowel, so no visible change
}

# Spelling shifts to preserve pronunciation. These apply to all six
# forms in the subjunctive (unlike indicative, where -car/-gar/-zar
# only matters in the preterite yo form).
SPELLING_SHIFTS = {
    "car": ("c", "qu"),
    "gar": ("g", "gu"),
    "zar": ("z", "c"),
}

# Fully irregular subjunctive verbs -- not derived from any indicative stem.
IRREGULAR_SUBJUNCTIVE = {
    "ser": ["sea", "seas", "sea", "seamos", "seáis", "sean"],
    "estar": ["esté", "estés", "esté", "estemos", "estéis", "estén"],
    "ir": ["vaya", "vayas", "vaya", "vayamos", "vayáis", "vayan"],
    "saber": ["sepa", "sepas", "sepa", "sepamos", "sepáis", "sepan"],
    "haber": ["haya", "hayas", "haya", "hayamos", "hayáis", "hayan"],
    "dar": ["dé", "des", "dé", "demos", "deis", "den"],
}


def apply_stem_change(stem, change_type):
    """Apply the primary present-tense stem-vowel change."""
    old, new = STEM_CHANGE_MAP[change_type]
    return replace_last(stem, old, new)


def apply_secondary_change(stem, change_type):
    """Weaker vowel change used in nosotros/vosotros for -ir stem-changers."""
    old, new = SECONDARY_IR_CHANGE[change_type]
    return replace_last(stem, old, new)


def get_subjunctive_stem(verb, stem, ending):
    """Resolve the base stem the subjunctive endings attach to,
    accounting for yo-form irregularities and -zco/-jo-type patterns."""
    if verb in SUBJUNCTIVE_STEM_OVERRIDES:
        return SUBJUNCTIVE_STEM_OVERRIDES[verb]

    # General -cer/-cir after a vowel -> zc (e.g. conocer, parecer, producir)
    if ending in ("er", "ir") and stem.endswith("c") and stem[-2:-1] in "aeiou":
        return stem[:-1] + "zc"

    # General -ger/-gir -> j, to keep the soft /x/ sound before a/o
    # (e.g. dirigir -> dirija, not the hard-g "diriga")
    if ending in ("er", "ir") and stem.endswith("g") and verb not in STEM_CHANGES:
        return stem[:-1] + "j"

    return stem


def conjugate_present_subjunctive(verb, pronoun_index):
    verb = verb.strip().lower()

    # 1. Fully irregular subjunctive verbs
    if verb in IRREGULAR_SUBJUNCTIVE:
        return IRREGULAR_SUBJUNCTIVE[verb][pronoun_index]

    ending = verb[-2:]
    if ending == "ír":
        # Accented -ír infinitives (oír, reír, ...) conjugate exactly like
        # -ir verbs -- the accent is just a stress mark on the infinitive.
        ending = "ir"
    if ending not in SUBJUNCTIVE_ENDINGS:
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")

    raw_stem = verb[:-2]
    stem = get_subjunctive_stem(verb, raw_stem, ending)

    # 2. Stem-changing verbs
    if verb in STEM_CHANGES:
        change_type = STEM_CHANGES[verb]
        if pronoun_index not in (3, 4):
            stem = apply_stem_change(stem, change_type)
        elif ending == "ir":
            # -ir verbs still change (weaker) in nosotros/vosotros
            stem = apply_secondary_change(stem, change_type)

        # -guir verbs (seguir, conseguir): the e->i change leaves a silent
        # "u" sitting before an "a"-type ending -- "sigu"+"a" would read
        # as "sigua" (/sigwa/), but it needs to be "siga". Every present-
        # subjunctive -ir ending starts with "a", so this hits all six
        # forms here, unlike the indicative where it's yo-form only.
        if verb.endswith("guir") and stem.endswith("gu"):
            stem = stem[:-1]

    # 3. Orthographic spelling shifts (-car/-gar/-zar), applies to all forms
    verb_ending_3 = verb[-3:]
    if verb_ending_3 in SPELLING_SHIFTS:
        old, new = SPELLING_SHIFTS[verb_ending_3]
        if stem.endswith(old):
            stem = stem[:-1] + new

    # 4. Apply subjunctive endings
    return stem + SUBJUNCTIVE_ENDINGS[ending][pronoun_index]
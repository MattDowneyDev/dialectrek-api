from languages.spanish.common import PRONOUNS

# The imperfect subjunctive stem is ALWAYS derived from the preterite
# "ellos/ustedes" form: drop the "-ron" ending, and what's left is the stem.
#   hablar  -> hablaron -> stem "habla"
#   comer   -> comieron -> stem "comie"
#   tener   -> tuvieron -> stem "tuvie"
#   decir   -> dijeron  -> stem "dije"
# This single rule absorbs ALL preterite irregularity (strong stems,
# stem-changers, i->y verbs, everything) automatically -- no separate
# irregular table needed here.

# Two equally correct endings sets exist in Spanish (-ra and -se forms).
# -ra is far more common in everyday speech (Latin America + most of Spain),
# -se is more literary/formal. Default to -ra; expose -se as an option.
ENDINGS_RA = ["ra", "ras", "ra", "'ramos", "rais", "ran"]
ENDINGS_SE = ["se", "ses", "se", "'semos", "seis", "sen"]

# Note: nosotros form always carries a written accent on the syllable
# before the ending (habláramos, tuviéramos, dijéramos) because adding
# a syllable shifts the natural stress. We handle that accent placement
# separately below rather than baking it into the ending string.


def get_preterite_ellos_stem(verb, preterite_ellos_form):
    """Strip the '-ron' off the preterite ellos/ustedes form to get
    the imperfect subjunctive stem. This is where all irregularity
    from the preterite naturally carries over."""
    if not preterite_ellos_form.endswith("ron"):
        raise ValueError(f"Unexpected preterite ellos form: {preterite_ellos_form}")
    return preterite_ellos_form[:-3]


def add_stress_accent(stem):
    """Add the accent mark required on the nosotros form, on the vowel
    right before where the ending attaches (e.g. hablara -> habláramos,
    tuviera -> tuviéramos, dijera -> dijéramos)."""
    accent_map = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
    if not stem:
        return stem
    last_char = stem[-1]
    if last_char in accent_map:
        return stem[:-1] + accent_map[last_char]
    return stem  # fallback, shouldn't normally hit this


def conjugate_imperfect_subjunctive(verb, pronoun_index, form="ra", preterite_lookup=None):
    """
    preterite_lookup: a function(verb) -> preterite ellos/ustedes form,
    e.g. your existing conjugate_preterite(verb, 5). Passing this in
    keeps this module decoupled from your preterite engine, but wired
    together they give you the full irregularity chain for free.
    """
    verb = verb.strip().lower()

    if preterite_lookup is None:
        raise ValueError("preterite_lookup function is required")

    preterite_ellos = preterite_lookup(verb)
    stem = get_preterite_ellos_stem(verb, preterite_ellos)

    endings = ENDINGS_RA if form == "ra" else ENDINGS_SE

    if pronoun_index == 3:  # nosotros needs the mid-word accent
        accented_stem = add_stress_accent(stem)
        return accented_stem + endings[3].replace("'", "")

    return stem + endings[pronoun_index].replace("'", "")
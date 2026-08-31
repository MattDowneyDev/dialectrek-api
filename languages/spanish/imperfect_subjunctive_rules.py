from languages.spanish.common import PRONOUNS

# The stem always comes from the preterite ellos/ustedes form: drop
# the "-ron" and that's it.
#   hablar  -> hablaron -> stem "habla"
#   comer   -> comieron -> stem "comie"
#   tener   -> tuvieron -> stem "tuvie"
#   decir   -> dijeron  -> stem "dije"
# That one rule pulls in every bit of preterite irregularity for free
# (strong stems, stem-changers, i->y verbs, all of it) -- no separate
# irregular table needed here.

# Two valid endings sets: -ra (much more common in everyday speech,
# both Latin America and most of Spain) and -se (more literary/formal).
# Default to -ra, expose -se as an option.
ENDINGS_RA = ["ra", "ras", "ra", "'ramos", "rais", "ran"]
ENDINGS_SE = ["se", "ses", "se", "'semos", "seis", "sen"]

# nosotros always gets a written accent on the syllable before the
# ending (habláramos, tuviéramos, dijéramos) since adding a syllable
# shifts the stress. Handled separately below instead of baked into
# the ending string.


def get_preterite_ellos_stem(verb, preterite_ellos_form):
    """Strip "-ron" off the preterite ellos/ustedes form -- that's the
    stem. All the preterite's irregularity just carries over for free."""
    if not preterite_ellos_form.endswith("ron"):
        raise ValueError(f"Unexpected preterite ellos form: {preterite_ellos_form}")
    return preterite_ellos_form[:-3]


def add_stress_accent(stem):
    """Accent the vowel right before where the nosotros ending
    attaches (hablara -> habláramos, tuviera -> tuviéramos, dijera ->
    dijéramos)."""
    accent_map = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
    if not stem:
        return stem
    last_char = stem[-1]
    if last_char in accent_map:
        return stem[:-1] + accent_map[last_char]
    return stem  # fallback, shouldn't normally hit this


def conjugate_imperfect_subjunctive(verb, pronoun_index, form="ra", preterite_lookup=None):
    """preterite_lookup is a function(verb) -> preterite ellos/ustedes
    form, e.g. conjugate_preterite_indicative(verb, 5). Keeps this
    module decoupled from the preterite engine, but wire them together
    and the whole irregularity chain just flows through for free."""
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
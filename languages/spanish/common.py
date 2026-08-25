"""Shared building blocks reused across the Spanish tense/mood rule sets."""

PRONOUNS = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ustedes"]


def replace_last(stem, old, new):
    """Replace the LAST occurrence of `old` in `stem` with `new`."""
    idx = stem.rfind(old)
    if idx == -1:
        return stem  # fallback: no change found
    return stem[:idx] + new + stem[idx + len(old):]


# Present-tense stem-changing verbs and their vowel patterns. Shared by
# present_indicative_rules and present_subjunctive_rules: both tenses
# classify the exact same verbs into the exact same four change types.
PRESENT_STEM_CHANGE_MAP = {
    "e_ie": ("e", "ie"),
    "o_ue": ("o", "ue"),
    "e_i": ("e", "i"),
    "u_ue": ("u", "ue"),
}

PRESENT_STEM_CHANGES = {
    "pensar": "e_ie",
    "querer": "e_ie",
    "empezar": "e_ie",
    "entender": "e_ie",
    "comenzar": "e_ie",
    "convertir": "e_ie",
    "perder": "e_ie",
    "sentir": "e_ie",
    "dormir": "o_ue",
    "poder": "o_ue",
    "volver": "o_ue",
    "contar": "o_ue",
    "encontrar": "o_ue",
    "morir": "o_ue",
    "recordar": "o_ue",
    "pedir": "e_i",
    "servir": "e_i",
    "repetir": "e_i",
    "seguir": "e_i",
    "conseguir": "e_i",
    "jugar": "u_ue",
}


def apply_present_stem_change(stem, change_type):
    """Apply a present-tense stem-vowel change (e.g. e->ie, o->ue)."""
    old, new = PRESENT_STEM_CHANGE_MAP[change_type]
    return replace_last(stem, old, new)

"""Shared building blocks reused across the French tense/mood rule sets."""

PRONOUNS = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]
PRONOUNS_ENGLISH = ["I", "you", "he/she/one", "we", "you all", "they"]

REFLEXIVE_PRONOUNS = ["me", "te", "se", "nous", "vous", "se"]

# letters that trigger elision of a reflexive pronoun ("se" -> "s'") --
# mute 'h' counts as a vowel here
ELIDABLE_STARTS = set("aeiouyhàâéèêëîïôùûœ")


def replace_last(stem, old, new):
    """Replace the LAST occurrence of `old` in `stem` with `new`."""
    idx = stem.rfind(old)
    if idx == -1:
        return stem  # fallback: no change found
    return stem[:idx] + new + stem[idx + len(old):]


def strip_reflexive(verb):
    """Split a reflexive infinitive ("se lever", "s'habiller") into its
    base infinitive ("lever", "habiller") and whether it was reflexive."""
    if verb.startswith("s'"):
        return verb[2:], True
    if verb.startswith("se "):
        return verb[3:], True
    return verb, False


def reflexive_pronoun(pronoun_index, conjugated_form):
    """The reflexive pronoun to prefix onto an already-conjugated base
    verb form, eliding to "m'"/"t'"/"s'" before a vowel sound."""
    pronoun = REFLEXIVE_PRONOUNS[pronoun_index]
    if pronoun in ("me", "te", "se") and conjugated_form[:1].lower() in ELIDABLE_STARTS:
        return pronoun[0] + "'"
    return pronoun + " "

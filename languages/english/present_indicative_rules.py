"""
English Present Tense (Third-Person Singular) -- Display Rules
------------------------------------------------------------------
This isn't a full English conjugator. Present tense in English is
identical to the infinitive for every person except "he/she/it"
(pronoun index 2), so the only real job here is producing that one
third-person form.

The dataset's `infinitive_english` values can be short phrases
("go out", "be able to") or list multiple translations separated by
"/" ("get up/raise"). Only the FIRST WORD of the chosen phrase is the
verb -- the "-s" belongs there, not glued onto the end of the whole
phrase ("go out" -> "goes out", never "go outs").
"""

# True exceptions to the regular spelling rules below. "do" and "go"
# are irregular in speech but land on the right spelling ("does",
# "goes") via the plain -o/-es rule, so they don't need an entry here.
IRREGULAR_THIRD_PERSON = {
    "be": "is",
    "have": "has",
}


def conjugate_third_person_word(verb: str) -> str:
    """Third-person singular present tense of a single verb word."""
    if verb in IRREGULAR_THIRD_PERSON:
        return IRREGULAR_THIRD_PERSON[verb]
    if verb.endswith(("o", "ch", "sh", "x", "z", "s")):
        return verb + "es"
    if verb.endswith("y") and verb[-2:-1] not in "aeiou":
        return verb[:-1] + "ies"
    return verb + "s"


def conjugate_present(infinitive_english: str, pronoun_index: int) -> str:
    """Naive present-tense conjugation of an English gloss, used only
    for display. Picks the first "/"-separated translation; only the
    third-person-singular form (pronoun_index == 2) differs from the
    infinitive."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    if pronoun_index != 2:
        return base

    verb, _, rest = base.partition(" ")
    conjugated_verb = conjugate_third_person_word(verb)
    return f"{conjugated_verb} {rest}" if rest else conjugated_verb


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to eat", 2, "eats"),
        ("to go out", 2, "goes out"),
        ("to look for", 2, "looks for"),
        ("to ask for", 2, "asks for"),
        ("to take out", 2, "takes out"),
        ("to turn out", 2, "turns out"),
        ("to get up/raise", 2, "gets up"),
        ("to be", 2, "is"),
        ("to be born", 2, "is born"),
        ("to be able to", 2, "is able to"),
        ("to have", 2, "has"),
        ("to do", 2, "does"),
        ("to go", 2, "goes"),
        ("to study", 2, "studies"),
        ("to eat", 0, "eat"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_present(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

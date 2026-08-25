"""
English Present Tense -- Display Rules
------------------------------------------------------------------
This isn't a full English conjugator. For nearly every English verb,
present tense is identical to the infinitive for every person except
"he/she/it" (pronoun index 2) -- so mostly the only real job here is
producing that one third-person form.

The one true exception is "be": am / are / is / are / are / are
varies across ALL SIX persons, not just the third-person singular, so
it needs its own per-pronoun table rather than the single-override
trick that works for every other verb ("have" -> "has", etc.).

The dataset's `infinitive_english` values can be short phrases
("go out", "be able to") or list multiple translations separated by
"/" ("get up/raise"). Only the FIRST WORD of the chosen phrase is the
verb -- the ending belongs there, not glued onto the end of the whole
phrase ("go out" -> "goes out", never "go outs").
"""

# True exceptions to the regular spelling rules below, for the
# third-person-singular form. "do" and "go" are irregular in speech
# but land on the right spelling ("does", "goes") via the plain
# -o/-es rule, so they don't need an entry here.
IRREGULAR_THIRD_PERSON = {
    "have": "has",
}

# "be" is irregular across every person, matching PRONOUNS order:
# yo, tú, él/ella/usted, nosotros, vosotros, ellos/ustedes.
BE_PRESENT_FORMS = ["am", "are", "is", "are", "are", "are"]


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
    for display. Picks the first "/"-separated translation; for every
    verb but "be", only the third-person-singular form (pronoun_index
    == 2) differs from the infinitive."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")

    if verb == "be":
        conjugated_verb = BE_PRESENT_FORMS[pronoun_index]
    elif pronoun_index == 2:
        conjugated_verb = conjugate_third_person_word(verb)
    else:
        return base

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
        ("to be", 0, "am"),
        ("to be", 1, "are"),
        ("to be", 2, "is"),
        ("to be", 3, "are"),
        ("to be", 4, "are"),
        ("to be", 5, "are"),
        ("to be able to", 5, "are able to"),
        ("to be born", 0, "am born"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_present(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

"""Not a full English conjugator. For nearly every verb, present tense
matches the infinitive except for he/she/it (pronoun index 2), so
really the only job here is producing that one third-person form.

"be" is the real exception: am/are/is/are/are/are varies across all
six persons, not just third-person singular, so it gets its own
per-pronoun table instead of the single-override trick used for
everything else ("have" -> "has", etc).

`infinitive_english` values can be short phrases ("go out", "be able
to") or multiple translations separated by "/" ("get up/raise"). Only
the first word of the chosen phrase is the verb -- the ending goes
there, not glued onto the whole phrase ("go out" -> "goes out", never
"go outs").
"""

# actual exceptions to the third-person spelling rule below -- "do"
# and "go" are irregular in speech but the plain -o/-es rule already
# spells them right ("does", "goes"), so they don't need an entry
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
    """Rough present-tense conjugation of an English gloss, display
    only. Takes the first "/"-separated translation; for every verb
    but "be", only third-person-singular (pronoun_index == 2) differs
    from the infinitive."""
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

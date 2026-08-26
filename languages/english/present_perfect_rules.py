"""
English Present Perfect -- Display Rules
------------------------------------------------------------------
The Spanish present perfect ("he hablado") reads as English "have
spoken", not the simple past ("spoke") the preterite already covers.
So this tense is "have"/"has" -- matching person, with the same
third-person-singular exception the present tense uses for "have"
itself -- plus the verb's past participle.

Unlike the imperfect's "was/were" + gerund, "be" doesn't need special
handling here: "have been able to" and "has been born" are both
ordinary, correct English, since a past participle ("been") composes
naturally with what follows it in a way a gerund ("being") doesn't.
"""

from languages.english.participle_rules import conjugate_past_participle_word

HAVE_THIRD_PERSON = "has"


def conjugate_present_perfect(infinitive_english: str, pronoun_index: int) -> str:
    """Naive present-perfect conjugation of an English gloss, used only
    for display. Picks the first "/"-separated translation; only the
    verb's first word takes the participle, since any words after it
    (phrasal particles like "out"/"up"/"for") never change."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")
    have_form = HAVE_THIRD_PERSON if pronoun_index == 2 else "have"
    participle = conjugate_past_participle_word(verb)

    return f"{have_form} {participle} {rest}" if rest else f"{have_form} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to walk", 0, "have walked"),
        ("to speak", 0, "have spoken"),
        ("to speak", 2, "has spoken"),
        ("to go out", 2, "has gone out"),
        ("to look for", 0, "have looked for"),
        ("to get up/raise", 0, "have gotten up"),
        ("to be", 0, "have been"),
        ("to be", 2, "has been"),
        ("to be able to", 5, "have been able to"),
        ("to be born", 0, "have been born"),
        ("to have", 0, "have had"),
        ("to die", 0, "have died"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_present_perfect(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

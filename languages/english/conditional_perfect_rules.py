"""Just "would have" + the past participle, same across all six
persons -- "would" doesn't vary by person here, same as the plain
conditional.
"""

from languages.english.participle_rules import conjugate_past_participle_word


def conjugate_conditional_perfect(infinitive_english: str, pronoun_index: int) -> str:
    """Rough conditional-perfect conjugation of an English gloss,
    display only. Takes the first "/"-separated translation; only the
    verb's first word takes the participle form -- phrasal particles
    like "out"/"up"/"for" never change. pronoun_index is unused, just
    kept for interface consistency with the other conjugate_*
    functions."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")
    participle = conjugate_past_participle_word(verb)
    conjugated = f"{participle} {rest}" if rest else participle

    return f"would have {conjugated}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to speak/talk", 0, "would have spoken"),
        ("to go out", 2, "would have gone out"),
        ("to be", 0, "would have been"),
        ("to be born", 0, "would have been born"),
        ("to be able to", 5, "would have been able to"),
        ("to get up/raise", 0, "would have gotten up"),
        ("to write", 0, "would have written"),
        ("to see", 0, "would have seen"),
        ("to have", 0, "would have had"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_conditional_perfect(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

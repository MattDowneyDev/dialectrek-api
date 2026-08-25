"""
English Future Perfect -- Display Rules
------------------------------------------------------------------
"will have" + the past participle (participle_rules), unchanged
across all six persons -- just like the plain future, "will" never
varies by person here either.
"""

from languages.english.participle_rules import conjugate_past_participle_word


def conjugate_future_perfect(infinitive_english: str, pronoun_index: int) -> str:
    """Naive future-perfect conjugation of an English gloss, used only
    for display. Picks the first "/"-separated translation; only the
    verb's first word takes the participle form, since any words after
    it (phrasal particles like "out"/"up"/"for") never change.
    pronoun_index is accepted only for interface consistency with the
    other conjugate_* functions."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")
    participle = conjugate_past_participle_word(verb)
    conjugated = f"{participle} {rest}" if rest else participle

    return f"will have {conjugated}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to speak/talk", 0, "will have spoken"),
        ("to go out", 2, "will have gone out"),
        ("to be", 0, "will have been"),
        ("to be born", 0, "will have been born"),
        ("to be able to", 5, "will have been able to"),
        ("to get up/raise", 0, "will have gotten up"),
        ("to write", 0, "will have written"),
        ("to see", 0, "will have seen"),
        ("to have", 0, "will have had"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_future_perfect(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

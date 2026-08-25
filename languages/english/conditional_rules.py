"""
English Conditional -- Display Rules
------------------------------------------------------------------
"would" + the base form of the verb, unchanged across all six
persons ("I would eat", "she would eat", "we would eat", ...) --
so unlike present/past tense, there's no per-person form to work
out here at all, just the infinitive stripped of "to".
"""


def conjugate_conditional(infinitive_english: str, pronoun_index: int) -> str:
    """Naive conditional conjugation of an English gloss, used only for
    display. Picks the first "/"-separated translation; "would" never
    varies by person, so pronoun_index is accepted only for interface
    consistency with the other conjugate_* functions."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    return f"would {base}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to eat", 0, "would eat"),
        ("to go out", 2, "would go out"),
        ("to be", 0, "would be"),
        ("to be able to", 5, "would be able to"),
        ("to get up/raise", 0, "would get up"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_conditional(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

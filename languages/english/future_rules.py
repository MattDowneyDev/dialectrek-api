"""
English Future -- Display Rules
------------------------------------------------------------------
"will" + the base form of the verb, unchanged across all six persons
("I will eat", "she will eat", "we will eat", ...) -- so unlike
present/past tense, there's no per-person form to work out here at
all, just the infinitive stripped of "to".
"""


def conjugate_future(infinitive_english: str, pronoun_index: int) -> str:
    """Naive future conjugation of an English gloss, used only for
    display. Picks the first "/"-separated translation; "will" never
    varies by person, so pronoun_index is accepted only for interface
    consistency with the other conjugate_* functions."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    return f"will {base}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to eat", 0, "will eat"),
        ("to go out", 2, "will go out"),
        ("to be", 0, "will be"),
        ("to be able to", 5, "will be able to"),
        ("to get up/raise", 0, "will get up"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_future(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

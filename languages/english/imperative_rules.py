"""
English Imperative -- Display Rules
------------------------------------------------------------------
English commands are just the bare verb ("speak!"), negated with
"don't" ("don't speak!") -- no per-person variation at all, except
"nosotros" ("let's speak" / "let's not speak"), which is really a
suggestion rather than a command aimed at someone else.
"""

# Pronoun index for "nosotros", matching PRONOUNS index order. It's
# the only person whose English phrasing ("let's ...") differs from
# every other person's ("...!" / "don't ...!").
NOSOTROS_INDEX = 3


def conjugate_imperative(infinitive_english: str, pronoun_index: int, polarity: str) -> str:
    """Naive imperative conjugation of an English gloss, used only for
    display. Picks the first "/"-separated translation; only the
    verb's first word is conjugated, since any words after it
    (phrasal particles like "out"/"up"/"for") never change."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    if pronoun_index == NOSOTROS_INDEX:
        return f"let's not {base}" if polarity == "negative" else f"let's {base}"
    return f"don't {base}" if polarity == "negative" else base


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to speak/talk", 1, "affirmative", "speak"),
        ("to speak/talk", 1, "negative", "don't speak"),
        ("to speak/talk", 3, "affirmative", "let's speak"),
        ("to speak/talk", 3, "negative", "let's not speak"),
        ("to go out", 2, "affirmative", "go out"),
        ("to go out", 5, "negative", "don't go out"),
        ("to be", 1, "affirmative", "be"),
        ("to be born", 1, "negative", "don't be born"),
    ]
    for infinitive, idx, polarity, expected in tests:
        result = conjugate_imperative(infinitive, idx, polarity)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] {polarity} = {result!r}  [{status}]")

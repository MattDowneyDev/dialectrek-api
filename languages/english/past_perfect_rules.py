"""Just "had" + the past participle, same across all six persons --
"had" never varies by person, same as "would (have)"/"will (have)".

English collapses several Spanish past-perfect tenses (preterite
perfect, pluperfect indicative, pluperfect subjunctive) into this one
gloss -- no separate "anterior" tense, no subjunctive distinction for
the pluperfect, so all three share this function.
"""

from languages.english.participle_rules import conjugate_past_participle_word


def conjugate_past_perfect(infinitive_english: str, pronoun_index: int) -> str:
    """Rough past-perfect conjugation of an English gloss, display
    only. Takes the first "/"-separated translation; only the verb's
    first word takes the participle form -- phrasal particles like
    "out"/"up"/"for" never change. pronoun_index is unused, just kept
    for interface consistency with the other conjugate_* functions."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")
    participle = conjugate_past_participle_word(verb)
    conjugated = f"{participle} {rest}" if rest else participle

    return f"had {conjugated}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to speak/talk", 0, "had spoken"),
        ("to go out", 2, "had gone out"),
        ("to be", 0, "had been"),
        ("to be born", 0, "had been born"),
        ("to be able to", 5, "had been able to"),
        ("to get up/raise", 0, "had gotten up"),
        ("to write", 0, "had written"),
        ("to see", 0, "had seen"),
        ("to have", 0, "had had"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_past_perfect(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

"""Needed for the conditional perfect gloss ("would have spoken"). For
regular verbs the participle matches the simple past (walked/walked),
and that holds for most of this app's irregulars too (brought/brought,
found/found, had/had, ...) -- conjugate_past_word already gets those
right.

Only the handful of verbs whose participle actually differs from
their simple-past spelling (spoke -> spoken, saw -> seen, went ->
gone, ...) need an entry below.
"""

from languages.english.preterite_indicative_rules import conjugate_past_word

# verbs whose participle differs from conjugate_past_word's simple-past form
IRREGULAR_PAST_PARTICIPLES = {
    "begin": "begun",
    "come": "come",
    "do": "done",
    "fall": "fallen",
    "get": "gotten",
    "give": "given",
    "go": "gone",
    "know": "known",
    "run": "run",
    "see": "seen",
    "speak": "spoken",
    "take": "taken",
    "write": "written",
}

# "be"'s participle is invariable, unlike its person-dependent simple
# past ("was"/"were").
BE_PAST_PARTICIPLE = "been"


def conjugate_past_participle_word(verb: str) -> str:
    """Past participle of a single (non-"be") verb word."""
    if verb == "be":
        return BE_PAST_PARTICIPLE
    if verb in IRREGULAR_PAST_PARTICIPLES:
        return IRREGULAR_PAST_PARTICIPLES[verb]
    return conjugate_past_word(verb)


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("walk", "walked"),
        ("study", "studied"),
        ("bring", "brought"),
        ("find", "found"),
        ("have", "had"),
        ("be", "been"),
        ("begin", "begun"),
        ("come", "come"),
        ("do", "done"),
        ("fall", "fallen"),
        ("get", "gotten"),
        ("give", "given"),
        ("go", "gone"),
        ("know", "known"),
        ("run", "run"),
        ("see", "seen"),
        ("speak", "spoken"),
        ("take", "taken"),
        ("write", "written"),
    ]
    for verb, expected in tests:
        result = conjugate_past_participle_word(verb)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} = {result}  [{status}]")

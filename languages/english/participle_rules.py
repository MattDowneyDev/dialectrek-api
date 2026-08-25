"""
English Past Participle -- Display Rules
------------------------------------------------------------------
Needed for the conditional perfect gloss ("would have spoken"). For
regular verbs the past participle is spelled identically to the
simple past (walked/walked), and that's true for most of this app's
irregular verbs too (brought/brought, found/found, had/had, ...) --
so conjugate_past_word already gets those right.

Only a handful of verbs need a participle that actually differs from
their simple-past spelling (spoke -> spoken, saw -> seen, went ->
gone, ...); those are the only entries that belong here.
"""

from languages.english.preterite_indicative_rules import conjugate_past_word

# Only verbs whose past participle differs from their simple-past
# form (conjugate_past_word) need an entry here.
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

# "be" -- invariable across every person, same as its simple-past
# forms are person-dependent ("was"/"were") but its participle isn't.
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

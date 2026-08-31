"""Unlike present tense, English past tense doesn't distinguish by
person at all, except "be" (was/were). So the real job here is just
picking the right past-tense spelling.

Can't derive that purely from spelling, though. Most verbs add "-ed"
(or "-d"/"-ied"), but plenty are irregular (go -> went, have -> had),
and some "regular" verbs double their final consonant depending on
where the stress falls (occur -> occurred, but enter -> entered, not
"enterred") -- not something you can read off the letters. Guessing
would silently produce wrong forms, so irregular and doubling verbs
are listed explicitly; only the genuinely predictable ones fall
through to the spelling rule.
"""

IRREGULAR_PAST = {
    "begin": "began",
    "bring": "brought",
    "come": "came",
    "do": "did",
    "fall": "fell",
    "feel": "felt",
    "find": "found",
    "get": "got",
    "give": "gave",
    "go": "went",
    "have": "had",
    "hear": "heard",
    "know": "knew",
    "leave": "left",
    "lose": "lost",
    "occur": "occurred",     # doubled consonant, stress on final syllable
    "pay": "paid",
    "permit": "permitted",   # doubled consonant, stress on final syllable
    "put": "put",
    "read": "read",          # same spelling, different pronunciation
    "run": "ran",
    "say": "said",
    "see": "saw",
    "speak": "spoke",
    "stop": "stopped",       # doubled consonant, single closed syllable
    "take": "took",
    "understand": "understood",
    "write": "wrote",
}

# "be" is the only verb that still varies by person in the past tense,
# matching PRONOUNS order: yo, tú, él/ella/usted, nosotros, vosotros,
# ellos/ustedes.
BE_PAST_FORMS = ["was", "were", "was", "were", "were", "were"]


def conjugate_past_word(verb: str) -> str:
    """Simple past tense of a single (non-"be") verb word."""
    if verb in IRREGULAR_PAST:
        return IRREGULAR_PAST[verb]
    if verb.endswith("e"):
        return verb + "d"
    if verb.endswith("y") and verb[-2:-1] not in "aeiou":
        return verb[:-1] + "ied"
    return verb + "ed"


def conjugate_past(infinitive_english: str, pronoun_index: int) -> str:
    """Rough simple-past conjugation of an English gloss, display
    only. Takes the first "/"-separated translation; only the verb's
    first word is conjugated -- phrasal particles like
    "out"/"up"/"for" never change."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")

    if verb == "be":
        conjugated_verb = BE_PAST_FORMS[pronoun_index]
    else:
        conjugated_verb = conjugate_past_word(verb)

    return f"{conjugated_verb} {rest}" if rest else conjugated_verb


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to walk", 0, "walked"),
        ("to like", 0, "liked"),
        ("to study", 0, "studied"),
        ("to stay", 0, "stayed"),
        ("to go out", 2, "went out"),
        ("to look for", 0, "looked for"),
        ("to ask for", 0, "asked for"),
        ("to get up/raise", 0, "got up"),
        ("to take out", 2, "took out"),
        ("to turn out", 0, "turned out"),
        ("to be", 0, "was"),
        ("to be", 1, "were"),
        ("to be", 2, "was"),
        ("to be", 3, "were"),
        ("to be", 4, "were"),
        ("to be", 5, "were"),
        ("to be able to", 5, "were able to"),
        ("to be born", 0, "was born"),
        ("to have", 0, "had"),
        ("to do", 0, "did"),
        ("to put", 0, "put"),
        ("to read", 0, "read"),
        ("to stop", 0, "stopped"),
        ("to occur", 0, "occurred"),
        ("to permit", 0, "permitted"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_past(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

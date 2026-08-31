"""Needed for the imperfect gloss ("was speaking"). Regular verbs just
take "-ing", with three spelling wrinkles: drop a silent trailing e
(write -> writing, but see -> seeing -- "-ee" isn't a silent-e case),
swap a trailing "-ie" for "y" (die -> dying), and double the final
consonant on a handful of one-syllable verbs to keep the vowel short
(get -> getting, stop -> stopping). Only the doubling verbs need an
entry below -- everything else falls through to the spelling rule.
"""

DOUBLED_CONSONANT_GERUNDS = {
    "begin": "beginning",
    "get": "getting",
    "occur": "occurring",
    "permit": "permitting",
    "put": "putting",
    "run": "running",
    "stop": "stopping",
}

BE_GERUND = "being"


def conjugate_gerund_word(verb: str) -> str:
    """Present participle (-ing form) of a single (non-"be") verb word."""
    if verb == "be":
        return BE_GERUND
    if verb in DOUBLED_CONSONANT_GERUNDS:
        return DOUBLED_CONSONANT_GERUNDS[verb]
    if verb.endswith("ee"):
        return verb + "ing"
    if verb.endswith("ie"):
        return verb[:-2] + "ying"
    if verb.endswith("e"):
        return verb[:-1] + "ing"
    return verb + "ing"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("walk", "walking"),
        ("study", "studying"),
        ("bring", "bringing"),
        ("come", "coming"),
        ("do", "doing"),
        ("fall", "falling"),
        ("find", "finding"),
        ("get", "getting"),
        ("give", "giving"),
        ("go", "going"),
        ("have", "having"),
        ("hear", "hearing"),
        ("know", "knowing"),
        ("leave", "leaving"),
        ("lose", "losing"),
        ("occur", "occurring"),
        ("pay", "paying"),
        ("permit", "permitting"),
        ("put", "putting"),
        ("read", "reading"),
        ("run", "running"),
        ("say", "saying"),
        ("see", "seeing"),
        ("speak", "speaking"),
        ("stop", "stopping"),
        ("take", "taking"),
        ("understand", "understanding"),
        ("write", "writing"),
        ("be", "being"),
        ("die", "dying"),
        ("lie", "lying"),
        ("tie", "tying"),
    ]
    for verb, expected in tests:
        result = conjugate_gerund_word(verb)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} = {result}  [{status}]")

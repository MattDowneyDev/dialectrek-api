"""
English Past Progressive -- Display Rules
------------------------------------------------------------------
The Spanish imperfect describes ongoing or habitual past action
("hablaba" = "was speaking"), which reads more naturally -- and
translates more instructively -- as the English past progressive
than as the simple past ("spoke") preterite already uses. So this
tense is "was/were" (matching person, same as the simple past's only
person-dependent word) plus the verb's gerund.

"be" itself is left as plain "was/were" rather than "was being",
since "be" glosses stative verbs (poder -> "to be able to") where
the progressive of "be" reads as broken English ("was being able
to"). That mirrors how the simple past also treats "be" as a bare
BE_PAST_FORMS lookup with no participle.
"""

from languages.english.gerund_rules import conjugate_gerund_word
from languages.english.preterite_indicative_rules import BE_PAST_FORMS


def conjugate_imperfect(infinitive_english: str, pronoun_index: int) -> str:
    """Naive past-progressive conjugation of an English gloss, used only
    for display. Picks the first "/"-separated translation; only the
    verb's first word takes the gerund, since any words after it
    (phrasal particles like "out"/"up"/"for") never change."""
    base = infinitive_english.split("/")[0].strip()
    if base.startswith("to "):
        base = base[3:]

    verb, _, rest = base.partition(" ")
    be_form = BE_PAST_FORMS[pronoun_index]

    if verb == "be":
        return f"{be_form} {rest}" if rest else be_form

    gerund = conjugate_gerund_word(verb)
    return f"{be_form} {gerund} {rest}" if rest else f"{be_form} {gerund}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("to walk", 0, "was walking"),
        ("to speak", 0, "was speaking"),
        ("to speak", 1, "were speaking"),
        ("to speak", 3, "were speaking"),
        ("to study", 0, "was studying"),
        ("to go out", 2, "was going out"),
        ("to look for", 0, "was looking for"),
        ("to get up/raise", 0, "was getting up"),
        ("to be", 0, "was"),
        ("to be", 3, "were"),
        ("to be able to", 5, "were able to"),
        ("to be born", 0, "was born"),
        ("to have", 0, "was having"),
    ]
    for infinitive, idx, expected in tests:
        result = conjugate_imperfect(infinitive, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{infinitive!r} [{idx}] = {result!r}  [{status}]")

"""
Spanish Future Indicative -- Rule Set
------------------------------------------
hablaré, hablarás, hablará, hablaremos, hablaréis, hablarán

Formed by attaching endings straight onto the FULL INFINITIVE (unlike
every other simple tense, which works off a stem) -- and -ar/-er/-ir
verbs all take the exact same endings, so there's only one regular
pattern to learn.

The only irregulars are a small, closed set of verbs whose stem gets
clipped or altered before the endings are added (tener -> tendr-,
hacer -> har-, etc). These are the same twelve verbs (plus their
compounds) that are irregular in the conditional tense, since both
tenses build on the same modified stem -- so this module reuses that
tense's IRREGULAR_STEMS table directly rather than duplicating it.
"""

from languages.spanish.common import PRONOUNS
from languages.spanish.conditional_indicative_rules import IRREGULAR_STEMS

# Endings are identical across -ar/-er/-ir and attach to the infinitive
# itself, not a stem stripped of its ending.
ENDINGS = ["é", "ás", "á", "emos", "éis", "án"]


def conjugate_future_indicative(verb, pronoun_index):
    verb = verb.strip().lower()

    if verb in IRREGULAR_STEMS:
        stem = IRREGULAR_STEMS[verb]
    else:
        if verb[-2:] not in ("ar", "er", "ir"):
            raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")
        stem = verb

    return stem + ENDINGS[pronoun_index]


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "hablaré"),
        ("comer", 3, "comeremos"),
        ("vivir", 5, "vivirán"),
        ("tener", 0, "tendré"),
        ("hacer", 1, "harás"),
        ("decir", 2, "dirá"),
        ("poner", 3, "pondremos"),
        ("salir", 4, "saldréis"),
        ("venir", 5, "vendrán"),
        ("poder", 0, "podré"),
        ("querer", 0, "querré"),
        ("saber", 0, "sabré"),
        ("haber", 0, "habré"),
        ("mantener", 0, "mantendré"),
        ("suponer", 0, "supondré"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_future_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} ({PRONOUNS[idx]}) = {result}  [{status}]")

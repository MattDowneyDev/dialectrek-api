"""
Spanish Conditional Indicative -- Rule Set
------------------------------------------
hablaría, hablarías, hablaría, hablaríamos, hablaríais, hablarían

Formed by attaching endings straight onto the FULL INFINITIVE (unlike
every other simple tense, which works off a stem) -- and -ar/-er/-ir
verbs all take the exact same endings, so there's only one regular
pattern to learn.

The only irregulars are a small, closed set of verbs whose stem gets
clipped or altered before the endings are added (tener -> tendr-,
hacer -> har-, etc). These are the same twelve verbs (plus their
compounds) that are irregular in the future tense, since both tenses
build on the same modified stem.
"""

from languages.spanish.common import PRONOUNS

# Endings are identical across -ar/-er/-ir and attach to the infinitive
# itself, not a stem stripped of its ending.
ENDINGS = ["ía", "ías", "ía", "íamos", "íais", "ían"]

# Irregular stems the endings above attach to, replacing the infinitive
# entirely. Closed set: no other verbs behave this way.
IRREGULAR_STEMS = {
    "decir": "dir",
    "hacer": "har",
    "poder": "podr",
    "poner": "pondr",
    "querer": "querr",
    "saber": "sabr",
    "salir": "saldr",
    "tener": "tendr",
    "valer": "valdr",
    "venir": "vendr",
    "caber": "cabr",
    "haber": "habr",
    # Compounds inherit the base verb's irregular stem.
    "mantener": "mantendr",
    "suponer": "supondr",
}


def conjugate_conditional_indicative(verb, pronoun_index):
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
        ("hablar", 0, "hablaría"),
        ("comer", 3, "comeríamos"),
        ("vivir", 5, "vivirían"),
        ("tener", 0, "tendría"),
        ("hacer", 1, "harías"),
        ("decir", 2, "diría"),
        ("poner", 3, "pondríamos"),
        ("salir", 4, "saldríais"),
        ("venir", 5, "vendrían"),
        ("poder", 0, "podría"),
        ("querer", 0, "querría"),
        ("saber", 0, "sabría"),
        ("haber", 0, "habría"),
        ("mantener", 0, "mantendría"),
        ("suponer", 0, "supondría"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_conditional_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} ({PRONOUNS[idx]}) = {result}  [{status}]")

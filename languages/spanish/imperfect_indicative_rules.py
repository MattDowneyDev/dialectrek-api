"""
Spanish Imperfect Indicative -- Rule Set
------------------------------------------
The imperfect is the most regular tense in Spanish:
  - No stem-changers (pensar, dormir, pedir all behave completely normally)
  - No orthographic spelling shifts (-car/-gar/-zar verbs are unaffected)
  - Only THREE irregular verbs in the entire language: ser, ir, ver

Because -er and -ir verbs share identical endings, there are really only
two conjugation patterns to learn: -ar, and everything else.
"""

from languages.spanish.common import PRONOUNS

# Regular endings by infinitive ending.
# Note -er and -ir are IDENTICAL here (unlike present tense).
REGULAR_ENDINGS = {
    "ar": ["aba", "abas", "aba", "ábamos", "abais", "aban"],
    "er": ["ía", "ías", "ía", "íamos", "íais", "ían"],
    "ir": ["ía", "ías", "ía", "íamos", "íais", "ían"],
}

# The only three irregular verbs in the imperfect indicative -- full stop.
IRREGULAR_VERBS = {
    "ser": ["era", "eras", "era", "éramos", "erais", "eran"],
    "ir": ["iba", "ibas", "iba", "íbamos", "ibais", "iban"],
    "ver": ["veía", "veías", "veía", "veíamos", "veíais", "veían"],
}


def conjugate_imperfect_indicative(verb, pronoun_index):
    verb = verb.strip().lower()

    # 1. The only irregulars that exist in this tense
    if verb in IRREGULAR_VERBS:
        return IRREGULAR_VERBS[verb][pronoun_index]

    ending = verb[-2:]
    if ending == "ír":
        # Accented -ír infinitives (oír, reír, ...) conjugate exactly like
        # -ir verbs -- the accent is just a stress mark on the infinitive.
        ending = "ir"
    if ending not in REGULAR_ENDINGS:
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")

    stem = verb[:-2]

    # 2. Everything else is 100% regular -- no stem changes, no spelling shifts
    return stem + REGULAR_ENDINGS[ending][pronoun_index]


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "hablaba"),
        ("comer", 3, "comíamos"),
        ("vivir", 5, "vivían"),
        ("ser", 1, "eras"),
        ("ir", 4, "ibais"),
        ("ver", 2, "veía"),
        ("pensar", 0, "pensaba"),   # note: NOT "piensaba" -- no stem change here
        ("dormir", 5, "dormían"),   # note: NOT "durmían" -- no stem change here
        ("oír", 0, "oía"),
        ("oír", 3, "oíamos"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_imperfect_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} ({PRONOUNS[idx]}) = {result}  [{status}]")
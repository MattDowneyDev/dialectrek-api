"""No "yo" form here -- you can't command yourself -- so pronoun index
0 is never valid. Callers should just skip it rather than call
conjugate_imperative with it.

Everything below is built out of pieces this app already has
elsewhere:

affirmative
  tu        -- the él/ella/usted present indicative form, except a
               small closed set of shortened irregulars (di, haz, ve,
               pon, sal, sé, ten, ven, ...)
  usted     -- él/ella/usted present subjunctive
  nosotros  -- nosotros present subjunctive ("let's ..."), except
               ir -> vamos (vayamos is the "correct" subjunctive, but
               vamos is what people actually say)
  vosotros  -- infinitive with the final -r swapped for -d, always
               regular -- no vosotros affirmative irregulars in Spanish
  ustedes   -- ellos/ustedes present subjunctive

negative
  every person, tu included, is just "no" + the matching present
  subjunctive form, no irregulars of its own. That's why "no vayas"
  (negative tu) looks nothing like "ve" (affirmative tu) -- they come
  from two completely different tenses.
"""

from languages.spanish.present_indicative_rules import conjugate_present_indicative
from languages.spanish.present_subjunctive_rules import conjugate_present_subjunctive

# tu affirmative irregulars -- shortened forms that override the
# regular él/ella/usted present indicative pattern.
IRREGULAR_TU_AFFIRMATIVE = {
    "decir": "di",
    "hacer": "haz",
    "ir": "ve",
    "poner": "pon",
    "salir": "sal",
    "ser": "sé",
    "tener": "ten",
    "venir": "ven",
    "haber": "he",
    "mantener": "mantén",
    "suponer": "supón",
}


def conjugate_imperative(verb: str, pronoun_index: int, polarity: str) -> str:
    verb = verb.strip().lower()
    if pronoun_index == 0:
        raise ValueError("The imperative has no 'yo' form.")

    if polarity == "negative":
        return f"no {conjugate_present_subjunctive(verb, pronoun_index)}"

    if pronoun_index == 1:
        if verb in IRREGULAR_TU_AFFIRMATIVE:
            return IRREGULAR_TU_AFFIRMATIVE[verb]
        return conjugate_present_indicative(verb, 2)
    if pronoun_index == 3 and verb == "ir":
        return "vamos"
    if pronoun_index == 4:
        if not verb.endswith("r"):
            raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")
        return verb[:-1] + "d"
    return conjugate_present_subjunctive(verb, pronoun_index)


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 1, "affirmative", "habla"),
        ("hablar", 1, "negative", "no hables"),
        ("hablar", 2, "affirmative", "hable"),
        ("hablar", 3, "affirmative", "hablemos"),
        ("hablar", 4, "affirmative", "hablad"),
        ("hablar", 4, "negative", "no habléis"),
        ("hablar", 5, "affirmative", "hablen"),
        ("tener", 1, "affirmative", "ten"),
        ("tener", 1, "negative", "no tengas"),
        ("mantener", 1, "affirmative", "mantén"),
        ("suponer", 1, "affirmative", "supón"),
        ("decir", 1, "affirmative", "di"),
        ("hacer", 1, "affirmative", "haz"),
        ("ir", 1, "affirmative", "ve"),
        ("ir", 1, "negative", "no vayas"),
        ("ir", 3, "affirmative", "vamos"),
        ("ir", 3, "negative", "no vayamos"),
        ("ir", 4, "affirmative", "id"),
        ("poner", 1, "affirmative", "pon"),
        ("salir", 1, "affirmative", "sal"),
        ("ser", 1, "affirmative", "sé"),
        ("ser", 1, "negative", "no seas"),
        ("venir", 1, "affirmative", "ven"),
        ("haber", 1, "affirmative", "he"),
        ("estar", 1, "affirmative", "está"),
        ("dar", 1, "affirmative", "da"),
        ("oír", 1, "affirmative", "oye"),
        ("oír", 4, "affirmative", "oíd"),
        ("pensar", 1, "affirmative", "piensa"),
        ("dormir", 1, "affirmative", "duerme"),
        ("pedir", 1, "affirmative", "pide"),
        ("seguir", 2, "affirmative", "siga"),
        ("volver", 2, "affirmative", "vuelva"),
    ]
    for verb, idx, polarity, expected in tests:
        result = conjugate_imperative(verb, idx, polarity)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] {polarity} = {result}  [{status}]")

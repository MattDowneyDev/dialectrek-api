"""había hablado, habías hablado, había hablado, habíamos hablado,
habíais hablado, habían hablado

Imperfect of "haber" (regular there -- only ser/ir/ver are irregular
in the imperfect, and haber isn't one of them) + the past participle.
Same shape as the present perfect, just a different auxiliary tense.
"""

from languages.spanish.imperfect_indicative_rules import conjugate_imperfect_indicative
from languages.spanish.participle_rules import conjugate_past_participle


def conjugate_pluperfect_indicative(verb: str, pronoun_index: int) -> str:
    auxiliary = conjugate_imperfect_indicative("haber", pronoun_index)
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "había hablado"),
        ("comer", 1, "habías comido"),
        ("vivir", 2, "había vivido"),
        ("hacer", 3, "habíamos hecho"),
        ("decir", 4, "habíais dicho"),
        ("ver", 5, "habían visto"),
        ("volver", 0, "había vuelto"),
        ("suponer", 0, "había supuesto"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_pluperfect_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

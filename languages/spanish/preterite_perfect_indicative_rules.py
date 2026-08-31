"""hube hablado, hubiste hablado, hubo hablado, hubimos hablado,
hubisteis hablado, hubieron hablado

Preterite of "haber" (stem "hub-", one of the strong-stem preterite
irregulars) + the past participle. Rare these days -- mostly literary,
always after a time conjunction like "en cuanto" or "cuando" -- but
built the same way as the other perfect compounds.
"""

from languages.spanish.preterite_indicative_rules import conjugate_preterite_indicative
from languages.spanish.participle_rules import conjugate_past_participle


def conjugate_preterite_perfect_indicative(verb: str, pronoun_index: int) -> str:
    auxiliary = conjugate_preterite_indicative("haber", pronoun_index)
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "hube hablado"),
        ("comer", 1, "hubiste comido"),
        ("vivir", 2, "hubo vivido"),
        ("hacer", 3, "hubimos hecho"),
        ("decir", 4, "hubisteis dicho"),
        ("ver", 5, "hubieron visto"),
        ("volver", 0, "hube vuelto"),
        ("suponer", 0, "hube supuesto"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_preterite_perfect_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

"""habría hablado, habrías hablado, habría hablado, habríamos hablado,
habríais hablado, habrían hablado

Conditional of "haber" + the past participle. Same shape as the
present perfect, just a different auxiliary tense -- so the only
thing that can go wrong here is an irregular participle.
"""

from languages.spanish.conditional_indicative_rules import conjugate_conditional_indicative
from languages.spanish.participle_rules import conjugate_past_participle


def conjugate_conditional_perfect_indicative(verb: str, pronoun_index: int) -> str:
    auxiliary = conjugate_conditional_indicative("haber", pronoun_index)
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "habría hablado"),
        ("comer", 1, "habrías comido"),
        ("vivir", 2, "habría vivido"),
        ("hacer", 3, "habríamos hecho"),
        ("decir", 4, "habríais dicho"),
        ("ver", 5, "habrían visto"),
        ("volver", 0, "habría vuelto"),
        ("suponer", 0, "habría supuesto"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_conditional_perfect_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

"""habré hablado, habrás hablado, habrá hablado, habremos hablado,
habréis hablado, habrán hablado

Future of "haber" + the past participle. Same shape as the present
perfect, just a different auxiliary tense -- only an irregular
participle can trip this up.
"""

from languages.spanish.future_indicative_rules import conjugate_future_indicative
from languages.spanish.participle_rules import conjugate_past_participle


def conjugate_future_perfect_indicative(verb: str, pronoun_index: int) -> str:
    auxiliary = conjugate_future_indicative("haber", pronoun_index)
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "habré hablado"),
        ("comer", 1, "habrás comido"),
        ("vivir", 2, "habrá vivido"),
        ("hacer", 3, "habremos hecho"),
        ("decir", 4, "habréis dicho"),
        ("ver", 5, "habrán visto"),
        ("volver", 0, "habré vuelto"),
        ("suponer", 0, "habré supuesto"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_future_perfect_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

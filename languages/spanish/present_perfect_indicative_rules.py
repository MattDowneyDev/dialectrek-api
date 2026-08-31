"""he hablado, has hablado, ha hablado, hemos hablado, habéis hablado,
han hablado

Present indicative of "haber" (already handled as an irregular verb in
present_indicative_rules) + the past participle. Nothing new to get
wrong here as long as those two pieces are right.
"""

from languages.spanish.present_indicative_rules import conjugate_present_indicative
from languages.spanish.participle_rules import conjugate_past_participle


def conjugate_present_perfect_indicative(verb: str, pronoun_index: int) -> str:
    auxiliary = conjugate_present_indicative("haber", pronoun_index)
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "he hablado"),
        ("comer", 1, "has comido"),
        ("vivir", 2, "ha vivido"),
        ("hacer", 3, "hemos hecho"),
        ("decir", 4, "habéis dicho"),
        ("ver", 5, "han visto"),
        ("volver", 0, "he vuelto"),
        ("leer", 0, "he leído"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_present_perfect_indicative(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

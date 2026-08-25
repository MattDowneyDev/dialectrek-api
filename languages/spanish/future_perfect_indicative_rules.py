"""
Spanish Future Perfect Indicative -- Rule Set
------------------------------------------------------
habré hablado, habrás hablado, habrá hablado, habremos hablado,
habréis hablado, habrán hablado

A compound tense: future of "haber" (future_indicative_rules) + the
past participle (participle_rules). Structurally identical to
present_perfect_indicative_rules -- just with a different auxiliary
tense -- so the only irregularity that can show up here is the same
irregular-participle irregularity that "perfect" already has.
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

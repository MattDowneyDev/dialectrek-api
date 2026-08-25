"""
Spanish Conditional Perfect Indicative -- Rule Set
------------------------------------------------------
habría hablado, habrías hablado, habría hablado, habríamos hablado,
habríais hablado, habrían hablado

A compound tense: conditional of "haber" (conditional_indicative_rules)
+ the past participle (participle_rules). Structurally identical to
present_perfect_indicative_rules -- just with a different auxiliary
tense -- so the only irregularity that can show up here is the same
irregular-participle irregularity that "perfect" already has.
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

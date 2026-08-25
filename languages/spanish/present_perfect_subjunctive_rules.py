"""
Spanish Present Perfect Subjunctive -- Rule Set
--------------------------------------------------
haya hablado, hayas hablado, haya hablado, hayamos hablado, hayáis
hablado, hayan hablado

A compound tense: present subjunctive of "haber" (already correctly
handled as one of the six fully irregular subjunctive verbs in
present_subjunctive_rules) + the past participle (participle_rules).
"""

from languages.spanish.present_subjunctive_rules import conjugate_present_subjunctive
from languages.spanish.participle_rules import conjugate_past_participle


def conjugate_present_perfect_subjunctive(verb: str, pronoun_index: int) -> str:
    auxiliary = conjugate_present_subjunctive("haber", pronoun_index)
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", 0, "haya hablado"),
        ("comer", 1, "hayas comido"),
        ("vivir", 2, "haya vivido"),
        ("hacer", 3, "hayamos hecho"),
        ("decir", 4, "hayáis dicho"),
        ("ver", 5, "hayan visto"),
        ("volver", 0, "haya vuelto"),
        ("leer", 0, "haya leído"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_present_perfect_subjunctive(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

"""
Spanish Pluperfect Subjunctive -- Rule Set
------------------------------------------------------
hubiera hablado, hubieras hablado, hubiera hablado, hubiéramos hablado,
hubierais hablado, hubieran hablado
(or, equally correct: hubiese hablado, hubieses hablado, ...)

A compound tense: imperfect subjunctive of "haber" (imperfect_subjunctive_rules)
+ the past participle (participle_rules). "haber" is a strong-stem
preterite irregular (stem "hub-", ellos/ustedes form "hubieron"), and
the imperfect subjunctive stem is always derived from that exact form
-- so the auxiliary here is fixed ("hubiera-"/"hubiese-") regardless of
which verb is being conjugated. As with every other perfect compound,
the only irregularity that can show up is an irregular participle.
"""

from languages.spanish.preterite_indicative_rules import conjugate_preterite_indicative
from languages.spanish.imperfect_subjunctive_rules import conjugate_imperfect_subjunctive
from languages.spanish.participle_rules import conjugate_past_participle


def _haber_preterite_ellos(verb: str) -> str:
    return conjugate_preterite_indicative(verb, 5)


def conjugate_pluperfect_subjunctive(verb: str, pronoun_index: int, form: str = "ra") -> str:
    auxiliary = conjugate_imperfect_subjunctive(
        "haber", pronoun_index, form=form, preterite_lookup=_haber_preterite_ellos,
    )
    participle = conjugate_past_participle(verb)
    return f"{auxiliary} {participle}"


if __name__ == "__main__":
    # quick smoke test (-ra form)
    tests = [
        ("hablar", 0, "hubiera hablado"),
        ("comer", 1, "hubieras comido"),
        ("vivir", 2, "hubiera vivido"),
        ("hacer", 3, "hubiéramos hecho"),
        ("decir", 4, "hubierais dicho"),
        ("ver", 5, "hubieran visto"),
        ("volver", 0, "hubiera vuelto"),
        ("suponer", 0, "hubiera supuesto"),
    ]
    for verb, idx, expected in tests:
        result = conjugate_pluperfect_subjunctive(verb, idx)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] = {result}  [{status}]")

    # -se form
    se_tests = [
        ("hablar", 0, "hubiese hablado"),
        ("hacer", 3, "hubiésemos hecho"),
    ]
    for verb, idx, expected in se_tests:
        result = conjugate_pluperfect_subjunctive(verb, idx, form="se")
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} [{idx}] (se) = {result}  [{status}]")

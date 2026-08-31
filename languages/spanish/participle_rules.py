"""Needed for the perfect tenses: haber (conjugated) + participle. The
participle itself is invariable here -- doesn't agree with anything,
unlike when it's used as an adjective.

Regular: -ar -> -ado (hablado), -er/-ir -> -ido (comido, vivido).

-er/-ir verbs with a stem ending in a vowel need an accent on "-ido"
to keep it a separate syllable: leer -> leído, not "leido" -- same
reason these verbs get an accent in their preterite tú/nosotros/
vosotros forms (leíste, leímos, leísteis). A "gu"/"qu" stem doesn't
count though -- that u is silent (guitar, queso), not a real vowel, so
seguir -> seguido, not "seguído" (one syllable, se-GUI-do).

The rest is a closed set of irregulars to memorize below, including
common compounds (descubrir, suponer, devolver, ...) since they
inherit their root verb's irregular participle.
"""

IRREGULAR_PARTICIPLES = {
    "abrir": "abierto",
    "cubrir": "cubierto",
    "descubrir": "descubierto",
    "decir": "dicho",
    "escribir": "escrito",
    "describir": "descrito",
    "hacer": "hecho",
    "deshacer": "deshecho",
    "satisfacer": "satisfecho",
    "morir": "muerto",
    "poner": "puesto",
    "componer": "compuesto",
    "disponer": "dispuesto",
    "exponer": "expuesto",
    "imponer": "impuesto",
    "oponer": "opuesto",
    "proponer": "propuesto",
    "suponer": "supuesto",
    "resolver": "resuelto",
    "romper": "roto",
    "ver": "visto",
    "prever": "previsto",
    "volver": "vuelto",
    "devolver": "devuelto",
    "envolver": "envuelto",
    "revolver": "revuelto",
    "imprimir": "impreso",
}


def conjugate_past_participle(verb: str) -> str:
    verb = verb.strip().lower()

    if verb in IRREGULAR_PARTICIPLES:
        return IRREGULAR_PARTICIPLES[verb]

    ending = verb[-2:]
    if ending == "ír":
        # Accented -ír infinitives (oír, reír, ...) conjugate exactly like
        # -ir verbs -- the accent is just a stress mark on the infinitive.
        ending = "ir"
    if ending not in ("ar", "er", "ir"):
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")

    stem = verb[:-2]

    if ending == "ar":
        return stem + "ado"

    if stem and stem[-1] in "aeiou" and stem[-2:] not in ("gu", "qu"):
        return stem + "ído"
    return stem + "ido"


if __name__ == "__main__":
    # quick smoke test
    tests = [
        ("hablar", "hablado"),
        ("comer", "comido"),
        ("vivir", "vivido"),
        ("abrir", "abierto"),
        ("decir", "dicho"),
        ("escribir", "escrito"),
        ("hacer", "hecho"),
        ("morir", "muerto"),
        ("poner", "puesto"),
        ("suponer", "supuesto"),
        ("ver", "visto"),
        ("volver", "vuelto"),
        ("descubrir", "descubierto"),
        ("caer", "caído"),
        ("creer", "creído"),
        ("leer", "leído"),
        ("oír", "oído"),
        ("traer", "traído"),
        ("ir", "ido"),
        ("ser", "sido"),
        ("tener", "tenido"),
        ("mantener", "mantenido"),
        ("seguir", "seguido"),
        ("conseguir", "conseguido"),
    ]
    for verb, expected in tests:
        result = conjugate_past_participle(verb)
        status = "OK" if result == expected else f"MISMATCH (expected {expected})"
        print(f"{verb} = {result}  [{status}]")

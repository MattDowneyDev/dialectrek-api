"""
Spanish Past Participle -- Rule Set
------------------------------------------
Needed to build the perfect tenses: haber (conjugated) + participle
(invariable -- it doesn't agree with anything here, unlike when a
participle is used as an adjective).

Regular formation:
  -ar verbs   -> -ado   (hablar -> hablado)
  -er/-ir     -> -ido   (comer -> comido, vivir -> vivido)

-er/-ir verbs whose stem ends in a vowel need an accent on that "-ido"
to keep it a separate syllable: leer -> leído, not "leido". This is
the same phonological rule that shows up in these same verbs' preterite
tú/nosotros/vosotros forms (leíste, leímos, leísteis).

Exception: a stem ending in "gu" or "qu" doesn't count -- that "u" is
the silent one from the hard-g/k spelling convention (guitar, queso),
not a real vowel forming a hiatus with the "i" that follows. seguir ->
seguido, not "seguído" (it's pronounced se-GUI-do, one syllable "gui").

A small closed set of participles is fully irregular and has to be
memorized; this table also carries their common compounds (descubrir,
suponer, devolver, ...) since a compound verb inherits its root verb's
irregularity here.
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

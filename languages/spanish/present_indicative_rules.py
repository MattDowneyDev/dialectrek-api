from languages.spanish.common import (
    PRONOUNS,
    PRESENT_STEM_CHANGES as STEM_CHANGES,
    apply_present_stem_change as apply_stem_change,
)

# Regular endings by infinitive ending, keyed by pronoun index (0-5)
REGULAR_ENDINGS = {
    "ar": ["o", "as", "a", "amos", "áis", "an"],
    "er": ["o", "es", "e", "emos", "éis", "en"],
    "ir": ["o", "es", "e", "imos", "ís", "en"],
}

# Fully irregular verbs: verb -> list of 6 forms matching PRONOUNS order
IRREGULAR_VERBS = {
    "ser": ["soy", "eres", "es", "somos", "sois", "son"],
    "estar": ["estoy", "estás", "está", "estamos", "estáis", "están"],
    "ir": ["voy", "vas", "va", "vamos", "vais", "van"],
    "haber": ["he", "has", "ha", "hemos", "habéis", "han"],
    "tener": ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"],
    "hacer": ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"],
    "decir": ["digo", "dices", "dice", "decimos", "decís", "dicen"],
    "venir": ["vengo", "vienes", "viene", "venimos", "venís", "vienen"],
    "saber": ["sé", "sabes", "sabe", "sabemos", "sabéis", "saben"],
    "dar": ["doy", "das", "da", "damos", "dais", "dan"],
    "ver": ["veo", "ves", "ve", "vemos", "veis", "ven"],
    "poner": ["pongo", "pones", "pone", "ponemos", "ponéis", "ponen"],
    "salir": ["salgo", "sales", "sale", "salimos", "salís", "salen"],
    "mantener": ["mantengo", "mantienes", "mantiene", "mantenemos", "mantenéis", "mantienen"],
    "suponer": ["supongo", "supones", "supone", "suponemos", "suponéis", "suponen"],
    "caer": ["caigo", "caes", "cae", "caemos", "caéis", "caen"],
    "traer": ["traigo", "traes", "trae", "traemos", "traéis", "traen"],
    "oír": ["oigo", "oyes", "oye", "oímos", "oís", "oyen"],
}


def conjugate_present_indicative(verb, pronoun_index):
    verb = verb.strip().lower()

    # 1. Fully irregular verbs
    if verb in IRREGULAR_VERBS:
        return IRREGULAR_VERBS[verb][pronoun_index]

    # Verb must end in -ar, -er, or -ir to proceed
    ending = verb[-2:]
    if ending not in REGULAR_ENDINGS:
        raise ValueError(f"'{verb}' doesn't look like a valid infinitive (must end in -ar/-er/-ir)")

    stem = verb[:-2]

    # 2. Stem-changing verbs (change applies to all but nosotros/vosotros)
    is_guir_stem_change = False
    if verb in STEM_CHANGES and pronoun_index not in (3, 4):
        stem = apply_stem_change(stem, STEM_CHANGES[verb])
        is_guir_stem_change = stem.endswith("gu")

    # 3. Spelling fixups that only affect the "yo" form
    if pronoun_index == 0:
        if is_guir_stem_change:
            return stem[:-1] + "o"  # drop the silent u: seguir -> sigo
        if ending in ("er", "ir") and stem.endswith("c") and stem[-2:-1] in "aeiou":
            return stem[:-1] + "zco"  # conocer -> conozco
        if ending in ("er", "ir") and stem.endswith("g") and verb not in STEM_CHANGES:
            return stem[:-1] + "jo"  # dirigir -> dirijo

    # 4. Regular pattern
    return stem + REGULAR_ENDINGS[ending][pronoun_index]

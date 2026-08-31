"""Passé composé: j'ai parlé, tu as parlé, il a parlé... / je suis
allé, tu es allé, il est allé...

Present tense of avoir or être (see ETRE_VERBS for which verbs take
être) plus the past participle. Reflexive verbs always take être no
matter what their base verb normally uses -- "lever" is avoir, but
"se lever" below is être -- so that gets checked first."""

from languages.french.common import reflexive_pronoun, strip_reflexive
from languages.french.participle_rules import conjugate_past_participle
from languages.french.present_indicative_rules import conjugate_present_indicative

# The classic "être verbs" (Dr & Mrs Vandertramp) -- everything else
# defaults to avoir. "passer" and "sortir" can go either way depending
# on meaning; our glosses ("to pass/spend time", "to go out/leave")
# read as avoir, so they're left off this list.
ETRE_VERBS = {
    "aller", "venir", "devenir", "arriver", "partir", "sortir", "entrer",
    "retourner", "rester", "tomber", "naître", "mourir",
}

# Masculine agreement by pronoun -- singular stays plain, plural adds
# "s". Only applies with être; avoir's participle never agrees.
AGREEMENT_ENDINGS = ["", "", "", "s", "s", "s"]


def agreed_participle(base_verb, pronoun_index, takes_etre):
    """Past participle with agreement applied if the auxiliary is être.
    Shared with the other compound tenses (pluperfect, future perfect)."""
    participle = conjugate_past_participle(base_verb)
    if takes_etre:
        participle += AGREEMENT_ENDINGS[pronoun_index]
    return participle


def conjugate_present_perfect_indicative(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)

    takes_etre = is_reflexive or base_verb in ETRE_VERBS
    auxiliary = conjugate_present_indicative("être" if takes_etre else "avoir", pronoun_index)
    participle = agreed_participle(base_verb, pronoun_index, takes_etre)

    if is_reflexive:
        return f"{reflexive_pronoun(pronoun_index, auxiliary)}{auxiliary} {participle}"
    return f"{auxiliary} {participle}"

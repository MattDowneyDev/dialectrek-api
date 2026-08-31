"""Le subjonctif passé: que j'aie parlé, que tu aies parlé... / que je
sois allé, que tu sois allé...

Same as passé composé (present_perfect_indicative_rules) -- same
avoir/être choice, same agreement, same reflexive handling -- just
with the auxiliary in the subjunctive instead of the present
indicative."""

from languages.french.common import reflexive_pronoun, strip_reflexive
from languages.french.present_perfect_indicative_rules import ETRE_VERBS, agreed_participle
from languages.french.present_subjunctive_rules import conjugate_present_subjunctive


def conjugate_present_perfect_subjunctive(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)

    takes_etre = is_reflexive or base_verb in ETRE_VERBS
    auxiliary = conjugate_present_subjunctive("être" if takes_etre else "avoir", pronoun_index)
    participle = agreed_participle(base_verb, pronoun_index, takes_etre)

    if is_reflexive:
        return f"{reflexive_pronoun(pronoun_index, auxiliary)}{auxiliary} {participle}"
    return f"{auxiliary} {participle}"

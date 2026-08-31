"""Le conditionnel passé: j'aurais parlé, tu aurais parlé... / je
serais allé, tu serais allé...

Same as passé composé (present_perfect_indicative_rules) -- same
avoir/être choice, same agreement, same reflexive handling -- just
with the auxiliary in the conditional instead of the present."""

from languages.french.common import reflexive_pronoun, strip_reflexive
from languages.french.conditional_indicative_rules import conjugate_conditional_indicative
from languages.french.present_perfect_indicative_rules import ETRE_VERBS, agreed_participle


def conjugate_conditional_perfect_indicative(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)

    takes_etre = is_reflexive or base_verb in ETRE_VERBS
    auxiliary = conjugate_conditional_indicative("être" if takes_etre else "avoir", pronoun_index)
    participle = agreed_participle(base_verb, pronoun_index, takes_etre)

    if is_reflexive:
        return f"{reflexive_pronoun(pronoun_index, auxiliary)}{auxiliary} {participle}"
    return f"{auxiliary} {participle}"

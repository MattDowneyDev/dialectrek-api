"""Le conditionnel présent: parlerais, parlerais, parlerait,
parlerions, parleriez, parleraient.

Same stem as the future simple -- irregular verbs included, envoyer ->
enverr- and all -- just with the imperfect's endings instead of the
future's. That's the whole rule; there's nothing conditional-specific
to get wrong once future_indicative_rules and imperfect_indicative_rules
are both right."""

from languages.french.common import reflexive_pronoun, strip_reflexive
from languages.french.future_indicative_rules import future_stem, is_irregular_future
from languages.french.imperfect_indicative_rules import IMPERFECT_ENDINGS


def conjugate_conditional_indicative(verb, pronoun_index):
    verb = verb.strip().lower()
    base_verb, is_reflexive = strip_reflexive(verb)
    conjugated = future_stem(base_verb) + IMPERFECT_ENDINGS[pronoun_index]
    if is_reflexive:
        return reflexive_pronoun(pronoun_index, conjugated) + conjugated
    return conjugated


# same stem, same irregulars -- just borrow future's classification
is_irregular_conditional = is_irregular_future

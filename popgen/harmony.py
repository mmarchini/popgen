
import random
from decimal import Decimal as D
from functools import partial
from operator import getitem

from scipy.stats import rv_discrete

from mingus.core import scales, chords

determine = partial(chords.determine, shorthand=True, no_inversions=True)

DEFAULT_MARKOV_CHAIN = [
    (24, 35, 0, 20, 70, 5),
    (2, 2, 5, 1, 1, 5),
    (2, 1, 0, 1, 2, 1),
    (39, 4, 85, 1, 13, 49),
    (20, 86, 2, 76, 1, 39),
    (35, 4, 8, 1, 14, 1),
]


class Harmony(object):

    def __init__(self, key="C", markov_chain=DEFAULT_MARKOV_CHAIN):
        triads = chords.triads(key)[:-1]
        self.key = [determine(t)[0] for t in triads]
        self.markov_chain = markov_chain

    def generate_chords(self):
        harmony = []
        harmony.append(random.choice(self.key))

        for i in range(3):
            probabilities = self.markov_chain[self.key.index(harmony[-1])]

            prob_sum = D(sum(probabilities))
            normalized = [prob/prob_sum for prob in probabilities]

            note = self.key[rv_discrete(values=(range(6), normalized)).rvs()]
            harmony.append(note)

        return harmony

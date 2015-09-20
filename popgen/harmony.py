
import random
from operator import itemgetter
from decimal import Decimal as D
from functools import partial

from scipy.stats import rv_discrete

from mingus.core import chords
from mingus.containers import Bar, NoteContainer

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

    def get_kicks(self, rhythm_bar):
        kicks = []
        a = dict()
        for beat in rhythm_bar.bar:
            if beat[2] is None:
                a[beat[0]] = [beat[1], None]
            elif a.get(beat[0], [32])[0] > beat[1]:
                a[beat[0]] = [beat[1], beat[2]]

        current_beat = 0
        for beat, n in sorted(a.items(), key=itemgetter(0)):
            if beat < current_beat:
                continue
            kicks.append([beat, n[0], n[1]])
            current_beat += 1/n[0]
        return kicks

    def generate_chord_bar(self, chords_, rhythm_bar):
        kicks = self.get_kicks(rhythm_bar)

        chord_bars = []
        for chord in chords_:
            chord = chords.from_shorthand(chord)
            chord = "{0}-3 {2}-4 {0}-4 {1}-5".format(*chord).split(" ")
            new_bar = Bar()
            N = lambda note: None if note is None else NoteContainer(chord)
            new_bar.bar = [[a[0], a[1], N(a[2])] for a in kicks]
            new_bar.current_beat = 1.0
            chord_bars.append(new_bar)
        return chord_bars

    def generate_bass_bar(self, chords_, rhythm_bar):
        kicks = self.get_kicks(rhythm_bar)

        chord_bars = []
        for chord in chords_:
            chord = chords.from_shorthand(chord)
            chord = ["%s-2" % chord[0]]
            new_bar = Bar()
            N = lambda note: None if note is None else NoteContainer(chord)
            new_bar.bar = [[a[0], a[1], N(a[2])] for a in kicks]
            new_bar.current_beat = 1.0
            chord_bars.append(new_bar)
        return chord_bars


import random
from decimal import Decimal as D
from functools import partial

from scipy.stats import rv_discrete

from mingus.core import chords
from mingus.containers import Bar, NoteContainer

from popgen.instruments import Instrument

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

    def __init__(self, key="C", instrument=Instrument,
                 markov_chain=DEFAULT_MARKOV_CHAIN):
        triads = chords.triads(key)[:-1]
        self.instrument = instrument
        self.key = [determine(t)[0] for t in triads]
        self.markov_chain = markov_chain

    def generate_chords(self):
        harmony = []
        harmony.append(random.choice(self.key))

        for i in range(3):
            probabilities = self.markov_chain[self.key.index(harmony[-1])]

            prob_sum = D(sum(probabilities))
            normalized = [D(prob) / prob_sum for prob in probabilities]

            note = self.key[rv_discrete(values=(range(6), normalized)).rvs()]
            harmony.append(note)

        return harmony

    def get_kicks(self, rhythm_bar):
        kicks = []
        last_beat = 0.
        for beat in filter(lambda b: b[2] is not None, rhythm_bar.bar)[1:]:
            duration = 1. / (beat[0] - last_beat)
            kicks.append([last_beat, duration, beat[1]])
            last_beat = beat[0]
        duration = 1. / (1. - last_beat)
        kicks.append([last_beat, duration, beat[1]])

        return kicks

    def generate_chord_bar(self, chords_, rhythm_bar):
        kicks = self.get_kicks(rhythm_bar)

        chord_bars = []
        for chord in chords_:
            new_bar = Bar()
            N = lambda note: None if note is None else self.instrument.chord(chord)
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

#!/usr/bin/env python


import random
from operator import itemgetter

from scipy.stats import rv_discrete

from mingus.containers import Bar, NoteContainer

from popgen.instruments import AcousticPercussion

# TEMPO_DISTRIBUTION = [
#     (60,  0.01),
#     (70,  0.03),
#     (80,  0.07),
#     (90,  0.20),
#     (100, 0.15),
#     (110, 0.24),
#     (120, 0.32),
#     (130, 0.14),
#     (140, 0.05),
#     (150, 0.01),
#     (160, 0.01),
# ]

POSITION_WEIGHT = [
    (1, 10),
    (2, 1),
    (3, 3),
    (4, 1),
    (5, 6),
    (6, 1),
    (7, 3),
    (8, 1),
    (9, 8),
    (10, 1),
    (11, 3),
    (12, 1),
    (13, 6),
    (14, 1),
    (15, 3),
    (16, 1),
]


class Rhythm(object):

    def __init__(self, tempo, instrument=AcousticPercussion):
        self.tempo = tempo
        self.instrument = instrument

    def number_of_kicks(self):
        kicks_mean = 1. + ((abs((self.tempo - 160.) / 40.)))
        kicks = int(round(random.gauss(kicks_mean, .45)))

        return kicks

    def generate_kicks(self):
        R = lambda: rv_discrete(values=[(4, 8), (0.60, 0.40)]).rvs()
        kicks = [
            (0, R())
        ]
        for i in range(self.number_of_kicks() - 1):
            duration = R()
            q = 16 / duration

            p = []
            for i in range(0, 16, q):
                if not any([i <= kick[0] < i + q for kick in kicks]):
                    p.append(i)

            kicks.append((random.choice(p), duration))
            kicks = sorted(kicks, key=itemgetter(0))
        return (self.instrument.kick, kicks)

    def generate_snares(self):
        R = lambda values: rv_discrete(values=values).rvs()
        snares = []
        for i in range(R(((1, 2, 3, 4, 0), (0.2, 0.4, 0.3, 0.09, 0.01)))):
            duration = R([(4, 8, 16), (0.5, 0.3, 0.2)])
            q = 16 / duration

            p = []
            for i in range(0, 16, q):
                if not any([i <= snare[0] < i + q for snare in snares]):
                    p.append(i)

            snares.append((random.choice(p), duration))
            snares = sorted(snares, key=itemgetter(0))
        return (self.instrument.snare, snares)

    def generate_hihats(self):
        R = lambda values: rv_discrete(values=values).rvs()
        hihats = []
        for i in range(R(((1, 2, 3, 4, 0), (0.2, 0.4, 0.3, 0.09, 0.01)))):
            duration = R([(4, 8, 16), (0.5, 0.3, 0.2)])
            q = 16 / duration

            p = []
            for i in range(0, 16, q):
                if not any([i <= ride[0] < i + q for ride in hihats]):
                    p.append(i)

            hihats.append((random.choice(p), duration))
            hihats = sorted(hihats, key=itemgetter(0))
        return (self.instrument.hi_hat, hihats)

    def generate_rides(self):
        R = lambda values: rv_discrete(values=values).rvs()
        rides = []
        for i in range(R(((1, 2, 3, 4, 0), (0.2, 0.4, 0.3, 0.09, 0.01)))):
            duration = R([(4, 8), (0.60, 0.40)])
            q = 16 / duration

            p = []
            for i in range(0, 16, q):
                if not any([i <= ride[0] < i + q for ride in rides]):
                    p.append(i)

            rides.append((random.choice(p), duration))
            rides = sorted(rides, key=itemgetter(0))
        return (self.instrument.ride, rides)

    def generate_bar(self):
        beats = [
            self.generate_kicks(),
            self.generate_rides(),
            self.generate_snares(),
            self.generate_hihats(),
        ]

        p = set()
        for instr, beat in beats:
            p |= set(map(itemgetter(0), beat))

        bar = Bar()
        for i in range(16):
            bar.place_notes(None, 16)

        for i in sorted(p):
            container = NoteContainer()
            for instr, beat in beats:
                beat = (filter(lambda b: b[0] == i, beat) or [None]).pop()
                if beat:
                    container.add_note(instr)

            bar.bar.pop(bar.bar.index([i / 16., 16, None]))
            bar.bar.append([i / 16., 16, container])
        bar.bar = sorted(bar.bar, key=itemgetter(0))
        bar.current_beat = 1.0

        return bar

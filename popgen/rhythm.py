#!/usr/bin/env python


import random

from mingus.containers import instrument
from mingus.containers import Bar, NoteContainer

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
    (1,  10),
    (2,  1),
    (3,  3),
    (4,  1),
    (5,  6),
    (6,  1),
    (7,  3),
    (8,  1),
    (9,  8),
    (10, 1),
    (11, 3),
    (12, 1),
    (13, 6),
    (14, 1),
    (15, 3),
    (16, 1),
]


class Rhythm(object):

    def __init__(self, tempo):
        self.tempo = tempo
        self.drum = instrument.MidiPercussionInstrument()

    def number_of_kicks(self):
        kicks_mean = 1.+((abs((self.tempo-160.)/40.)))
        additional_kicks = int(round(random.gauss(kicks_mean, .45)))

        return additional_kicks

    def generate_bar(self):
        bar = Bar()

        bar.place_notes(self.drum.bass_drum_1(), 4)
        while bar.current_beat < bar.length:
            duration = random.choice([4, 8, 16])

            note = NoteContainer()

            # Ride
            if duration != 16:
                if random.uniform(0, 100) < 80:
                    note.add_note(self.drum.ride_cymbal_1())

            if random.uniform(0, 100) < 80:
                note.add_note(self.drum.acoustic_snare())

            if random.uniform(0, 100) < 80:
                note.add_note(self.drum.closed_hi_hat())

            bar.place_notes(note, duration)

        return bar

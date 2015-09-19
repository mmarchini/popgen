#!/usr/bin/env python

import random

from mingus.containers import instrument
from mingus.containers import Bar, Track, Composition, NoteContainer
from mingus.midi import fluidsynth

TEMPO_DISTRIBUTION = [
    (60,  0.01),
    (70,  0.03),
    (80,  0.07),
    (90,  0.20),
    (100, 0.15),
    (110, 0.24),
    (120, 0.32),
    (130, 0.14),
    (140, 0.05),
    (150, 0.01),
    (160, 0.01),
]

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


def define_tempo():
    tempo = random.gauss(110, 20)

    return tempo


def number_of_kicks(tempo):
    kicks_mean = 1.+((abs((tempo-160.)/40.)))
    additional_kicks = int(round(random.gauss(kicks_mean, .45)))

    return additional_kicks


tempo = define_tempo()

composition = Composition()

drum = instrument.MidiPercussionInstrument()
drum_track = Track(drum)

bar = Bar()

bar.place_notes(drum.bass_drum_1(), 4)
while bar.current_beat < bar.length:
    duration = random.choice([4, 8, 16])

    note = NoteContainer()

    # Ride
    if duration != 16:
        if random.uniform(0, 100) < 80:
            note.add_note(drum.ride_cymbal_1())

    bar.place_notes(note, duration)

drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)
drum_track.add_bar(bar)

fluidsynth.init("/usr/share/sounds/sf2/FluidR3_GM.sf2", "alsa")
channel = 9
fluidsynth.set_instrument(channel, 0, 1)
fluidsynth.play_Track(drum_track, channel)

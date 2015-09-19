
import unittest

from mingus.midi import fluidsynth
from mingus.containers import Track

from popgen import rhythm, tempo


class TestRhythm(unittest.TestCase):

    def test_generation(self):
        drum_track = Track()

        rhythm_ = rhythm.Rhythm(tempo.define_tempo())
        bar = rhythm_.generate_bar()
        drum_track.add_bar(bar)
        drum_track.add_bar(bar)

        fluidsynth.init("/usr/share/sounds/sf2/FluidR3_GM.sf2", "alsa")
        channel = 9
        fluidsynth.set_instrument(channel, 0, 1)
        fluidsynth.play_Track(drum_track, channel)

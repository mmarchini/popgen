
import unittest

from mingus.containers import Track

from popgen import rhythm, tempo


class TestRhythm(unittest.TestCase):

    def test_generation(self):
        drum_track = Track()

        rhythm_ = rhythm.Rhythm(tempo.define_tempo())
        bar = rhythm_.generate_bar()
        drum_track.add_bar(bar)
        drum_track.add_bar(bar)

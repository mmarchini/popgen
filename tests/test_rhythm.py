
import random
import unittest

from numpy import random as np_random

from popgen import rhythm


class TestRhythm(unittest.TestCase):

    def setUp(self):
        self.rhythm = rhythm.Rhythm(120)
        self.drum = self.rhythm.drum

    def test_number_of_kicks_1(self):
        random.seed(5)
        assert self.rhythm.number_of_kicks() == 1

    def test_number_of_kicks_2(self):
        random.seed(3)
        assert self.rhythm.number_of_kicks() == 2

    def test_number_of_kicks_3(self):
        random.seed(1)
        assert self.rhythm.number_of_kicks() == 3

    def test_generate_kicks(self):
        random.seed(1)
        np_random.seed(1)

        kicks = (self.drum.bass_drum_1(), [(0, 4), (4, 4), (12, 8)])
        assert self.rhythm.generate_kicks() == kicks

    def test_generate_snares(self):
        random.seed(1)
        np_random.seed(1)

        snares = (self.drum.acoustic_snare(), [(2, 8), (12, 4)])
        assert self.rhythm.generate_snares() == snares

    def test_generate_hihats(self):
        random.seed(1)
        np_random.seed(1)

        hihats = (self.drum.pedal_hi_hat(), [(2, 8), (12, 4)])
        assert self.rhythm.generate_hihats() == hihats

    def test_generate_rides(self):
        random.seed(1)
        np_random.seed(1)

        rides = (self.drum.ride_cymbal_1(), [(2, 8), (12, 4)])
        assert self.rhythm.generate_rides() == rides

    def test_generrate_bar(self):
        random.seed(1)
        np_random.seed(1)

        bar = [[0.0, 4, [self.drum.bass_drum_1(), self.drum.pedal_hi_hat()]],
               [0.0625, 16, None], [0.125, 16, None], [0.1875, 16, None],
               [0.25, 4, [self.drum.bass_drum_1(), self.drum.ride_cymbal_1()]],
               [0.3125, 16, None], [0.375, 16, None], [0.4375, 16, None],
               [0.5, 4, [self.drum.acoustic_snare(), self.drum.ride_cymbal_1()]],
               [0.5625, 16, None], [0.625, 16, None], [0.6875, 16, None],
               [0.75, 8, [self.drum.bass_drum_1(), self.drum.pedal_hi_hat()]],
               [0.8125, 16, None], [0.875, 16, None], [0.9375, 16, None]]
        generated_bars = list(self.rhythm.generate_bar())
        assert generated_bars == bar

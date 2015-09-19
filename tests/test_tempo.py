import unittest

from popgen import tempo


class TestTempo(unittest.TestCase):

    def test_default_tempo(self,):
        for i in range(1000):
            t = tempo.define_tempo()
            assert 60 <= t
            assert t <= 160

    def test_lower_boundary(self,):
        for i in range(1000):
            t = tempo.define_tempo(lower=30)
            assert 30 <= t
            assert t <= 160

    def test_upper_boundary(self, ):
        for i in range(1000):
            t = tempo.define_tempo(upper=240)
            assert 60 <= t
            assert t <= 240

    def test_upper_and_lower_boundaries(self, ):
        for i in range(1000):
            t = tempo.define_tempo(lower=70, upper=100)
            assert 70 <= t
            assert t <= 100

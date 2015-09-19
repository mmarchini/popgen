
import unittest

from popgen import harmony


class TestHarmony(unittest.TestCase):

    def test_default_generation(self):
        harmony_ = harmony.Harmony()
        for i in range(1000):
            chords = harmony_.generate_chords()
            assert set(chords) <= set(['CM', 'Dm', 'Em', 'FM', 'GM', 'Am'])

    def test_E_generation(self):
        harmony_ = harmony.Harmony('E')
        for i in range(1000):
            chords = harmony_.generate_chords()
            assert set(chords) <= set(['EM', 'F#m', 'G#m', 'AM', 'BM', 'C#m'])

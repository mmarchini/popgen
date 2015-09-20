
import unittest

from mingus.containers import Note as N

from popgen import melody


class TestHarmony(unittest.TestCase):

    def test_notes_from_range(self):
        notes = [N("A-3"), N("B-3"), N("C-4"), N("D-4")]
        calculated_notes = melody.notes_from_range("C", "A-3", "D-4")
        assert notes == calculated_notes

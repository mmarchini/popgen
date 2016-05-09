
from math import ceil, floor

from mingus.core import chords
from mingus.containers import Note, NoteContainer, MidiInstrument

from popgen.utils import get_scale, notes_from_range


class Instrument(object):

    def chord(self, chord):
        chord = chords.from_shorthand(chord)
        chord = "{0}-3 {2}-4 {0}-4 {1}-4".format(*chord).split(" ")
        # chord = "{0}-3 {1}-3 {2}-3".format(*chord).split(" ")
        return NoteContainer(chord)

    @classmethod
    def get_midi_instrument(cls):
        if not cls._instrument:
            return None
        midi_instrument = MidiInstrument(name=cls._instrument)
        instr_nr = MidiInstrument.names.index(cls._instrument) + 1
        midi_instrument.instrument_nr = instr_nr

        return midi_instrument

    @classmethod
    def get_instrument_by_name(cls, instrument_name):
        if getattr(cls, '_instrument', None) == instrument_name:
            return cls
        for instr_class in cls.__subclasses__():
            instrument = instr_class.get_instrument_by_name(instrument_name)
            if instrument:
                return instrument

        return None

    @classmethod
    def get_range(cls, scale, lower, upper):
        l = Note(cls.lower)
        u = Note(cls.upper)

        next_note = l
        notes = []
        while next_note != u:
            notes.append(next_note)
            next_note = Note().from_int(int(next_note))
            next_note.augment()
            next_note = Note().from_int(int(next_note))
        notes.append(next_note)
        lower_index = int(floor(len(notes) * lower))
        upper_index = int(ceil(len(notes) * upper))
        print notes
        notes = notes[lower_index:upper_index]
        print lower, upper
        print lower_index, upper_index
        print notes

        full_scale = get_scale(scale).ascending()[:-1]
        lowest_note = "%s-1" % full_scale[0]
        highest_note = "%s-10" % full_scale[-1]
        valid_notes = notes_from_range(scale, lowest_note, highest_note)
        notes = [note for note in notes if note in valid_notes]
        lower = notes[0]
        upper = notes[-1]

        return (lower, upper)


from mingus.core import chords
from mingus.containers import NoteContainer, MidiInstrument


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

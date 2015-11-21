
from mingus.midi.midi_file_out import write_Composition
from mingus.containers import Track, MidiInstrument, Composition
# from mingus.containers.instrument import MidiPercussionInstrument

from popgen import (rhythm as rhythm_, harmony as harmony_, tempo as tempo_,
                    melody as melody_, phrase_structure as phrase_structure_)


class Composer(object):

    def __init__(self, bpm=None, rhythm=None, harmony=None, melody=None,
                 phrase_structure=None):
        self.bpm = bpm or tempo_.define_tempo()
        self.rhythm = rhythm or rhythm_.Rhythm(self.bpm)
        self.harmony = harmony or harmony_.Harmony()
        self.melody = melody or melody_.Melody()
        self.phrase_structure = phrase_structure or \
            phrase_structure_.PhraseStructure()

    def compose(self):
        self.drum_track = Track()
        self.drum_track.channel = 9
        self.drum_track.instrument = MidiInstrument()

        chords_instrumnet = MidiInstrument(name='Electric Guitar (jazz)')
        instr_nr = MidiInstrument.names.index(chords_instrumnet.name) + 1
        chords_instrumnet.instrument_nr = instr_nr
        self.chords_track = Track()
        self.chords_track.channel = 1
        self.chords_track.instrument = chords_instrumnet

        bass_instrument = MidiInstrument(name='Electric Bass (finger)')
        instr_nr = MidiInstrument.names.index(bass_instrument.name) + 1
        bass_instrument.instrument_nr = instr_nr
        self.bass_track = Track()
        self.bass_track.channel = 2
        self.bass_track.instrument = bass_instrument

        melody_instrument = MidiInstrument(name='Overdriven Guitar')
        instr_nr = MidiInstrument.names.index(melody_instrument.name) + 1
        melody_instrument.instrument_nr = instr_nr
        self.melody_track = Track()
        self.melody_track.channel = 0
        self.melody_track.instrument = melody_instrument

        drum_bar = self.rhythm.generate_bar()

        chords = self.harmony.generate_chords()
        chord_bars = self.harmony.generate_chord_bar(chords, drum_bar)
        bass_bars = self.harmony.generate_bass_bar(chords, drum_bar)

        self.melody.harmony = chords
        self.melody.phrase_structure = self.phrase_structure
        melody_bars = self.melody.generate_melody()

        for i, chord_bar in enumerate(melody_bars):
            self.chords_track.add_bar(chord_bars[i % len(chord_bars)])
            self.bass_track.add_bar(bass_bars[i % len(bass_bars)])
            self.melody_track.add_bar(melody_bars[i])
            self.drum_track.add_bar(drum_bar)

    def save(self, filename):
        composition = Composition()
        composition.add_track(self.drum_track)
        composition.add_track(self.chords_track)
        composition.add_track(self.bass_track)
        composition.add_track(self.melody_track)
        # composition.
        write_Composition(filename, composition, self.bpm)

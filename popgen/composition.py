from mingus.midi.fluidsynth import FluidSynthSequencer
from mingus.containers import Track, MidiInstrument
from mingus.containers.instrument import MidiPercussionInstrument

from popgen import (rhythm as rhythm_, harmony as harmony_, tempo as tempo_,
                    melody as melody_, phrase_structure as phrase_structure_)


class Composition(object):

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
        self.drum_track.instrument = MidiPercussionInstrument()

        chords_instrumnet = MidiInstrument(name='Eletric Guitar (jazz)')
        self.chords_track = Track()
        self.chords_track.instrument = chords_instrumnet

        bass_instrument = MidiInstrument(name='Electric Bass (finger)')
        self.bass_track = Track()
        self.bass_track.instrument = bass_instrument

        self.melody_track = Track()
        self.melody_track.instrument = MidiInstrument(name='Overdriven Guitar')

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

    def play(self, filename=None):
        fluidsynth = FluidSynthSequencer()
        if filename is not None:
            fluidsynth.start_recording(filename)
        else:
            fluidsynth.start_audio_output("alsa")
        fluidsynth.load_sound_font("arachno.sf2")
        fluidsynth.fs.program_reset()
        fluidsynth.is_general_midi = True
        fluidsynth.main_volume(0, 110)
        fluidsynth.main_volume(1, 110)
        fluidsynth.main_volume(2, 127)
        fluidsynth.main_volume(9, 110)

        fluidsynth.play_Tracks(
            [self.chords_track, self.bass_track, self.melody_track,
             self.drum_track],
            [0, 1, 2, 9],
            self.bpm
        )

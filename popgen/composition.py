from mingus.midi import fluidsynth
from mingus.containers import Track, MidiInstrument
from mingus.containers.instrument import MidiPercussionInstrument

from popgen import rhythm, harmony, tempo, melody, phrase_structure


class Composition(object):

    def compose(self):
        self.drum_track = Track()
        self.drum_track.instrument = MidiPercussionInstrument()

        chords_instrumnet = MidiInstrument(name='Electric Grand Piano')
        self.chords_track = Track()
        self.chords_track.instrument = chords_instrumnet

        bass_instrument = MidiInstrument(name='Electric Bass (finger)')
        self.bass_track = Track()
        self.bass_track.instrument = bass_instrument

        self.melody_track = Track()
        self.melody_track.instrument = MidiInstrument(name='Synth Voice')

        self.bpm = tempo.define_tempo()

        rhythm_ = rhythm.Rhythm(self.bpm)
        drum_bar = rhythm_.generate_bar()

        harmony_ = harmony.Harmony()
        chords = harmony_.generate_chords()
        chord_bars = harmony_.generate_chord_bar(chords, drum_bar)
        bass_bars = harmony_.generate_bass_bar(chords, drum_bar)

        melody_ = melody.Melody(tempo=self.bpm)
        melody_.harmony = chords
        melody_.phrase_structure = phrase_structure.PhraseStructure()
        melody_bars = melody_.generate_melody()

        for i, chord_bar in enumerate(melody_bars):
            self.chords_track.add_bar(chord_bars[i % len(chord_bars)])
            self.bass_track.add_bar(bass_bars[i % len(bass_bars)])
            self.melody_track.add_bar(melody_bars[i])
            self.drum_track.add_bar(drum_bar)

    def play(self):
        print fluidsynth.init("arachno.sf2", "alsa")
        fluidsynth.midi.is_general_midi = True
        fluidsynth.main_volume(0, 70)
        fluidsynth.main_volume(1, 75)
        fluidsynth.main_volume(2, 200)
        fluidsynth.main_volume(9, 75)

        fluidsynth.play_Tracks(
            [self.chords_track, self.bass_track, self.melody_track,
             self.drum_track],
            [0, 1, 2, 9],
            self.bpm
        )

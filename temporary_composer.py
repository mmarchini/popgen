
from mingus.midi import fluidsynth
from mingus.containers import Track, MidiInstrument
from mingus.containers.instrument import MidiPercussionInstrument

from popgen import rhythm, harmony, tempo, melody

drum_track = Track()
drum_track.instrument = MidiPercussionInstrument()
chords_track = Track()
chords_track.instrument = MidiInstrument(name='Electric Guitar (clean)')
bass_track = Track()
bass_track.instrument = MidiInstrument(name='Electric Bass (finger)')
melody_track = Track()
melody_track.instrument = MidiInstrument(name='Overdriven Guitar')

bpm = tempo.define_tempo()
rhythm_ = rhythm.Rhythm(bpm)
drum_bar = rhythm_.generate_bar()

harmony_ = harmony.Harmony()
chords = harmony_.generate_chords()
chord_bars = harmony_.generate_chord_bar(chords, drum_bar)
bass_bars = harmony_.generate_bass_bar(chords, drum_bar)

melody_ = melody.Melody(tempo=bpm)
melody_.harmony = chords
melody_bars = melody_.generate_melody()

for _ in range(2):
    for i, chord_bar in enumerate(chord_bars):
        chords_track.add_bar(chord_bar)
        bass_track.add_bar(bass_bars[i])
        melody_track.add_bar(melody_bars[i])
        drum_track.add_bar(drum_bar)

print fluidsynth.init("arachno.sf2", "alsa")
fluidsynth.midi.is_general_midi = True
fluidsynth.main_volume(0, 70)
fluidsynth.main_volume(1, 75)
fluidsynth.main_volume(2, 100)
fluidsynth.main_volume(9, 75)

fluidsynth.play_Tracks(
    [chords_track, bass_track, melody_track, drum_track],
    [0, 1, 2, 9],
    bpm
)

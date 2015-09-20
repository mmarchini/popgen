
from mingus.midi import fluidsynth
from mingus.containers import Track, MidiInstrument
from mingus.containers.instrument import MidiPercussionInstrument

from popgen import rhythm, harmony, tempo

drum_track = Track()
drum_track.instrument = MidiPercussionInstrument()
chords_track = Track()
chords_track.instrument = MidiInstrument(name='Electric Guitar (jazz)')
bass_track = Track()
bass_track.instrument = MidiInstrument(name='Electric Bass (finger)')

bpm = tempo.define_tempo()
rhythm_ = rhythm.Rhythm(bpm)
bar = rhythm_.generate_bar()
harmony_ = harmony.Harmony()
chords = harmony_.generate_chords()
chord_bars = harmony_.generate_chord_bar(chords, bar)
bass_bars = harmony_.generate_bass_bar(chords, bar)

for _ in range(2):
    for i, chord_bar in enumerate(chord_bars):
        chords_track.add_bar(chord_bar)
        bass_track.add_bar(bass_bars[i])
        drum_track.add_bar(bar)

fluidsynth.init("arachno.sf2", "alsa")
# fluidsynth.set_instrument(0, 30, 0)
# fluidsynth.set_instrument(9, 0, 128)

fluidsynth.play_Tracks([chords_track, bass_track, drum_track], [0, 1, 9], bpm)

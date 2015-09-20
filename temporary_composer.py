
from mingus.midi import fluidsynth
from mingus.core import chords as C
from mingus.containers import Track, MidiInstrument, NoteContainer, Bar
from mingus.containers.instrument import MidiPercussionInstrument

from popgen import rhythm, harmony, tempo

drum_track = Track()
drum_track.instrument = MidiPercussionInstrument()
harmony_track = Track()
harmony_track.instrument = MidiInstrument(name='Pad3 (polysynth)')

bpm = tempo.define_tempo()
rhythm_ = rhythm.Rhythm(bpm)
bar = rhythm_.generate_bar()
guitar = MidiInstrument()

stomps = map(lambda t: [t[0], t[1], None] if t[2] is None or not rhythm_.drum.bass_drum_1() in t[2] else t, bar.bar)
harmony_ = harmony.Harmony()
chords = harmony_.generate_chords()

chord_bars = []
for chord in chords:
    chord = C.from_shorthand(chord)
    chord = ["%s-2" % chord[0], "%s-3" % chord[1], "%s-3" % chord[2]]
    new_bar = Bar()
    new_bar.bar = [[a[0], a[1], a[2] if a[2] is None else NoteContainer(chord)] for a in stomps]
    new_bar.current_beat = 1.0
    chord_bars.append(new_bar)

for chord_bar in chord_bars:
    harmony_track.add_bar(chord_bar)
    drum_track.add_bar(bar)

fluidsynth.init("arachno.sf2", "alsa")
fluidsynth.set_instrument(0, 30, 0)
fluidsynth.set_instrument(9, 0, 128)

fluidsynth.play_Tracks([harmony_track, drum_track], [0, 9], bpm)

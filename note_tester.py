# coding=utf-8

from mingus.midi import fluidsynth
from mingus.containers import Track, MidiInstrument
from mingus.containers import Note, NoteContainer, Bar

from popgen import soundfonts

fluidsynth.midi.is_general_midi = True
fluidsynth.main_volume(0, 200)
fluidsynth.init(soundfonts.DEFAULT_SOUNDFONT, "alsa")


class NoteTestTrack(Track):

    def __len__(self):
        """Enable the len() function for Tracks."""
        return len(self.notes)

    def __getitem__(self, index):
        """Enable the '[]' notation for Tracks."""
        bar = Bar()
        print self.notes[index]
        bar.place_notes(NoteContainer(Note(self.notes[index])), 1)

        return bar


def get_range(a, b):
    a = Note(a)
    b = Note(b)

    next_note = a
    notes = []
    while next_note != b:
        notes.append(next_note)
        next_note = Note().from_int(int(next_note))
        next_note.dynamics["velocity"] = 10
        next_note.augment()
        next_note = Note().from_int(int(next_note))
    notes.append(next_note)

    return notes


def test_instrument(instrument, a, b):
    print instrument
    track = NoteTestTrack()
    track.channel = 0
    track.notes = get_range(a, b)
    track.instrument = MidiInstrument(name=instrument)

    fluidsynth.play_Tracks(
        [track],
        [0],
        120 * 5
    )

# Acoustic #
#  Melody
# test_instrument('Acoustic Guitar (steel)', 'A-2', 'G-4')
#  Chord
# test_instrument('Acoustic Guitar (nylon)', 'A-2', 'C-5')
#  Bass
# test_instrument('Acoustic Bass', 'A-1', 'F-3')

# Jazz #
#  Melody
# test_instrument('Trumpet', 'C-3', 'D-5')
# test_instrument('Alto Sax', 'G-3', 'E-5')
# test_instrument('Tenor Sax', 'A-3', 'G-5')
#  Chord
# test_instrument('Bright Acoustic Piano', 'C-2', 'C-5')
# test_instrument('Electric Guitar (jazz)', 'C-2', 'B-4')
# test_instrument('Electric Grand Piano', 'C-2', 'C-5')
#  Bass
# test_instrument('Baritone Sax', 'C-2', 'C-4')
# test_instrument('Soprano Sax', 'A-1', 'C-4')
# test_instrument('Cello', 'C-2', 'C-4')

# Orchestra #
#  Melody
# test_instrument('Orchestral Harp', 'C-3', 'C-5')
# test_instrument('Violin', 'G-3', 'C-5')
#  Chords
# test_instrument('Viola', 'C-2', 'C-4')
# test_instrument('Cello', 'C-2', 'C-4')
#  Bass
# test_instrument('Contrabass', 'A-1', 'D-3')
# test_instrument('Pizzicato Strings', 'C-2', 'C-4')

# Pano #
#  Melody
# test_instrument('Acoustic Grand Piano', 'C-2', 'C-5')
# test_instrument('Honky-tonk Piano', 'C-2', 'C-5')
# test_instrument('Electric Grand Piano', 'C-2', 'C-5')
#  Chords
# test_instrument('Electric Piano 1', 'C-2', 'C-5')
# test_instrument('Bright Acoustic Piano', 'C-2', 'C-5')
#  Bass
# test_instrument('Electric Piano 2', 'C-2', 'C-5')
# test_instrument('Bright Acoustic Piano', 'C-2', 'C-5')

# Rock #
#  Melody
# test_instrument('Overdriven Guitar', 'C-2', 'G-5')
# test_instrument('Distortion Guitar', 'C-2', 'G-5')
#  Chords
# test_instrument('Overdriven Guitar', 'C-2', 'G-5')
# test_instrument('Electric Guitar (jazz)', 'C-2', 'C-4')
# test_instrument('Electric Guitar (muted)', 'C-2', 'C-4')
#  Bass
# test_instrument('Electric Bass (finger)', 'A-1', 'C-3')
# test_instrument('Electric Bass (pick)', 'A-1', 'C-3')
# test_instrument('Slap Bass 1', 'A-1', 'C-3')
# test_instrument('Slap Bass 2', 'A-1', 'C-3')

# Techno #
#  Melody
# test_instrument('SynthBrass 1', 'C-2', 'C-5')
# test_instrument('SynthBrass 2', 'C-2', 'C-5')
# test_instrument('Lead1 (square)', 'C-2', 'C-5')
# test_instrument('Lead2 (sawtooth)', 'C-2', 'C-5')
# test_instrument('Lead5 (charang)', 'C-2', 'C-5')
# test_instrument('Lead8 (bass + lead)', 'C-2', 'C-5')
# test_instrument('Pad3 (polysynth)', 'C-2', 'C-5')
# test_instrument('FX1 (rain)', 'C-2', 'C-5')
# test_instrument('FX 8 (sci-fi)', 'C-2', 'C-5')
#  Chords
# test_instrument('SynthStrings 1', 'C-2', 'C-4')
# test_instrument('Synth Bass 2', 'C-2', 'C-4')
# test_instrument('Lead4 (chiff)', 'C-2', 'C-4')
# test_instrument('Lead6 (voice)', 'C-2', 'C-4')
# test_instrument('Pad4 (choir)', 'C-2', 'C-4')
# test_instrument('FX 7 (echoes)', 'C-2', 'C-4')
#  Bass
# test_instrument('Synth Bass 1', 'A-1', 'C-3')
# test_instrument('SynthStrings 2', 'A-1', 'C-3')
# test_instrument('Synth Voice', 'A-1', 'C-3')
# test_instrument('Lead3 (calliope)', 'A-1', 'C-3')
# test_instrument('Pad2 (warm)', 'A-1', 'C-3')
# test_instrument('Pad7 (halo)', 'A-1', 'C-3')
# test_instrument('FX 4 (atmosphere)', 'A-1', 'C-3')

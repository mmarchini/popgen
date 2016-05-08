
from mingus.containers import Note
from mingus.containers.instrument import MidiPercussionInstrument

from popgen.instruments import Instrument


class Percussion(Instrument):
    _instrument = "Percussion"
    kick = None
    snare = None
    hi_hat = None
    ride = None


class AcousticPercussion(Percussion):
    _instrument = "Acoustic Percussion"
    kick = MidiPercussionInstrument().acoustic_bass_drum()
    snare = MidiPercussionInstrument().acoustic_snare()
    hi_hat = MidiPercussionInstrument().claves()
    ride = MidiPercussionInstrument().high_timbale()


class OrchestraPercussion(Percussion):
    _instrument = "Orchestra Percussion"
    kick = MidiPercussionInstrument().acoustic_bass_drum()
    snare = MidiPercussionInstrument().acoustic_snare()
    hi_hat = MidiPercussionInstrument().pedal_hi_hat()
    ride = MidiPercussionInstrument().ride_cymbal_1()


class PianoPercussion(Percussion):
    _instrument = "Piano Percussion"
    kick = Note('C-0')  # MidiPercussionInstrument().acoustic_bass_drum()
    snare = Note('C-0')  # MidiPercussionInstrument().acoustic_snare()
    hi_hat = Note('C-0')  # MidiPercussionInstrument().pedal_hi_hat()
    ride = Note('C-0')  # MidiPercussionInstrument().ride_cymbal_1()


class NoPercussion(Percussion):
    _instrument = "No Percussion"
    kick = Note('C-0')  # MidiPercussionInstrument().acoustic_bass_drum()
    snare = Note('C-0')  # MidiPercussionInstrument().acoustic_snare()
    hi_hat = Note('C-0')  # MidiPercussionInstrument().pedal_hi_hat()
    ride = Note('C-0')  # MidiPercussionInstrument().ride_cymbal_1()


class JazzPercussion(Percussion):
    _instrument = "Jazz Percussion"
    kick = MidiPercussionInstrument().high_tom()
    snare = MidiPercussionInstrument().high_timbale()
    hi_hat = MidiPercussionInstrument().open_hi_hat()
    ride = MidiPercussionInstrument().ride_cymbal_1()


class RockPercussion(Percussion):
    _instrument = "Rock Percussion"
    kick = MidiPercussionInstrument().low_floor_tom()
    snare = MidiPercussionInstrument().electric_snare()
    hi_hat = MidiPercussionInstrument().pedal_hi_hat()
    ride = MidiPercussionInstrument().crash_cymbal_2()


class SynthPercussion(Instrument):
    _instrument = "Synth Percussion"
    kick = MidiPercussionInstrument().bass_drum_1()
    snare = MidiPercussionInstrument().hand_clap()
    hi_hat = MidiPercussionInstrument().open_triangle()
    ride = MidiPercussionInstrument().splash_cymbal()


import yaml
from mingus.midi.midi_file_out import write_Composition
from mingus.containers import Track, MidiInstrument, Composition
# from mingus.containers.instrument import MidiPercussionInstrument

from popgen.utils import recursive_update_dict, silent_bar
from popgen.utils import calc_preferred_range, calc_maximum_range
from popgen.rhythm import Rhythm
from popgen.harmony import Harmony, DEFAULT_MARKOV_CHAIN
from popgen.tempo import define_tempo
from popgen.melody import Melody, DYNAMICS, HARMONIC_COMPILANCE
from popgen.phrase_structure import PhraseStructure
from popgen.instruments import Instrument

# from popgen import (rhythm as rhythm_, harmony as harmony_, tempo as tempo_,
#                     melody as melody_, phrase_structure as phrase_structure_)

DEFAULT_INSTRUMENTS = {
    'melody': 'Overdriven Guitar',
    'rhythm': 'Acoustic Percussion',
    'chord': 'Electric Guitar (jazz)',
    'bass': 'Electric Bass (finger)',
}

DEFAULT_PARAMETERS = {
    'harmony': {
        'markov_chain': DEFAULT_MARKOV_CHAIN
    },
    'instruments': DEFAULT_INSTRUMENTS,
    'phrase_structure': PhraseStructure(),
    'key': 'C',
    'melody': {
        'dynamics': DYNAMICS,
        'harmonic_compilance': HARMONIC_COMPILANCE,
        'power': 1,
        'preferred_range': {
            'lower_offset': 0.25,
            'upper_offset': 0.75
        },
        'maximum_range': {
            'lower_offset': 0.1,
            'upper_offset': 0.9
        },
        'inner_drop_off': 0.04,
        'outer_drop_off': 0.15,
    },
    'tempo': {
        'lower': 60, 'upper': 160
    }
}


class Composer(object):

    def __init__(self, bpm=None, rhythm=None, harmony=None, melody=None,
                 phrase_structure=None, instruments={}):
        self.bpm = bpm or define_tempo()
        self.rhythm = rhythm or Rhythm(self.bpm)
        self.harmony = harmony or Harmony()
        self.melody = melody or Melody()
        self.phrase_structure = phrase_structure or \
            PhraseStructure()
        self._instruments = DEFAULT_INSTRUMENTS.copy()
        self._instruments.update(instruments)

    def instrument(self, name, instrument=None):
        if instrument:
            self._instruments[name] = instrument
        return Instrument.get_instrument_by_name(self._instruments[name])

    def compose(self):
        self.drum_track = Track()
        self.drum_track.channel = 9
        self.rhythm.instrument = self.instrument('rhythm')
        self.drum_track.instrument = MidiInstrument()

        chords_instrument = self.instrument('chord')
        self.harmony.instrument = chords_instrument()
        self.chords_track = Track()
        self.chords_track.channel = 1
        self.chords_track.instrument = chords_instrument.get_midi_instrument()

        bass_instrument = self.instrument('bass')
        self.bass_track = Track()
        self.bass_track.channel = 2
        self.bass_track.instrument = bass_instrument.get_midi_instrument()

        melody_instrument = self.instrument('melody')
        self.melody_track = Track()
        self.melody_track.channel = 0
        self.melody_track.instrument = melody_instrument.get_midi_instrument()

        drum_bar = self.rhythm.generate_bar()

        chords = self.harmony.generate_chords()
        chord_bars = self.harmony.generate_chord_bar(chords, drum_bar)
        bass_bars = self.harmony.generate_bass_bar(chords, drum_bar)

        self.melody.harmony = chords
        self.melody.phrase_structure = self.phrase_structure
        melody_bars = self.melody.generate_melody()

        for i, melody_bar in enumerate(melody_bars):
            self.chords_track.add_bar(chord_bars[i % len(chord_bars)])
            self.bass_track.add_bar(bass_bars[i % len(bass_bars)])
            self.melody_track.add_bar(melody_bar)
            self.drum_track.add_bar(drum_bar)
        # Silent bar
        self.chords_track.add_bar(silent_bar())
        self.bass_track.add_bar(silent_bar())
        self.melody_track.add_bar(silent_bar())
        self.drum_track.add_bar(silent_bar())

    def save(self, filename):
        composition = Composition()
        composition.add_track(self.drum_track)
        composition.add_track(self.chords_track)
        composition.add_track(self.bass_track)
        composition.add_track(self.melody_track)
        write_Composition(filename, composition, self.bpm)

    @classmethod
    def from_yaml(cls, filename):
        """
        :param filename: Path to YAML file with parameters.
        """
        params = DEFAULT_PARAMETERS.copy()
        with open(filename) as file_:
            recursive_update_dict(params, yaml.load(file_))

        tempo = params['tempo']
        tempo = define_tempo(tempo['lower'], tempo['upper'])
        tempo = params['tempo'].get('fixed') or tempo

        key = params.get('key')

        rhythm = Rhythm(tempo)

        harmony = Harmony(
            key=key,
            markov_chain=params['harmony']['markov_chain']
        )

        melody = params['melody']
        melody_instrument = Instrument.get_instrument_by_name(params['instruments']['melody'])
        lower = melody['preferred_range']['lower_offset']
        upper = melody['preferred_range']['upper_offset']
        preferred_range = melody_instrument.get_range(key, lower, upper)
        lower = melody['maximum_range']['lower_offset']
        upper = melody['maximum_range']['upper_offset']
        maximum_range = melody_instrument.get_range(key, lower, upper)
        melody = Melody(
            scale=key,
            tempo=tempo,
            power=melody['power'],
            preferred_range=preferred_range,
            maximum_range=maximum_range,
            inner_drop_off=melody['inner_drop_off'],
            outer_drop_off=melody['outer_drop_off']
        )

        phrase_structure = params.get('phrase_structure')

        composer = cls(
            bpm=tempo,
            rhythm=rhythm,
            harmony=harmony,
            melody=melody,
            phrase_structure=phrase_structure,
            instruments=params['instruments']
        )

        return composer

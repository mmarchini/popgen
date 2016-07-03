
from math import copysign

from cdecimal import Decimal
from operator import itemgetter

from scipy.stats import rv_discrete

from mingus.core.value import dots
from mingus.core import progressions, chords
from mingus.containers import NoteContainer, Bar

from popgen.harmony import determine
from popgen.utils import notes_from_range, get_scale

HARMONIC_COMPLIANCE = [
    [0.94, 0.30, 0.95, 0.16, 0.87, 0.26, 0.15],  # I
    [0.20, 0.90, 0.26, 0.86, 0.24, 0.88, 0.02],  # II
    [0.01, 0.18, 0.87, 0.09, 0.89, 0.24, 0.83],  # III
    [0.90, 0.26, 0.18, 0.82, 0.29, 0.99, 0.01],  # IV
    [0.28, 0.92, 0.28, 0.27, 0.95, 0.30, 0.75],  # V
    [0.92, 0.28, 0.85, 0.03, 0.25, 0.91, 0.20],  # VI
]

DYNAMICS = [10, 1, 3, 1, 6, 1, 3, 1, 8, 1, 3, 1, 6, 1, 3, 1]

CONTINUATION = [1.6, 1.35, 1.19, 0.9, 0.75, 0.6, 0.5, 0.45, 0.41, 0.35]


class Melody(object):

    def __init__(self, scale="C", tempo=110, power=1,
                 preferred_range=("A-3", "A-4"), maximum_range=("F-2", "D-4"),
                 inner_drop_off=0.04, outer_drop_off=0.15,
                 harmonic_compliance=HARMONIC_COMPLIANCE, dynamics=DYNAMICS):
        self.preferred_range = preferred_range
        self.maximum_range = maximum_range
        self.inner_drop_off = inner_drop_off
        self.outer_drop_off = outer_drop_off
        self.power = power
        self.scale = scale
        self.tempo = tempo
        self.harmonic_compliance = harmonic_compliance
        self.dynamics = dynamics
        self.phrase_structure = []
        self.harmony = []

    def _init_caches(self):
        u""" Inicializa todas as caches utilizadas durante a composição """
        self.ambitus_cache = {}
        self.current_direction = 0
        self.steps_in_same_direction = 0
        self.note_length_cache = {}
        self._pref_notes = notes_from_range(self.scale, *self.preferred_range)
        self._max_notes = notes_from_range(self.scale, *self.maximum_range)

        self.suggested_notes = []
        for note in self._max_notes:
            for beat in [2, dots(4), 4, dots(8), 8, 16]:
                self.suggested_notes.append((note, beat))
        self.suggested_indexes = map(
            lambda v: self.suggested_notes.index(v),
            self.suggested_notes
        )

        beat_range = lambda a, b, c: [i / 16. for i in range(a, b, c)]
        self.possible_beats = {
            2: [0.15 + (0.0075 * (self.tempo - 70)), beat_range(0, 16, 8)],
            dots(4): [
                0.35 + (0.0085 * (self.tempo - 70)), beat_range(0, 12, 2)],
            4: [0.5 + (0.007 * (self.tempo - 70)), beat_range(0, 16, 4)],
            dots(8): [
                0.151 - (0.002 * (self.tempo - 70)), beat_range(0, 14, 2)],
            8: [abs(0.016 * (self.tempo - 100)), beat_range(0, 16, 2)],
            16: [
                0.65 - (0.014 * (self.tempo - 70)), beat_range(0, 16, 1), None]
        }

        self.poor_compliance_score = {
            2: 0.1,
            dots(4): 0.6,
            4: 1,
            dots(8): 1.1,
            8: 1.18,
            16: 1.25
        }

        self.good_compliance_score = {
            2: 1.25,
            dots(4): 1.15,
            4: 1,
            dots(8): 0.7,
            8: 0.37,
            16: 0.1
        }

    def generate_melody(self, ):
        melody_bars = []
        self._phrases = {}
        self._init_caches()

        for phrase, bars in self.phrase_structure:
            melody_bars.extend(self._generate_phrase_bars(phrase, bars))
        return melody_bars

    def _generate_phrase_bars(self, phrase, bars):
        if phrase in self._phrases:
            return self._phrases[phrase]
        phrase_bars = []
        self.melody = []
        self.last_note = (None, None)
        for bar in range(bars):
            for chord in self.harmony:
                self.current_chord = chord
                self.melody.append([])
                melody_bar = Bar()

                while not melody_bar.is_full():
                    probabilities = []
                    self.current_beat = melody_bar.current_beat
                    for note, beat in self.suggested_notes:
                        probabilities.append(self.calculate_score(note, beat))

                    total = Decimal(sum(probabilities))
                    if not total:
                        note, beat = None, 1 / (1 - self.current_beat)
                    else:
                        normalize = lambda p: p / total
                        probabilities = map(normalize, probabilities)

                        values = [self.suggested_indexes, probabilities]
                        index = rv_discrete(values=values).rvs()

                        note, beat = self.suggested_notes[index]
                    self.melody[-1].append((note, beat))
                    self.last_note = (note, beat)
                    if note is not None:
                        cbeat = int(16 * self.current_beat)
                        velocity = 110 + self.dynamics[cbeat]
                        velocity = velocity if velocity < 128 else 127
                        note.velocity = velocity
                        note = NoteContainer(note)
                    note = note
                    melody_bar.place_notes(note, beat)
                phrase_bars.append(melody_bar)

        self._phrases[phrase] = phrase_bars

        return phrase_bars

    def get_note_chord_compliance(self, note, chord):
        if not getattr(self, "_chord_compliance", None):
            self._chord_compliance = {}
        if not self._chord_compliance.get((note, chord)):
            a = ['I', 'II', 'III', 'IV', 'V', 'VI']

            key_chords = map(determine, progressions.to_chords(a, self.scale))
            key_chords = map(itemgetter(0), key_chords)

            p = self.harmonic_compliance[key_chords.index(chord)]
            comp = p[get_scale(self.scale).ascending()
                     .index(note.name)]

            self._chord_compliance[(note, chord)] = comp

        return self._chord_compliance.get((note, chord))

    def get_interval(self, first_note, second_note):

        possible_notes = self._max_notes

        first_note_pos = possible_notes.index(first_note)
        second_note_pos = possible_notes.index(second_note)

        return second_note_pos - first_note_pos

    def is_pentatonic(self, note):
        pentatonic = get_scale(self.scale)

        if note.name in pentatonic.ascending():
            return True
        return False

    def calculate_ambitus(self, note):
        score = self.ambitus_cache.get(note, None)
        if score:
            return score
        score = Decimal(1)
        pref_notes = self._pref_notes
        maximum_notes = self._max_notes

        if not getattr(self, 'lower_note', None):
            self.lower_note = min(pref_notes)
        if not getattr(self, 'upper_note', None):
            self.upper_note = max(pref_notes)

        if getattr(self, 'lower', None) is None:
            self.lower = filter(lambda r: r < min(pref_notes), maximum_notes)
        if getattr(self, 'upper', None) is None:
            self.upper = filter(lambda r: r > max(pref_notes), maximum_notes)

        if self.lower_note <= note <= self.upper_note:
            if len(pref_notes) % 2 == 1:
                median = len(pref_notes) / 2
            else:
                m = pref_notes[(len(pref_notes) / 2) - 1]
                n = pref_notes[len(pref_notes) / 2]
                if note <= m:
                    median = pref_notes.index(m)
                else:
                    median = pref_notes.index(n)
            offset = abs(median - pref_notes.index(note))
            lowered_by = self.inner_drop_off * offset
        elif note <= self.lower_note:
            lowered_by = (self.lower.index(note) + 1) * self.outer_drop_off
        elif note >= self.upper_note:
            lowered_by = (self.upper.index(note) + 1) * self.outer_drop_off
        else:
            raise ValueError("Invalid note", note)

        score *= Decimal(1 - lowered_by)
        self.ambitus_cache[note] = score
        return score

    def calculate_harmonic_compliance(self, note):
        compliance = self.get_note_chord_compliance(note, self.current_chord)
        return Decimal(compliance)

    def calculate_intervals_n_harmonic_compliance(self, note):
        score = 1
        last_note = self.last_note[0]
        if last_note is None:
            return score
        if not getattr(self, '_intervals_n_harmonic_compliance', None):
            self._intervals_n_harmonic_compliance = {}
        if self._intervals_n_harmonic_compliance.get((last_note, note)):
            return self._intervals_n_harmonic_compliance[(last_note, note)]

        # Harmonic Compilance
        C = self.get_note_chord_compliance
        interval = self.get_interval(last_note, note)
        last_note_compliance = C(last_note, self.current_chord)
        current_note_compliance = C(note, self.current_chord)
        # As it is not clear how they calculate, let's try guessing
        last_note_score = interval * (last_note_compliance - 0.5)
        current_note_score = interval * (current_note_compliance - 0.5)
        score += (last_note_score + current_note_score) / 2.0

        # One pitch step
        chord_notes = chords.from_shorthand(self.current_chord)
        if interval >= 1:
            if not (last_note.name in chord_notes or note.name in chord_notes):
                score -= 0.15
        # Two Pitch steps 1
        is_last_pentatonic = self.is_pentatonic(last_note)
        is_this_pentatonic = self.is_pentatonic(note)
        if interval >= 2:
            if not (last_note.name in chord_notes or note.name in chord_notes):
                if is_last_pentatonic and is_this_pentatonic:
                    score -= 0.1
                else:
                    score -= 0.2
        # Two Pitch steps 2
        if interval >= 2:
            if not (is_last_pentatonic and is_this_pentatonic):
                score -= 0.05

        score = Decimal(score)
        self._intervals_n_harmonic_compliance[(last_note, note)] = score
        return score

    def calculate_note_length(self, beat):
        score = self.note_length_cache.get((self.current_beat, beat), None)
        if score:
            return Decimal(score)

        if self.current_beat + (16. / beat) / 16. > 1.0:
            self.note_length_cache[(self.current_beat, beat)] = -1000
            return -1000

        beat_ = self.possible_beats.get(beat, None)

        if beat_:
            if beat_[1] and self.current_beat not in beat_[1]:
                self.note_length_cache[(self.current_beat, beat)] = -1000
                return -1000
            score = beat_[0]
        else:
            raise ValueError("Unexpected beat", beat)

        if score < 0:
            score = -1000
        self.note_length_cache[(self.current_beat, beat)] = score
        return Decimal(score)

    def calculate_note_length_n_harmonic_compliance(self, note, beat):
        last_note, last_beat = self.last_note
        if not last_note:
            return 0

        score = 1
        C = self.get_note_chord_compliance
        current_note_compliance = C(note, self.current_chord)

        # Poor
        if current_note_compliance < 0.5:
            # Shorter with poor = slightly higher
            # Longer with poor = lower
            self.poor_compliance_score[beat]

        # Good
        else:
            # Shorter with good = lower
            # Longer with good = slightly higher
            self.good_compliance_score[beat]

        return Decimal(score)

    def calculate_good_continuation(self, note):
        last_note = self.last_note[0] or note
        direction = copysign(1, int(note) - int(last_note))
        if self.current_direction == 0:
            self.current_direction = direction
            self.steps_in_same_direction = 0
        elif copysign(1, self.current_direction) == direction:
            self.steps_in_same_direction += 1
        else:
            self.current_direction = 0
            self.steps_in_same_direction = 0

        if self.steps_in_same_direction == 0:
            return Decimal(0.1)
        elif self.steps_in_same_direction > len(CONTINUATION):
            return Decimal(0.1)
        return Decimal(CONTINUATION[self.steps_in_same_direction - 1])

    def calculate_score(self, note, beat):
        score = 0
        # Ambitus
        score += self.calculate_ambitus(note)

        # Harmonic Compilance
        score += self.calculate_harmonic_compliance(note)

        # Intervals & Harmonic Compilance
        score += self.calculate_intervals_n_harmonic_compliance(note)

        # Note Length
        score += self.calculate_note_length(beat)

        # Note Length & Harmonic Compilance
        score += self.calculate_note_length_n_harmonic_compliance(note, beat)

        # Good Continuation
        score += self.calculate_good_continuation(note)

        if score < 0:
            return 0

        return score


from math import copysign

from cdecimal import Decimal
from operator import itemgetter

from scipy.stats import rv_discrete

from mingus.core.value import dots
from mingus.core import scales, progressions, chords
from mingus.containers import Note, NoteContainer, Bar

from popgen.harmony import determine

HARMONIC_COMPILANCE = [
    [0.94, 0.30, 0.95, 0.16, 0.87, 0.26, 0.15],  # I
    [0.20, 0.90, 0.26, 0.86, 0.24, 0.88, 0.02],  # II
    [0.01, 0.18, 0.87, 0.09, 0.89, 0.24, 0.83],  # III
    [0.90, 0.26, 0.18, 0.82, 0.29, 0.99, 0.01],  # IV
    [0.28, 0.92, 0.28, 0.27, 0.95, 0.30, 0.75],  # V
    [0.92, 0.28, 0.85, 0.03, 0.25, 0.91, 0.20],  # VI
]

DYNAMICS = [10, 1, 3, 1, 6, 1, 3, 1, 8, 1, 3, 1, 6, 1, 3, 1]

def notes_from_range(scale, a, b):
    a = Note(a)
    b = Note(b)
    valid_notes = scales.Major(scale).ascending()[:-1]
    if not (a.name in valid_notes and b.name in valid_notes):
        raise ValueError("Invalid notes")

    next_note = a
    notes = []
    while next_note != b:
        if next_note.name in valid_notes:
            notes.append(next_note)
        next_note = Note().from_int(int(next_note))
        next_note.dynamics["velocity"] = 10
        next_note.augment()
        next_note = Note().from_int(int(next_note))
    notes.append(next_note)

    return notes


class Melody(object):

    def __init__(self, scale="C", tempo=110, truncate=0, power=1,
                 preferred_range=("A-3", "A-4"), maximum_range=("F-2", "D-4"),
                 inner_drop_off=0.04, outer_drop_off=0.15):
        self.preferred_range = preferred_range
        self.maximum_range = maximum_range
        self.inner_drop_off = inner_drop_off
        self.outer_drop_off = outer_drop_off
        self.truncate = truncate
        self.power = power
        self.scale = scale
        self.tempo = tempo
        self.phrase_structure = []
        self.harmony = []

    def generate_melody(self, ):
        melody_bars = []
        self._phrases = {}
        self._pref_notes = notes_from_range(self.scale, *self.preferred_range)
        self._max_notes = notes_from_range(self.scale, *self.maximum_range)
        for phrase, bars in self.phrase_structure:
            melody_bars.extend(self._generate_phrase_bars(phrase, bars))

        return melody_bars

    def _generate_phrase_bars(self, phrase, bars):
        if phrase in self._phrases:
            return self._phrases[phrase]
        phrase_bars = []
        self.melody = []
        self.last_note = (None, None)
        possible_notes = self._max_notes
        for bar in range(bars):
            for chord in self.harmony:
                self.current_chord = chord
                self.melody.append([])
                melody_bar = Bar()

                suggested_notes = []
                for note in possible_notes:
                    for beat in [2, dots(4), 4, dots(8), 8, 16]:
                        suggested_notes.append((note, beat))
                suggested_indexes = map(
                    lambda v: suggested_notes.index(v),
                    suggested_notes
                )

                while not melody_bar.is_full():
                    probabilities = []
                    self.current_beat = melody_bar.current_beat
                    for note, beat in suggested_notes:
                        probabilities.append(self.calculate_score(note, beat))

                    total = Decimal(sum(probabilities))
                    if not total:
                        note, beat = None, 1/(1-self.current_beat)
                    else:
                        normalize = lambda p: p/total
                        probabilities = map(normalize, probabilities)

                        values = [suggested_indexes, probabilities]
                        index = rv_discrete(values=values).rvs()

                        note, beat = suggested_notes[index]
                    self.melody[-1].append((note, beat))
                    self.last_note = (note, beat)
                    if note is not None:
                        note.velocity = 117+DYNAMICS[int(16*self.current_beat)]
                        note = NoteContainer(note)
                    note = note
                    melody_bar.place_notes(note, beat)
                phrase_bars.append(melody_bar)

        self._phrases[phrase] = phrase_bars

        return phrase_bars

    def get_note_chord_compilance(self, note, chord):
        if not getattr(self, "_chord_compilance", None):
            self._chord_compilance = {}
        if not self._chord_compilance.get((note, chord)):
            a = ['I', 'II', 'III', 'IV', 'V', 'VI']

            key_chords = map(determine, progressions.to_chords(a, self.scale))
            key_chords = map(itemgetter(0), key_chords)

            p = HARMONIC_COMPILANCE[key_chords.index(chord)]
            comp = p[scales.Major(self.scale).ascending().index(note.name)]

            self._chord_compilance[(note, chord)] = comp

        return self._chord_compilance.get((note, chord))

    def get_interval(self, first_note, second_note):

        possible_notes = self._max_notes

        first_note_pos = possible_notes.index(first_note)
        second_note_pos = possible_notes.index(second_note)

        return second_note_pos - first_note_pos

    def is_pentatonic(self, note):
        pentatonic = scales.PentatonicMajor(self.scale)

        if note.name in pentatonic.ascending():
            return True
        return False

    def calculate_ambitus(self, note):
        ''' A regression towards the mean pitch is achieved by establishing an
        allowed ambitus. The user specifies a preferred range and a maximum
        range as well  as  an  inner  and  an  outer  drop-off. With the inner
        drop off the user can specify how much the score is lowered for each
        step that the pitch deviates from the median pitch within the preferred
        range. With the  outer drop-off the user can specify how much the score
        is lowered as the  pitch moves  towards  the  maximum  range outside
        of  the preferred range. The preferred range represents tessitura, a
        comfortable range for the singer in which most of the pitches should
        reside.'''

        score = Decimal(1)

        pref_notes = self._pref_notes
        maximum_notes = self._max_notes

        if not getattr(self, 'lower', None):
            self.lower = filter(lambda r: r < min(pref_notes), maximum_notes)
            self.lower_note = max(self.lower)
        if not getattr(self, 'upper', None):
            self.upper = filter(lambda r: r > min(pref_notes), maximum_notes)
            self.upper_note = min(self.upper)
        if self.lower_note < note < self.upper_note:
            if len(pref_notes) % 2 == 1:
                median = len(pref_notes)/2
            else:
                m = pref_notes[(len(pref_notes)/2)-1]
                n = pref_notes[len(pref_notes)/2]
                if note <= m:
                    median = pref_notes.index(m)
                else:
                    median = pref_notes.index(n)
            offset = abs(median - pref_notes.index(note))
            lowered_by = self.inner_drop_off * offset
        elif note <= self.lower_note:
            lowered_by = (self.lower.index(note)+1) * self.outer_drop_off
        elif note >= self.upper_note:
            lowered_by = (self.upper.index(note)+1) * self.outer_drop_off
        else:
            raise ValueError("Invalid note", note)

        score *= Decimal(1-lowered_by)

        return score

    def calculate_harmonic_compilance(self, note):
        ''' How  well  a  given  note harmonizes with the chord is an important
        aspect and is in this  paper  referred  to  as harmonic  compliance.
        Each  of the pitches have been given a value between 0-1 for how well
        they harmonize with the different chords, values that can be edited by
        the user as well.
        '''

        compilance = self.get_note_chord_compilance(note, self.current_chord)
        return Decimal(compilance)

    # TODO calculate_intervals_n_harmonic_compilante review
    def calculate_intervals_n_harmonic_compilante(self, note):
        ''' The size of the interval between two notes has a close connection
        to harmony. For larger intervals the dependency on good harmonization
        is much bigger than for small intervals. The harmonization of the notes
        from Table 3 is used in combination with the size of the intervals to
        calculate a harmonic compliance of the intervals. Larger upward
        intervals are favoured over larger downward intervals, and smaller
        downward intervals are favoured over smaller upward intervals. Unusual
        intervals are awarded a lower score even if the two pitches of the
        interval have a perfect harmonic compliance. Some more rules have been
        applied as well.

          * An interval of at least one pitch step where none of the two notes
            belongs to the chord is awarded a lower score.
          * An interval of at least two pitch steps where one of the notes does
            not belong to the chord is awarded a lowered score. If both of the
            notes are pentatonic the lowering is small. If at least one of the
            notes is non-pentatonic the lowering is bigger0.89, 0.24, 0.83.
          * An interval of at least two pitch steps where one of the notes is
            not pentatonic is awarded a slightly lower score, regardless of
            harmonic compliance.
        '''

        score = 1
        last_note = self.last_note[0]
        if last_note is None:
            return score
        if not getattr(self, '_intervals_n_harmonic_compilante', None):
            self._intervals_n_harmonic_compilante = {}
        if self._intervals_n_harmonic_compilante.get((last_note, note)):
            return self._intervals_n_harmonic_compilante[(last_note, note)]

        # Harmonic Compilance

        C = self.get_note_chord_compilance
        interval = self.get_interval(last_note, note)
        last_note_compilance = C(last_note, self.current_chord)
        current_note_compilance = C(note, self.current_chord)
        # As it is not clear how they calculate, let's try guessing
        last_note_score = interval * (last_note_compilance - 0.5)
        current_note_score = interval * (current_note_compilance - 0.5)
        score += (last_note_score + current_note_score)/2.0

        # TODO Unusual intervals??

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
        self._intervals_n_harmonic_compilante[(last_note, note)] = score
        return score

    def calculate_note_length(self, beat):
        ''' As a new note is suggested the previous note will get its length
        determined based on the onset of the new note. One part of the
        evaluation of the new note position is therefore an evaluation of the
        length of the previous note. Here a Markov chain based on statistics
        would have been a good solution but the complexity that comes with
        such a solution would have made it harder to overview. Also a
        connection to tempo was seen as harder to integrate into a Markov
        chain. In Table 4 the probability for different note lengths and their
        dependency on tempo can be observed.
        A normalization is applied so that the highest scoring note receives
        the score 1. Negative values constitute a zero probability.
        Consideration is also taken to positions in the measure for a more
        musical result. As an example, a note falling on an uneven position is
        not allowed to have an even length.
        '''

        beat_range = lambda a, b, c: [i/16. for i in range(a, b, c)]

        possible_beats = {
            2: [0.15 + (0.0075*(self.tempo-70)), beat_range(0, 16, 8)],
            dots(4): [0.35 + (0.0085*(self.tempo-70)), beat_range(0, 12, 2)],
            4: [0.5 + (0.007*(self.tempo-70)), beat_range(0, 16, 4)],
            dots(8): [0.151 - (0.002*(self.tempo-70)), beat_range(0, 14, 2)],
            8: [abs(0.016*(self.tempo-100)), beat_range(0, 16, 2)],
            16: [0.65 - (0.014*(self.tempo-70)), beat_range(0, 16, 1), None]
        }
        beat_ = possible_beats.get(beat, None)

        if self.current_beat + (16./beat)/16. > 1.0:
            return -1000
        elif beat_:
            if beat_[1] and self.current_beat not in beat_[1]:
                return -1000
            score = beat_[0]
        else:
            raise ValueError("Unexpected beat", beat)

        if score < 0:
            score = -1000
        return Decimal(score)

    # TODO calculate_note_length_n_harmonic_compilance
    def calculate_note_length_n_harmonic_compilance(self, note, beat):
        ''' The program tries to create melodies where longer notes in general
        have better harmonization than shorter notes. This means that longer
        notes with poor harmonization are awarded a lower score and that longer
        notes with good harmonization are awarded a higher score. It also means
        that shorter notes with good harmonization are awarded a slightly lower
        score and that shorter notes with poor harmonization are awarded a
        slightly higher score.
        '''
        last_note, last_beat = self.last_note
        if not last_note:
            return 0

        score = 1
        C = self.get_note_chord_compilance
        current_note_compilance = C(note, self.current_chord)

        # Poor
        if current_note_compilance < 0.5:
            # Shorter with poor = slightly higher
            # Longer with poor = lower
            score = {
                2: 0.1,
                dots(4): 0.6,
                4: 1,
                dots(8): 1.1,
                8: 1.18,
                16: 1.25
            }[beat]

        # Good
        else:
            # Shorter with good = lower
            # Longer with good = slightly higher
            score = {
                2: 1.25,
                dots(4): 1.15,
                4: 1,
                dots(8): 0.7,
                8: 0.37,
                16: 0.1
            }[beat]

        return Decimal(score)

    # TODO calculate_note_length_n_interval_size
    def calculate_note_length_n_interval_size(self, note):
        ''' As can be seen in Figure 2, Section C there is a relationship
        between note length and interval size. This is implemented in the
        program so that the probability for a small interval size is higher
        between shorter notes and the probability for a large interval size is
        higher between longer notes.
        '''

        return 1

    # TODO calculate_prase_arch
    def calculate_prase_arch(self, note):
        ''' Compliance with Huron's (2006) findings of convex phrase arches can
        be ensured if the user choses to.
        '''

        return 1

    # TODO calculate_tonal_resolution
    def calculate_tonal_resolution(self, note):
        ''' At the end of the refrain the melody will resolve at a tonic. This
        may happen in the verse as well if there is a position where a dominant
        V chord is followed by the tonic I. In Figure 7 we see statistical
        findings for tonal resolution at the end of songs in the Essen Folksong
        Collection (Elowsson, 2012). The gradually narrowing distance to the
        tonic, as symbolized by arrows is achieved in the program by a
        narrowing window.
        '''

        return 1

    # TODO calculate_repetition
    def calculate_repetition(self, note):
        ''' Patterns in the melody repeat themselves over and over again both
        at a rhythmical level and concerning pitch intervals. As we have seen
        in Figure 1 much repetition comes at a phrase level and the program
        uses earlier phrases as "mirrors" for the following phrases. If the
        phrase is to repeat an earlier phrase, consideration is taken to how
        the intervals between the notes in the phrase correspond to the
        intervals of the notes in the mirror phrase. Consideration is also
        taken separately to the difference in contour. The score is given by:

            c . I

        The differences in contour determine 'c'. The default setting is
          * Same contour = 1.2
          * Not same, not opposite contour = 0.9
          * Opposite contour = 0.7

        The values can be tuned by the user. The value of I is determined by
        the interval I2 of the mirror phrase and the interval I1 of the current
        phrase by the equation:

            k^|I2-I1|

        The constant k can be tuned by the user.
        '''

        return 1

    def calculate_good_continuation(self, note):
        ''' To give the melody a sense of direction a higher score is awarded
        to melodies that continue in a newly established direction. A
        statistical foundation can be seen in Figure 8 (Elowsson, 2012).
        '''

        same_direction = True
        count = 0
        direction = 0
        last_note = note
        for bar in reversed(self.melody):
            for note, beat in reversed(bar):
                if note is None:
                    continue
                current_direction = copysign(1, int(last_note) - int(note))
                if note == last_note:
                    last_note = note
                    count += 1
                elif direction == 0:
                    direction = current_direction
                    last_note = note
                    count += 1
                elif direction == current_direction:
                    last_note = note
                    count += 1
                else:
                    same_direction = False
                    break
            if not same_direction:
                break

        p = [1.6, 1.35, 1.19, 0.9, 0.75, 0.6, 0.5, 0.45, 0.41, 0.35]
        if count > len(p):
            return 0
        elif direction == 0:
            return Decimal(0.1)

        return Decimal(p[count-1])

    def calculate_score(self, note, beat):
        score = 0
        # 1. Ambitus
        score += self.calculate_ambitus(note)

        # 2. Harmonic Compilance
        score += self.calculate_harmonic_compilance(note)

        # 3. Intervals & Harmonic Compilance
        score += self.calculate_intervals_n_harmonic_compilante(note)

        # 4. Note Length
        score += self.calculate_note_length(beat)

        # 5. Note Length & Harmonic Compilance
        score += self.calculate_note_length_n_harmonic_compilance(note, beat)

        # 6. Note Length & Interval Size
        score += self.calculate_note_length_n_interval_size(note)

        # 7. Prase Arch
        score += self.calculate_prase_arch(note)

        # 8. Tonal Resolution
        score += self.calculate_tonal_resolution(note)

        # 9. Repetition
        score += self.calculate_repetition(note)

        # 10. Good Continuation
        score += self.calculate_good_continuation(note)

        if score < 0:
            return 0

        return score


from decimal import Decimal

from scipy.stats import rv_discrete

from mingus.core import scales
from mingus.containers import Note, NoteContainer, Bar

HARMONIC_COMPILANCE = [
    [0.94, 0.30, 0.95, 0.16, 0.87, 0.26, 0.15],  # I
    [0.20, 0.90, 0.26, 0.86, 0.24, 0.88, 0.02],  # II
    [0.01, 0.18, 0.87, 0.09, 0.89, 0.24, 0.83],  # III
    [0.90, 0.26, 0.18, 0.82, 0.29, 0.99, 0.01],  # IV
    [0.28, 0.92, 0.28, 0.27, 0.95, 0.30, 0.75],  # V
    [0.92, 0.28, 0.85, 0.03, 0.25, 0.91, 0.20],  # VI
]


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
        next_note.augment()
        next_note = Note().from_int(int(next_note))
    notes.append(next_note)

    return notes


class Melody(object):

    def __init__(self, scale="C", truncate=0, power=1,
                 preferred_range=("A-3", "A-4"), maximum_range=("F-2", "D-4"),
                 inner_drop_off=0.04, outer_drop_off=0.15):
        self.preferred_range = preferred_range
        self.maximum_range = maximum_range
        self.inner_drop_off = inner_drop_off
        self.outer_drop_off = outer_drop_off
        self.truncate = truncate
        self.power = power
        self.scale = scale
        self.harmony = []

    def generate_melody(self, ):
        melody_bars = []
        for chord in self.harmony:
            melody_bar = Bar()

            possible_notes = notes_from_range(self.scale, *self.maximum_range)
            suggested_notes = []
            for note in possible_notes:
                for beat in [1, 2, 4, 8, 16]:
                    suggested_notes.append((note, beat))
            suggested_indexes = map(
                lambda v: suggested_notes.index(v),
                suggested_notes
            )

            while not melody_bar.is_full():
                probabilities = []
                for note, beat in suggested_notes:
                    probabilities.append(self.calculate_score(note, beat))

                total = Decimal(sum(probabilities))
                normalize = lambda p: p/total
                probabilities = map(normalize, probabilities)

                values = [suggested_indexes, probabilities]
                print len(suggested_notes), len(probabilities)
                index = rv_discrete(values=values).rvs()

                note, beat = suggested_notes[index]
                melody_bar.place_notes(NoteContainer(note), beat)
            melody_bars.append(melody_bar)

        return melody_bars

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

        return 1

    def calculate_harmonic_compilance(self, note):
        ''' How  well  a  given  note harmonizes with the chord is an important
        aspect and is in this  paper  referred  to  as harmonic  compliance.
        Each  of the pitches have been given a value between 0-1 for how well
        they harmonize with the different chords, values that can be edited by
        the user as well.
        '''

        return 1

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
            notes is non-pentatonic the lowering is bigger.
          * An interval of at least two pitch steps where one of the notes is
            not pentatonic is awarded a slightly lower score, regardless of
            harmonic compliance.
        '''

        return 1

    def calculate_note_length(self, note):
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

        return 1

    def calculate_note_length_n_harmonic_compilance(self, note):
        ''' The program tries to create melodies where longer notes in general
        have better harmonization than shorter notes. This means that longer
        notes with poor harmonization are awarded a lower score and that longer
        notes with good harmonization are awarded a higher score. It also means
        that shorter notes with good harmonization are awarded a slightly lower
        score and that shorter notes with poor harmonization are awarded a
        slightly higher score.
        '''

        return 1

    def calculate_note_length_n_interval_size(self, note):
        ''' As can be seen in Figure 2, Section C there is a relationship
        between note length and interval size. This is implemented in the
        program so that the probability for a small interval size is higher
        between shorter notes and the probability for a large interval size is
        higher between longer notes.
        '''

        return 1

    def calculate_prase_arch(self, note):
        ''' Compliance with Huron's (2006) findings of convex phrase arches can
        be ensured if the user choses to.
        '''

        return 1

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

        return 1

    def calculate_score(self, note, beat):
        score = 0
        # 1. Ambitus
        score += self.calculate_ambitus(note)

        # 2. Harmonic Compilance
        score += self.calculate_harmonic_compilance(note)

        # 3. Intervals & Harmonic Compilance
        score += self.calculate_intervals_n_harmonic_compilante(note)

        # 4. Note Length
        score += self.calculate_note_length(note)

        # 5. Note Length & Harmonic Compilance
        score += self.calculate_note_length_n_harmonic_compilance(note)

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

        return score

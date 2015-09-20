
from mingus.core import scales
from mingus.containers import Note

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
                 preferred_range=("A-3", "A-4"), maximum_range=("F2-D4"),
                 inner_drop_off=0.04, outer_drop_off=0.15):
        self.preferred_range = preferred_range
        self.maximum_range = maximum_range
        self.inner_drop_off = inner_drop_off
        self.outer_drop_off = outer_drop_off
        self.maximum_range = maximum_range
        self.truncate = truncate
        self.power = power

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

        self.note

    def calculate_harmonic_compilance(self, note):
        pass

    def calculate_score(self, note):
        score = 0
        # 1. Ambitus

        # 2. Harmonic Compilance

        # 3. Intervals & Harmonic Compilance

        # 4. Note Length

        # 5. Note Length & Harmonic Compilance

        # 6. Note Length & Interval Size

        # 7. Prase Arch

        # 8. Tonal Resolution

        # 9. Repetition

        # 10. Good Continuation

        return score

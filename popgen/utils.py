import collections

from mingus.core import scales
from mingus.containers import Note


def get_scale(scale):
    scale_mode = scales.Major if scale.isupper() else scales.NaturalMinor
    return scale_mode(scale.upper())


def notes_from_range(scale, a, b):
    a = Note(a)
    b = Note(b)
    valid_notes = get_scale(scale).ascending()[:-1]

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


def calc_preferred_range(scale, center, lower, upper):
    valid_notes = get_scale(scale).ascending()[:-1]
    lowest_note = "%s-0" % valid_notes[0]
    highest_note = "%s-10" % valid_notes[-1]
    valid_notes = notes_from_range(scale, lowest_note, highest_note)

    center = Note(scale.upper(), center)
    center_idx = valid_notes.index(center)

    upper_boundary = valid_notes[center_idx + upper]
    lower_boundary = valid_notes[center_idx - lower]

    return (lower_boundary, upper_boundary)


def calc_maximum_range(scale, preferred_range, lower, upper):
    valid_notes = get_scale(scale).ascending()[:-1]
    lowest_note = "%s-0" % valid_notes[0]
    highest_note = "%s-10" % valid_notes[-1]
    valid_notes = notes_from_range(scale, lowest_note, highest_note)

    preferred_upper = valid_notes.index(preferred_range[1])
    upper_boundary = valid_notes[preferred_upper + upper]

    preferred_lower = valid_notes.index(preferred_range[0])
    lower_boundary = valid_notes[preferred_lower - lower]

    return (lower_boundary, upper_boundary)


def recursive_update_dict(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = recursive_update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

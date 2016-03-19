
""" Ideas:
* Structure attributes that could affect melody and rhythm generation, as
  well as harmony chords
*
"""


class PhraseStructure(object):

    def __init__(self):
        pass

    def __iter__(self):
        return iter([
            (1, 1),
            (2, 2),
            (3, 3),
            (2, 2),
            (4, 1),
            (3, 3),
            (5, 1),
        ])

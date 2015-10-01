

class PhraseStructure(object):

    def __init__(self):
        pass

    def __iter__(self):
        return iter([
            (1, 2),
            (2, 4),
            (3, 4),
            (2, 4),
            (4, 1),
            (3, 4),
            (5, 1),
        ])

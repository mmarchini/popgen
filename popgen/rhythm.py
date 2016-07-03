#coding=utf8

import random
from operator import itemgetter

from mingus.containers import Bar, NoteContainer

from popgen.utils import WeightedChoice
from popgen.instruments import AcousticPercussion

# TEMPO_DISTRIBUTION = [
#     (60,  0.01),
#     (70,  0.03),
#     (80,  0.07),
#     (90,  0.20),
#     (100, 0.15),
#     (110, 0.24),
#     (120, 0.32),
#     (130, 0.14),
#     (140, 0.05),
#     (150, 0.01),
#     (160, 0.01),
# ]

POSITION_WEIGHT = [
    (1, 10),
    (2, 1),
    (3, 3),
    (4, 1),
    (5, 6),
    (6, 1),
    (7, 3),
    (8, 1),
    (9, 8),
    (10, 1),
    (11, 3),
    (12, 1),
    (13, 6),
    (14, 1),
    (15, 3),
    (16, 1),
]


class Rhythm(object):

    def __init__(self, tempo, instrument=AcousticPercussion):
        self.tempo = tempo
        self.instrument = instrument

    def number_of_kicks(self):
        kicks_mean = 1. + ((abs((self.tempo - 160.) / 40.)))
        kicks = int(round(random.gauss(kicks_mean, .45)))

        return kicks

    def calculate_beats(self, quantity, possible_durations, beats=[]):
        duration_chooser = WeightedChoice(*possible_durations)

        # Determina a posição e duração das notas
        for i in range(quantity):
            beat_duration = duration_chooser.choose()
            beat_step = 16 / beat_duration

            possible_positions = []
            # Itera sobre as posições possíveis, baseado na duração da nota
            for i in range(0, 16, beat_step):
                # Verifica se a nota atual não se sobrepôe as notas
                # já escolhidas
                if not any([i <= beat[0] < i + beat_step for beat in beats]):
                    possible_positions.append(i)

            # Escolhe uma das notas possíveis
            chosen_position = random.choice(possible_positions)
            beats.append((chosen_position, beat_duration))

            # Ordena as notas de acordo com as suas posições
            beats = sorted(beats, key=itemgetter(0))
        return beats

    def generate_kicks(self):
        u""" Gera os `kicks` que aparecerção na composição """
        possible_durations = [(4, 0.60), (8, 0.40)]

        return (self.instrument.kick, self.calculate_beats(
            quantity=self.number_of_kicks()-1,
            possible_durations=possible_durations,
            beats=[
                (0, WeightedChoice(possible_durations).choose())
            ]
        ))

    def generate_snares(self):
        u""" Gera os `snares` que aparecerção na composição """
        number_of_snares = WeightedChoice(
            (1, 0.2), (2, 0.4), (3, 0.3), (4, 0.09), (0, 0.01)
        ).choose()

        return (self.instrument.snare, self.calculate_beats(
            quantity=number_of_snares,
            possible_durations=[(4, 0.5), (8, 0.3), (16, 0.2)],
        ))

    def generate_hihats(self):
        u""" Gera os `hihats` que aparecerção na composição """
        number_of_hihats = WeightedChoice(
            (1, 0.2), (2, 0.4), (3, 0.3), (4, 0.09), (0, 0.01)
        ).choose()

        return (self.instrument.hi_hat, self.calculate_beats(
            quantity=number_of_hihats,
            possible_durations=[(4, 0.5), (8, 0.3), (16, 0.2)],
        ))

    def generate_rides(self):
        u""" Gera os `rides` que aparecerção na composição """
        number_of_rides = WeightedChoice(
            (1, 0.2), (2, 0.4), (3, 0.3), (4, 0.09), (0, 0.01)
        ).choose()

        return (self.instrument.ride, self.calculate_beats(
            quantity=number_of_rides,
            possible_durations=[(4, 0.60), (8, 0.40)],
        ))

    def generate_bar(self):
        u""" Gera o ritmo da música, utilizando todas as notas de percussção
        possívels. Retorna esse ritmo representado por um objeto do tipo
        `mingus.container.Bar` """
        beats = [
            self.generate_kicks(),
            self.generate_rides(),
            self.generate_snares(),
            self.generate_hihats(),
        ]

        p = set()
        for instr, beat in beats:
            p |= set(map(itemgetter(0), beat))

        bar = Bar()
        for i in range(16):
            bar.place_notes(None, 16)

        for i in sorted(p):
            container = NoteContainer()
            for instr, beat in beats:
                beat = (filter(lambda b: b[0] == i, beat) or [None]).pop()
                if beat:
                    container.add_note(instr)

            bar.bar.pop(bar.bar.index([i / 16., 16, None]))
            bar.bar.append([i / 16., 16, container])
        bar.bar = sorted(bar.bar, key=itemgetter(0))
        bar.current_beat = 1.0

        return bar


from popgen.instruments.base import Instrument


class BaseSax(Instrument):
    pass


class Trumpet(BaseSax):
    # test_instrument('Trumpet', 'C-3', 'D-5')
    _instrument = 'Trumpet'
    lower = 'C-3'
    upper = 'D-5'


class AltoSax(BaseSax):
    # test_instrument('Alto Sax', 'G-3', 'E-5')
    _instrument = 'Alto Sax'
    lower = 'G-3'
    upper = 'E-5'


class TenorSax(BaseSax):
    # test_instrument('Tenor Sax', 'A-3', 'G-5')
    _instrument = 'Tenor Sax'
    lower = 'A-3'
    upper = 'G-5'


class BaritoneSax(BaseSax):
    # test_instrument('Baritone Sax', 'C-2', 'C-4')
    _instrument = 'Baritone Sax'
    lower = 'C-2'
    upper = 'C-4'


class SopranoSax(BaseSax):
    # test_instrument('Soprano Sax', 'A-1', 'C-4')
    _instrument = 'Soprano Sax'
    lower = 'A-1'
    upper = 'C-4'


from popgen.instruments.base import Instrument


class BaseOrchestra(Instrument):
    pass


class OrchestralHarp(BaseOrchestra):
    # test_instrument('Orchestral Harp', 'C-3', 'C-5')
    _instrument = 'Orchestral Harp'
    lower = 'C-3'
    upper = 'C-5'


class Violin(BaseOrchestra):
    # test_instrument('Violin', 'G-3', 'C-5')
    _instrument = 'Violin'
    lower = 'G-3'
    upper = 'C-5'


class Viola(BaseOrchestra):
    # test_instrument('Viola', 'C-2', 'C-4')
    _instrument = 'Viola'
    lower = 'C-2'
    upper = 'C-4'


class Cello(BaseOrchestra):
    # test_instrument('Cello', 'C-2', 'C-4')
    _instrument = 'Cello'
    lower = 'C-2'
    upper = 'C-4'


class Contrabass(BaseOrchestra):
    # test_instrument('Contrabass', 'A-1', 'D-3')
    _instrument = 'Contrabass'
    lower = 'A-1'
    upper = 'D-3'


class PizzicatoStrings(BaseOrchestra):
    # test_instrument('Pizzicato Strings', 'C-2', 'C-4')
    _instrument = 'Pizzicato Strings'
    lower = 'C-2'
    upper = 'C-4'

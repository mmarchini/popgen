
from popgen.instruments.base import Instrument


class TangoAccordion(Instrument):
    # test_instrument('Tango Accordion', 'G-2', 'G-4')
    _instrument = 'Tango Accordion'
    lower = 'G-2'
    upper = 'G-4'


class Accordion(Instrument):
    # test_instrument('Accordion', 'C-4', 'C-6')
    _instrument = 'Accordion'
    lower = 'C-4'
    upper = 'C-6'


class Harmonica(Instrument):
    # test_instrument('Harmonica', 'C-4', 'C-6')
    _instrument = 'Harmonica'
    lower = 'C-4'
    upper = 'C-6'

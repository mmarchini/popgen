

from popgen.instruments.base import Instrument


class BasePiano(Instrument):
    pass


class AcousticGrandPiano(BasePiano):
    # test_instrument('Acoustic Grand Piano', 'C-2', 'C-5')
    _instrument = 'Acoustic Grand Piano'
    lower = 'C-2'
    upper = 'C-5'


class HonkyTonkPiano(BasePiano):
    # test_instrument('Honky-tonk Piano', 'C-2', 'C-5')
    _instrument = 'Honky-tonk Piano'
    lower = 'C-2'
    upper = 'C-5'


class ElectricGrandPiano(BasePiano):
    # test_instrument('Electric Grand Piano', 'C-2', 'C-5')
    _instrument = 'Electric Grand Piano'
    lower = 'C-2'
    upper = 'C-5'


class ElectricPiano1(BasePiano):
    # test_instrument('Electric Piano 1', 'C-2', 'C-5')
    _instrument = 'Electric Piano 1'
    lower = 'C-2'
    upper = 'C-5'


class BrightAcousticPiano(BasePiano):
    # test_instrument('Bright Acoustic Piano', 'C-2', 'C-5')
    _instrument = 'Bright Acoustic Piano'
    lower = 'C-2'
    upper = 'C-5'


class ElectricPiano2(BasePiano):
    # test_instrument('Electric Piano 2', 'C-2', 'C-5')
    _instrument = 'Electric Piano 2'
    lower = 'C-2'
    upper = 'C-5'

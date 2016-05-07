
from popgen.instruments.base import Instrument


class BaseGuitar(Instrument):
    pass


class AcousticSteelGuitar(BaseGuitar):
    # test_instrument('Acoustic Guitar (steel)', 'A-2', 'G-4')
    _instrument = 'Acoustic Guitar (steel)'
    lower = 'A-2'
    upper = 'G-4'


class AcousticNylonGuitar(BaseGuitar):
    # test_instrument('Acoustic Guitar (nylon)', 'A-2', 'C-5')
    _instrument = 'Acoustic Guitar (nylon)'
    lower = 'A-2'
    upper = 'C-5'


class AcousticBass(BaseGuitar):
    # test_instrument('Acoustic Bass', 'A-1', 'F-3')
    _instrument = 'Acoustic Bass'
    lower = 'A-1'
    upper = 'F-3'


class ElectricJazzGuitar(BaseGuitar):
    # test_instrument('Electric Guitar (jazz)', 'C-2', 'B-4')
    _instrument = 'Electric Guitar (jazz)'
    lower = 'C-2'
    upper = 'B-4'


class OverdrivenGuitar(BaseGuitar):
    # test_instrument('Overdriven Guitar', 'C-2', 'G-5')
    _instrument = 'Overdriven Guitar'
    lower = 'C-2'
    upper = 'G-5'


class DistortionGuitar(BaseGuitar):
    # test_instrument('Distortion Guitar', 'C-2', 'G-5')
    _instrument = 'Distortion Guitar'
    lower = 'C-2'
    upper = 'G-5'


class ElectricMutedGuitar(BaseGuitar):
    # test_instrument('Electric Guitar (muted)', 'C-2', 'C-4')
    _instrument = 'Electric Guitar (muted)'
    lower = 'C-2'
    upper = 'C-4'


class ElectricFingerBass(BaseGuitar):
    # test_instrument('Electric Bass (finger)', 'A-1', 'C-3')
    _instrument = 'Electric Bass (finger)'
    lower = 'A-1'
    upper = 'C-3'


class ElectricPickBass(BaseGuitar):
    # test_instrument('Electric Bass (pick)', 'A-1', 'C-3')
    _instrument = 'Electric Bass (pick)'
    lower = 'A-1'
    upper = 'C-3'


class SlapBass1(BaseGuitar):
    # test_instrument('Slap Bass 1', 'A-1', 'C-3')
    _instrument = 'Slap Bass 1'
    lower = 'A-1'
    upper = 'C-3'


class SlapBass2(BaseGuitar):
    # test_instrument('Slap Bass 2', 'A-1', 'C-3')
    _instrument = 'Slap Bass 2'
    lower = 'A-1'
    upper = 'C-3'

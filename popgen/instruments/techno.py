

from popgen.instruments.base import Instrument


class BaseSynth(Instrument):
    pass


class SynthBrass1(BaseSynth):
    # test_instrument('SynthBrass 1', 'C-2', 'C-5')
    _instrument = 'SynthBrass 1'
    lower = 'C-2'
    upper = 'C-5'


class SynthBrass2(BaseSynth):
    # test_instrument('SynthBrass 2', 'C-2', 'C-5')
    _instrument = 'SynthBrass 2'
    lower = 'C-2'
    upper = 'C-5'


class LeadSquare(BaseSynth):
    # test_instrument('Lead1 (square)', 'C-2', 'C-5')
    _instrument = 'Lead1 (square)'
    lower = 'C-2'
    upper = 'C-5'


class LeadSawtooth(BaseSynth):
    # test_instrument('Lead2 (sawtooth)', 'C-2', 'C-5')
    _instrument = 'Lead2 (sawtooth)'
    lower = 'C-2'
    upper = 'C-5'


class LeadCharang(BaseSynth):
    # test_instrument('Lead5 (charang)', 'C-2', 'C-5')
    _instrument = 'Lead5 (charang)'
    lower = 'C-2'
    upper = 'C-5'


class LeadBassLead(BaseSynth):
    # test_instrument('Lead8 (bass + lead)', 'C-2', 'C-5')
    _instrument = 'Lead8 (bass + lead)'
    lower = 'C-2'
    upper = 'C-5'


class PadPolysynth(BaseSynth):
    # test_instrument('Pad3 (polysynth)', 'C-2', 'C-5')
    _instrument = 'Pad3 (polysynth)'
    lower = 'C-2'
    upper = 'C-5'


class FXRain(BaseSynth):
    # test_instrument('FX1 (rain)', 'C-2', 'C-5')
    _instrument = 'FX1 (rain)'
    lower = 'C-2'
    upper = 'C-5'


class FXSciFi(BaseSynth):
    # test_instrument('FX 8 (sci-fi)', 'C-2', 'C-5')
    _instrument = 'FX 8 (sci-fi)'
    lower = 'C-2'
    upper = 'C-5'


class SynthStrings1(BaseSynth):
    # test_instrument('SynthStrings 1', 'C-2', 'C-4')
    _instrument = 'SynthStrings 1'
    lower = 'C-2'
    upper = 'C-4'


class SynthBass2(BaseSynth):
    # test_instrument('Synth Bass 2', 'C-2', 'C-4')
    _instrument = 'Synth Bass 2'
    lower = 'C-2'
    upper = 'C-4'


class LeadChiff(BaseSynth):
    # test_instrument('Lead4 (chiff)', 'C-2', 'C-4')
    _instrument = 'Lead4 (chiff)'
    lower = 'C-2'
    upper = 'C-4'


class LeadVoice(BaseSynth):
    # test_instrument('Lead6 (voice)', 'C-2', 'C-4')
    _instrument = 'Lead6 (voice)'
    lower = 'C-2'
    upper = 'C-4'


class PadChoir(BaseSynth):
    # test_instrument('Pad4 (choir)', 'C-2', 'C-4')
    _instrument = 'Pad4 (choir)'
    lower = 'C-2'
    upper = 'C-4'


class FXEchoes(BaseSynth):
    # test_instrument('FX 7 (echoes)', 'C-2', 'C-4')
    _instrument = 'FX 7 (echoes)'
    lower = 'C-2'
    upper = 'C-4'


class SynthBass1(BaseSynth):
    # test_instrument('Synth Bass 1', 'A-1', 'C-3')
    _instrument = 'Synth Bass 1'
    lower = 'A-1'
    upper = 'C-3'


class SynthStrings2(BaseSynth):
    # test_instrument('SynthStrings 2', 'A-1', 'C-3')
    _instrument = 'SynthStrings 2'
    lower = 'A-1'
    upper = 'C-3'


class SynthVoice(BaseSynth):
    # test_instrument('Synth Voice', 'A-1', 'C-3')
    _instrument = 'Synth Voice'
    lower = 'A-1'
    upper = 'C-3'


class LeadCalliope(BaseSynth):
    # test_instrument('Lead3 (calliope)', 'A-1', 'C-3')
    _instrument = 'Lead3 (calliope)'
    lower = 'A-1'
    upper = 'C-3'


class PadWarm(BaseSynth):
    # test_instrument('Pad2 (warm)', 'A-1', 'C-3')
    _instrument = 'Pad2 (warm)'
    lower = 'A-1'
    upper = 'C-3'


class PadHalo(BaseSynth):
    # test_instrument('Pad7 (halo)', 'A-1', 'C-3')
    _instrument = 'Pad7 (halo)'
    lower = 'A-1'
    upper = 'C-3'


class FXAtmosphere(BaseSynth):
    # test_instrument('FX 4 (atmosphere)', 'A-1', 'C-3')
    _instrument = 'FX 4 (atmosphere)'
    lower = 'A-1'
    upper = 'C-3'

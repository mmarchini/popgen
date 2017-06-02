#!/usr/bin/env python

import subprocess

from popgen import playa
from popgen import composition, soundfonts

composer = composition.Composer.from_yaml('tests.yaml')

print("Composing...")
composer.compose()

print("Saving file...")
midi_file = '/tmp/teste.midi'
wave_file = '/tmp/teste.wav'
composer.save(midi_file)
print("Opening song...")
playa.play(midi_file, soundfonts.DEFAULT_SOUNDFONT, wave_file)
subprocess.call(['aplay', wave_file])

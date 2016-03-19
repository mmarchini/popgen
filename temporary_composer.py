
import subprocess

from ministrel import utils

from popgen import composition

composer = composition.Composer.from_yaml('tests.yaml')

print("Composing...")
composer.compose()

print("Saving file...")
midi_file = '/tmp/teste.midi'
wave_file = '/tmp/teste.wav'
composer.save(midi_file)
print("Opening song...")
utils.play(midi_file, 'arachno.sf2', wave_file)
subprocess.call(['aplay', wave_file])

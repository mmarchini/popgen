import hashlib
import os
import fcntl
import subprocess as sp
from datetime import datetime
from ctypes import c_int16, c_void_p, c_int, c_char_p, POINTER, byref, cast

import soundfile
from numpy import array, int16
from mingus.midi.pyfluidsynth import cfunc
from mingus.midi.pyfluidsynth import new_fluid_settings, fluid_settings_setstr
from mingus.midi.pyfluidsynth import fluid_synth_sfload, fluid_settings_setint
from mingus.midi.pyfluidsynth import delete_fluid_synth, delete_fluid_settings
from mingus.midi.pyfluidsynth import new_fluid_synth


new_fluid_player = cfunc('new_fluid_player', c_void_p, ('synth', c_void_p, 1))

fluid_player_add = cfunc('fluid_player_add', c_int, ('player', c_void_p, 1),
                         ('midifile', c_char_p, 1))

fluid_player_play = cfunc('fluid_player_play', c_int, ('player', c_void_p, 1))

fluid_player_join = cfunc('fluid_player_join', c_int, ('player', c_void_p, 1))

delete_fluid_player = cfunc('delete_fluid_player', c_int,
                            ('player', c_void_p, 1))

new_fluid_file_renderer = cfunc('new_fluid_file_renderer', c_void_p,
                                ('synth', c_void_p, 1))

delete_fluid_file_renderer = cfunc('delete_fluid_file_renderer', None,
                                   ('dev', c_void_p, 1))

delete_fluid_file_renderer = cfunc('delete_fluid_file_renderer', None,
                                   ('dev', c_void_p, 1))

fluid_player_get_status = cfunc('fluid_player_get_status', c_int,
                                ('player', c_void_p, 1))

fluid_file_renderer_process_block = cfunc('fluid_file_renderer_process_block',
                                          c_int, ('dev', c_void_p, 1))

fluid_synth_write_float = cfunc('fluid_synth_write_float', c_int,
                                ('synth', c_void_p, 1),
                                ('len', c_int, 1),
                                ('lout', c_void_p, 1),
                                ('loff', c_int, 1),
                                ('lincr', c_int, 1),
                                ('rout', c_void_p, 1),
                                ('roff', c_int, 1),
                                ('rincr', c_int, 1))

fluid_synth_write_s16 = cfunc('fluid_synth_write_s16', c_int,
                              ('synth', c_void_p, 1),
                              ('len', c_int, 1),
                              ('lout', c_void_p, 1),
                              ('loff', c_int, 1),
                              ('lincr', c_int, 1),
                              ('rout', c_void_p, 1),
                              ('roff', c_int, 1),
                              ('rincr', c_int, 1))


fluid_settings_getint = cfunc('fluid_settings_getint', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', POINTER(c_int), 1))


# class FluidFileRenderer(Structure):
#     _fields_ = [
#         ('a', c_uint8),
#         ('b', c_uint8),
#         ('c', c_uint32),
#         ('d', POINTER(c_uint8)),
# 	SNDFILE* ('sndfile', ),
# 	float* ('buf', ),
# 	int ('period_size', ),
# 	int ('buf_size', ),
# ]

# fluid_synth_write_float(fluid_synth_t* synth, int len, void* lout,
#    int loff, int lincr, void* rout, int roff, int rincr)
# fluid_synth_write_float(dev->synth, dev->period_size, dev->buf, 0, 2,
#    dev->buf, 1, 2);

# get period_size from 'audio.period-size'
# buffer size = period_size
# Two buffers = left and right


FFMPEG_BIN = "/usr/bin/avconv"


def motherfucker(settings, synth, player):
    FLUID_PLAYER_PLAYING = 1
    period_size = c_int(0)
    fluid_settings_getint(settings, 'audio.period-size', byref(period_size))
    period_size = period_size.value
    try:
        proc = sp.Popen([FFMPEG_BIN, '-y', "-f", 's16le', '-ar', "44100",
                         '-ac', '2', '-i', '-', '-vn', '-f', 'mp3', '-ac', '2',
                         'pipe:1'],
                        stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        buff = (c_int16 * (period_size * 2))()
        while (fluid_player_get_status(player) == FLUID_PLAYER_PLAYING):
            r = fluid_synth_write_s16(
                synth,
                period_size,
                cast(buff, POINTER(c_int16)),
                0,
                2,
                cast(buff, POINTER(c_int16)),
                1,
                2
            )
            proc.stdin.write(buff)
            try:
                yield proc.stdout.read()
            except IOError:
                pass
            if (r != 0):
                print("Oh, that's embarassing...")
                break
        proc.stdin.close()
        while proc.poll():
            try:
                yield proc.stdout.read()
            except IOError:
                pass
    except:
        proc.kill()


def fast_render_loop(settings, synth, player):
    FLUID_PLAYER_PLAYING = 1

    renderer = new_fluid_file_renderer(synth)
    if not renderer:
        return

    while (fluid_player_get_status(player) == FLUID_PLAYER_PLAYING):
        if (fluid_file_renderer_process_block(renderer) != 0):
            break

    delete_fluid_file_renderer(renderer)


def play(midifile, sffile, output_filename):
    settings = new_fluid_settings()
    fluid_settings_setstr(settings, 'audio.driver', 'alsa')
    fluid_settings_setstr(settings, 'synth.verbose', 'no')
    fluid_settings_setstr(settings, 'midi.driver', 'alsa_seq')
    fluid_settings_setstr(settings, 'audio.file.name', output_filename)
    fluid_settings_setstr(settings, "player.timing-source", "sample")
    fluid_settings_setint(settings, "synth.parallel-render", 1)

    synth = new_fluid_synth(settings)
    player = new_fluid_player(synth)

    fluid_synth_sfload(synth, sffile, 1)

    fluid_player_add(player, midifile)
    fluid_player_play(player)

    fast_render_loop(settings, synth, player)

    delete_fluid_player(player)
    delete_fluid_synth(synth)
    delete_fluid_settings(settings)


def stream(midifile, sffile):
    settings = new_fluid_settings()
    fluid_settings_setstr(settings, 'audio.driver', 'alsa')
    fluid_settings_setstr(settings, 'synth.verbose', 'no')
    fluid_settings_setstr(settings, 'midi.driver', 'alsa_seq')
    fluid_settings_setstr(settings, 'audio.file.type', 'raw')
    fluid_settings_setstr(settings, "player.timing-source", "sample")
    fluid_settings_setint(settings, "synth.parallel-render", 1)

    synth = new_fluid_synth(settings)
    player = new_fluid_player(synth)

    fluid_synth_sfload(synth, sffile, 1)

    fluid_player_add(player, midifile)
    fluid_player_play(player)

    for piece in motherfucker(settings, synth, player):
        yield piece

    delete_fluid_player(player)
    delete_fluid_synth(synth)
    delete_fluid_settings(settings)


def get_hash():
    hasher = hashlib.sha1()
    hasher.update(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    return hasher.hexdigest()

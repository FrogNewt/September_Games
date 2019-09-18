#!/usr/bin/env python3

import pyglet

snd = pyglet.media.load('sounds/Night_Riding.wav')

p = pyglet.media.Player()
p.queue(snd)
p.play()
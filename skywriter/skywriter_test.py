#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Einfaches Skript zur Nutzung der Skywriter-Erweiterung.

Sources:
 - https://github.com/pimoroni/skywriter-hat
 - http://docs.pimoroni.com/skywriter/index.html

@author: Christian Wichmann
@license: GNU GPL
"""

import signal

import skywriter


@skywriter.airwheel()
def airwheel(rotation_delta):
    print('rotation: ', rotation_delta)


@skywriter.flick()
def flick(start, finish):
    print('flicked: ', start, finish)


@skywriter.move()
def move(x, y, z):
    print('moved ', x, y, z)


@skywriter.tap(repeat_rate=2, position='north')
def tap():
    print('tapped')


@skywriter.double_tap(repeat_rate=2, position='north')
def double_tap(position):
    print('double_tapped in: ', position)


@skywriter.touch(repeat_rate=2, position='north')
def touch():
    print('touched')


if __name__ == '__main__':
    signal.pause()

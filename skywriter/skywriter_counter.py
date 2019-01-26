#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zähler mit Gestensteuerung.

Quellen:
 - https://github.com/pimoroni/skywriter-hat
 - http://docs.pimoroni.com/skywriter/index.html

@author: Christian Wichmann
@license: GNU GPL
"""

import sys
import time

import skywriter


def output_counter(start_value=42):
    counter = start_value
    while True:
        print('Wert: ', counter)
        counter += yield 


@skywriter.airwheel()
def airwheel(rotation_delta):
    if rotation_delta > 0:
        counter.send(10)
    elif rotation_delta < 0:
        counter.send(-10)


@skywriter.flick()
def flick(start, finish):
    if start == 'west' and finish == 'east':
        counter.send(1)
    elif start == 'east' and finish == 'west':
        counter.send(-1)


@skywriter.double_tap(repeat_rate=1)
def double_tap(position):
    # TODO: Finde einen Weg, den Thread der Event Chain in der Bibliothek 
    # skywriter zu beenden!
    sys.exit()


if __name__ == '__main__':
    counter = output_counter()
    counter.send(None)
    while True:
        time.sleep(1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zahlenraten

@author: Christian Wichmann
@license: GNU GPL
"""

import random


print("Zahlenraten")

# Zufallszahl berechnen
random.seed()
zielzahl = random.randint(1,100)

# Spieler raten lassen und Hinweis geben
eingabe = 0
while zielzahl is not eingabe:
    eingabe = int(input("Zahl eingeben: "))
    if eingabe > zielzahl:
        print("Zahl zu groß!")
    elif eingabe < zielzahl:
        print("Zahl zu klein!")
    else:
        print("Sie haben gewonnen!")


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
correct_answer = random.randint(1,100)

# Spieler raten lassen und Hinweis geben
player_input = 0
while player_input is not correct_answer:
    player_input = int(input("Zahl eingeben: "))
    if player_input > correct_answer:
        print("Zahl zu groß!")
    elif player_input < correct_answer:
        print("Zahl zu klein!")
    else:
        print("Sie haben gewonnen!")


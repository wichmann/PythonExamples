
"""
Spiel "Zahlenraten", in Python programmiert.
"""

import random


print('Zahlenraten')

# initialisiere des Zufallszahlengenerators
random.seed()
# erzeuge neue Zufallszahl zwischen 1 und 100
correct_answer = random.randint(1,100)

player_input = 0

# solange der Spieler noch nicht die richtige Antwort eingegebe hat...
while player_input != correct_answer:
    # lese Eingabe vom Spieler ein und parse den eingegebenen String zu einer Ganzzahl (int)
    player_input = int(input('Zahl eingeben: '))
    # vergleiche Eingabe mit der richtigen Antwort
    if player_input > correct_answer:
        print('Zahl zu groß!')
    elif player_input < correct_answer:
        print('Zahl zu klein!')
    else:
        print('Sie haben gewonnen!')

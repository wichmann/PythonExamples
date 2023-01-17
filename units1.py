
"""
Einfaches Skript zur Umrechnung von Einheiten.

Um die benötigte Bibliothek "pint" [1] zu installieren, bitte das folgende
Kommando ausführen:

    pip install pint

[1] https://pint.readthedocs.io/en/latest/

"""

import pint

einheiten = pint.UnitRegistry()
Q_ = einheiten.Quantity


max_geschwindigkeit = 130 * einheiten.kilometers / einheiten.hours

distance = einheiten.parse_expression(input('Bitte Entfernung eingeben: '))
print('Eingegebene Entfernung: {}'.format(distance))

time = einheiten.parse_expression(input('Bitte Zeit eingeben: '))
print('Eingegebene Zeit: {}'.format(time))

speed = distance / time
print('Geschwindigkeit: {}'.format(speed))
print('Geschwindigkeit in m/s: {}'.format(speed.to(einheiten.meter / einheiten.second)))
print('Geschwindigkeit in Basiseinheiten: {}'.format(speed.to_base_units()))

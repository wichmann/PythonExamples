
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


volumen = 0.5 * einheiten.liter
dichte = 1 * einheiten.kilogram / (einheiten.decimeter ** 3)
raumtemperatur = Q_(21.0, einheiten.degC)
endtemperatur = Q_(373.14, einheiten.kelvin)
wärmekapazität = 4.181 * einheiten.kilojoule / (einheiten.kilogram * einheiten.kelvin)
zeit = 10 * einheiten.seconds

leistung = (wärmekapazität * volumen * dichte * (endtemperatur - raumtemperatur)) / zeit
print(leistung.to(einheiten.watt))

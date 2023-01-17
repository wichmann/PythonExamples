#!/usr/bin/env python3

"""
Währungsrechner mit Kommandozeilen-Oberfläche.

@author: Christian Wichmann
"""

import sys


def currency_calculator():
    """Gibt Benutzermeldungen aus und errechnet anschließend das Ergebnis."""
    
    # Lese Ausgangsbetrag ein
    print("===== "+app_name+" =====")
    print("Bitte umzurechnenden Betrag in einer der möglichen Währungen eingeben: " + ", ".join(currencies))
    source_input = str(input("Betrag: ")).upper()

    # Finde mögliche Zielwährungen
    for currency in currencies:
        if currency in source_input:
            source_currency = currency
            break
    available_destination_currencies = [c for c in currencies if c is not source_currency]
    
    # Zielwährung abfragen
    print("Bitte eine der möglichen Zielwährungen eingeben: " + ", ".join(available_destination_currencies))
    dest_input = str(input("Zielwährung: ")).upper()
    
    # Setze Zielwährung und berechne Umrechnungsfaktor
    for currency in currencies:
        if currency in dest_input:
            dest_currency = currency
            break

    # Berechne Zielbetrag
    source_value = float(source_input[:source_input.find(source_currency)])
    dest_value = source_value * calculateFactor(source_currency, dest_currency)
    
    # Gib Zielbetrag in Zielwährung aus
    print("Zielbetrag: " + "%0.2f" % dest_value + " " + dest_currency)


def calculateFactor(source_currency, destination_currency):
    """Berechnet den Umrechnungsfaktor für die ausgewählten Währungen"""
    factor = 1
    # zuerst Umrechnung in EUR
    factor *= factors[source_currency]
    # dann Umrechnung in Zielwährung
    factor /= factors[destination_currency]
    return factor


if __name__ == "__main__":
    
    # Konstanten für das Programm
    app_name = "Währungsrechner"
    
    # Liste mit allen Währungen und Umrechnungsfaktoren in EUR
    currencies = ("EUR", "USD", "YEN")
    factors = {"EUR": 1,
               "USD": 0.751540658,
               "YEN": 0.00774763265}

    currency_calculator()


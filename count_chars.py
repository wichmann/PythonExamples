#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zeichen in Text zählen

@author: Christian Wichmann
@license: GNU GPL
"""

import string
from collections import defaultdict


def count_chars(text, count_numbers=True, count_upper=True,
                count_lower=True, count_special=False):
    """Zählt alle Zeichen in einem gegebenen Text, deren Typ gezählt werden
    soll und gibt die resultierende Statistik als Dictionary zurück."""
    if text is None:
        return {}

    def should_count_char(char):
        """Gibt zurück, ob das übergebene Zeichen gezählt werden soll."""
        return (string.printable.count(char) and
               (count_numbers and char.isdigit()
                or count_upper and char.isupper()
                or count_lower and char.islower()
                or count_special and not char.isalnum()))

    # result als Dictionary mit Integer-Werten definieren
    result = defaultdict(int)
    for char in text:
        if should_count_char(char):
            result[char] += 1

    return result


def print_statistics(statistics):
    """Ausgeben eines Statistik über alle gefundenen Zeichen."""
    for char in sorted(statistics, key=statistics.get, reverse=True):
        number_of_chars = sum(statistics.values())
        bar_length = int(statistics[char] * 100.0 / number_of_chars * 4)
        bar = "#" * max(min(bar_length, 60), 1) + " [%3i]" % statistics[char]
        print("%10s %1s: %s" % (char_type(char), char, bar))


def char_type(character=""):
    """Gibt einen String zurück, der das übergebene Zeichen beschreibt."""
    if character.isdigit():
        return "Zahl"
    elif character.isalpha():
        return "Buchstabe"
    else:
        return "Zeichen"


if __name__ == "__main__":
    EXAMPLE = """Freilebende Gummibärchen gibt es nicht. Man kauft sie in
    Packungen an der Kinokasse (1,68 €). Dieser Kauf ist der Beginn einer fast
    erotischen und sehr ambivalenten Beziehung Gummibärchen-Mensch. Zuerst
    genießt man. Dieser Genuß umfaßt alle Sinne. Man wühlt in den Gummibärchen,
    man fühlt sie. Gummibärchen haben eine Konsistenz wie weichgekochter
    Radiergummi. Die Tastempfindung geht auch ins Sexuelle. Das bedeutet nicht
    unbedingt, daß das Verhältnis zum Gummibärchen ein geschlechtliches wäre,
    denn prinzipiell sind diese geschlechtsneutral. Nun sind Gummibärchen
    weder wabbelig noch zäh; sie stehen genau an der Grenze. Auch das macht
    sie spannend. Gummibärchen sind auf eine aufreizende Art weich. Und da sie
    weich sind, kann man sie auch ziehen. Ich mache das sehr gerne. Ich sitze
    im dunklen Kino und ziehe meine Gummibärchen in die Länge, ganz ganz
    langsam. Man will sie nicht kaputtmachen, und dann siegt doch die Neugier,
    wieviel Zug so ein Bärchen aushält. (Vorstellbar sind u.a. Gummibärchen-
    Expander für Kinder und Genesende). Forscherdrang und gleichzeitig das
    Böse im Menschen erreichen den Climax, wenn sich die Mitte des gezerrten
    Bärchens von Millionen Mikrorissen weiß färbt und gleich darauf das
    zweigeteilte Stück auf die Finger zurückschnappt. Man hat ein Gefühl der
    Macht über das hilflose, nette Gummibärchen. Und wie man damit umgeht:
    Mensch erkenne dich selbst! Jetzt ist es so, daß Gummibärchen ja nicht
    gleich Gummibärchen ist. Ich bevorzuge das klassische Gummibärchen,
    künstlich gefärbt und aromatisiert. Mag sein, daß es eine Sentimentalität
    ist."""
    RESULT = count_chars(EXAMPLE)
    print_statistics(RESULT)

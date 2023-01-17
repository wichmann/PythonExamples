#!/usr/bin/env python3

"""
Ausgabe der Größe aller Dateien in einem Verzeichnis.

HINWEIS: Dieses Programm wurde für die Benutzung unter Linux geschrieben!

@author: Christian Wichmann
@license: GNU GPL
"""

import os, fnmatch, shutil

app_title = "Dateigrößenberechnung"
directory = "/home/christian/"
destination = "/home/christian/temp/"
filter_string = "*.png"
count_files = 0
size_files = 0

# Banner ausgeben
print(app_title)

# Rekursiv alle Dateien suchen, die dem Filter entsprechen und die Größe aufaddieren
for root, dirnames, filenames in os.walk(directory):
    for filename in fnmatch.filter(filenames, filter_string):
        count_files += 1
        size_files += os.path.getsize(os.path.join(root, filename))
        
        # Datei ins Ziel kopieren
        #if not os.path.exists(destination):
        #    os.mkdir(destination)
        #shutil.copy(os.path.join(root, filename), destination)


print("Anzahl der Dateien: " + str(count_files))
print("Größe der Dateien: " + str(size_files))


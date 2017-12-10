#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Einfache SQLite-Konsole.

Nach Eingabe eines Dateinames für die SQLite-Datenbank können SQL-Kommandos
direkt in die Kommandozeile eingegeben werden. Bei Abfragen gefundene Datensätze
werden in Tabellenform ausgegeben. Die Konsole kann durch STRG+C beendet werden.

Vor dem Starten muss die Bibliothek 'tabulate' installiert werden:

    pip install tabulate

@author: Christian Wichmann
@date: 2016-06-28
"""

import os
import sqlite3
import readline

from tabulate import tabulate


# activate auto completion in command line
readline.parse_and_bind('tab: complete')

# ask user for database file name
db_file_name = input('Dateiname der Datenbank: ')

# check if database file already exists
if os.path.exists(db_file_name):
    print('Öffne Datenbank ({}).'.format(db_file_name))
else:
    print('Erzeuge neue Datenbank ({}).'.format(db_file_name))

# open database file
connection = sqlite3.connect(db_file_name)
cursor = connection.cursor()

try:
    while True:
        # get next SQL command
        sql_command = input('SQL-Befehl: ')
        if not sql_command:
            continue
        with connection:
            try:
                # execute SQL command and fetch all rows
                result = cursor.execute(sql_command)
                connection.commit()
                rows = result.fetchall()
                if rows:
                    names = [description[0] for description in cursor.description]
                    print(tabulate(rows, names, tablefmt='grid'))
                else:
                    print('SQL-Befehl erfolgreich!')
            except sqlite3.OperationalError as e:
                print('Fehler beim Ausführen des SQL-Befehls: {}'.format(e))
except KeyboardInterrupt:
    print('Auf Wiedersehen!')
finally:
    connection.close()


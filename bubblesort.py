#-------------------------------------------------------------------------------
# Name:        bubblesort
# Purpose:
#
# Author:      Christian Wichmann
#
# Created:     14.02.2014
# Copyright:   (c) Christian Wichmann 2014
# Licence:     GNU GPL
#-------------------------------------------------------------------------------

def main():
    zahlen = []
    sortiert = False
    anzahl = int(input('Anzahl der Zahlen eingeben: '))
    for i in range(anzahl):
        zahl = input('Zahl eingeben: ')
        zahlen.append(zahl)
    while not sortiert:
        sortiert = True
        for i in range(anzahl-1):
            if zahlen[i] > zahlen[i+1]:
                zwischenspeicher = zahlen[i]
                zahlen[i] = zahlen[i+1]
                zahlen[i+1] = zwischenspeicher
                sortiert = False
    for i in range(anzahl):
        print(zahlen[i])

if __name__ == '__main__':
    main()

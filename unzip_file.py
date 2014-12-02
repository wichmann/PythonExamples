#!/usr/bin/env python3

"""
ZIP-Datei entpacken

Quelle: http://stackoverflow.com/questions/19483775/python-zipfile-extract-doesnt-extract-all-files

@author: Christian Wichmann
@license: GNU GPL
"""

import zipfile


def unzip(zip_datei_name, ziel_verzeichnis):
    with zipfile.ZipFile(zip_datei_name, 'r') as zf:
        zf.extractall(ziel_verzeichnis)


if __name__ == '__main__':
    unzip('./testfile.zip', '.')

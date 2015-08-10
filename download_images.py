#!/usr/bin/env python3
"""
Herunterladen aller Bilddateien von einer HTML-Seite in ein Verzeichnis.
"""

__author__ = 'Christian Wichmann <wichmann@bbs-os-brinkstr.de>'
__license__ = 'GNU GPL'
__version__ = '0.0.1'


import os
import sys
import requests
import posixpath
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from requests.exceptions import MissingSchema, ConnectionError


OVERWRITE_DIRECTORY = True


def get_image_list(url):
    """
    Herunterladen einer HTML-Seite und heraussuchen aller Links auf Bilddateien.

    :param url: URL, deren Bilddateien herausgesucht werden sollen
    :return: Liste mit den Links aller Bilddateien der HTML-Seite
    """
    try:
        html_code = requests.get(url).text
    except MissingSchema:
        print('Bitte in der URL nicht das Protokol vergessen. www.google.de -> http://www.google.de')
        sys.exit(0)
    except ConnectionError:
        print('Die angegebene URL konnte nicht gelesen werden.')
        sys.exit(0)
    soup = BeautifulSoup(html_code)
    return [image['src'] for image in soup.findAll('img')]


def download_image_to_disk(base_url, image_link):
    """
    Herunterladen einer Bilddatei von einem Server und abspeichern der Datei in
    einem Unterverzeichnis.

    Das Zielverzeichnis hat den Hostnamen des Servers von dem die HTML-Seite
    geladen wurde. (http://www.example.com/images.html -> www.example.com)

    :param base_url: URL, von der die HTML-Seite geladen wurde
    :param image_link: Link zur Bilddatei auf dem Server
    :return: Dateiname unter dem die Bilddatei lokal gespeichert wurde
    """
    image_url = urljoin(base_url, image_link)
    domain_name = urlparse(url).hostname
    try:
        os.makedirs(domain_name, exist_ok=OVERWRITE_DIRECTORY)
    except FileExistsError:
        print('Ziel-Verzeichnis "{}" existiert bereits.'.format(domain_name))
        sys.exit(0)
    image_name = posixpath.basename(urlparse(image_url).path)
    print('Lade Datei "{image}" von "{domain}" herunter...'.format(domain=domain_name,
                                                                   image=shorten_file_name(image_name)))
    image_file_name_on_disk = os.path.join(domain_name, image_name)
    with open(image_file_name_on_disk, 'wb') as image_on_disk:
        image_on_disk.write(requests.get(image_url).content)
    return image_file_name_on_disk


def shorten_file_name(file_name, max_length=30):
    """
    Kürzt einen Dateinamen so ein, dass der erste Teil vor der Dateierweiterung
    höchstens eine maximale Anzahl von Zeichen lang ist. Die maximale Länge
    kann als optionaler Parameter angegeben werden.

    :param file_name: Dateiname, der gekürzt werden soll
    :param max_length: maximale Länge des Dateinamens ohne seine Dateierweiterung
    :return: gekürzte Version des Dateinamens
    """
    file_name_without_extension, extension = os.path.splitext(file_name)
    shortened_file_name = file_name_without_extension[:max_length] + (file_name_without_extension[max_length:] and '...')
    return ''.join((shortened_file_name, extension))


if __name__ == '__main__':
    print('Starten...')
    if len(sys.argv) != 2:
        script_name = os.path.basename(sys.argv[0])
        print('Ungültiger Aufruf: python3 {} [url]'.format(script_name))
        exit()

    url = sys.argv[1]
    images = get_image_list(url)
    for image in images:
        download_image_to_disk(url, image)
    print('Tschüß!')

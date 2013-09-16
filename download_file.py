#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Datei von Server herunterladen

Quelle: https://developers.google.com/edu/python/utilities

@author: Christian Wichmann
@license: GNU GPL
"""

import urllib
import urllib.request


def print_url_content(url):
    try:
        request = urllib.request.urlopen(url)
        print(request.read())
    except IOError:
        print('Problem reading url: ', url)
    

def save_url_content(url, filename):
    try:
        request = urllib.request.urlopen(url)
        local_file = open(filename, 'w')
        local_file.write(request.read().decode('utf-8'))
    except IOError:
        print('Problem reading url: ', url)


def download_file(url, filename):
    try:
        # request data from url
        request = urllib.request.urlopen(url)
        header = request.info()
        
        # writing data to local file...
        print('Loading file from url.', end='')
        chunk_size = 1024
        local_file = open(filename, 'wb')
        while True:
            chunk = request.read(chunk_size)
            # ...as long there is data
            if not chunk:
                break
            local_file.write(chunk)
            print('.', end='')
    except IOError:
        print('Problem reading url: ', url)
    print('')


if __name__ == '__main__':
    print_url_content('http://www.bbs-os-brinkstr.de')
    save_url_content('http://www.bbs-os-brinkstr.de', 'temp.html')
    download_file('http://www.bbs-os-brinkstr.de/fileadmin/0_intern/Schulleitung/Terminrahmenplan_public/Terminrahmenplan_2013_2014.pdf', 'temp.pdf')



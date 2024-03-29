#!/usr/bin/env python3

"""
Thumbnail für eine Datei erzeugen (benötigt Python Imaging Library)

Quelle: http://effbot.org/imagingbook/introduction.htm

@author: Christian Wichmann
@license: GNU GPL
"""

import os, sys
from PIL import Image

size = 128, 128

for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, "JPEG")
        except IOError:
            print("cannot create thumbnail for %s" % infile)

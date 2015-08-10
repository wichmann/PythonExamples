#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Einfacher Webserver, der den Pfad zur gesuchten Ressource als Information
ausgibt. Der Server kann durch Drücken von Ctrl-C gestoppt werden.

Quelle: https://wiki.python.org/moin/BaseHttpServer

@author: Christian Wichmann
@license: GNU GPL v2
"""

import time
import http.server


HOST_NAME = '192.168.10.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9020


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        """Sende Antwort auf GET-Anfrage."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>Title goes here.</title></head>'.encode('utf8'))
        self.wfile.write('<body><p>This is a test.</p>'.encode('utf8'))
        self.wfile.write('<p>You accessed path: {}</p>'.format(self.path).encode('utf8'))
        self.wfile.write('</body></html>'.encode('utf8'))

if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Starte Server - {host}:{port}'.format(host=HOST_NAME, port=PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Stoppe Server - {host}:{port}'.format(host=HOST_NAME, port=PORT_NUMBER))

#!/usr/bin/env python3

"""
Echo-Server 2

Quelle: http://wiki.python.org/moin/TcpCommunication

@author: Christian Wichmann
@license: GNU GPL
"""

import socketserver
import socket


class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Echo the back to the client
        data = self.request.recv(BUFFER_SIZE)
        print('{}: {}'.format(self.client_address[0], data))
        #self.request.send(data)
        self.request.send(data)
        #return

if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 5005
    BUFFER_SIZE = 20
    server = socketserver.TCPServer((HOST, PORT), EchoHandler)
    server.allow_reuse_address = True
    server.address_family = socket.AF_INET
    server.serve_forever()

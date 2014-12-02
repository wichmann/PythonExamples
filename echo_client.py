#!/usr/bin/env python3

"""
Echo-Client

Quelle: http://wiki.python.org/moin/TcpCommunication

@author: Christian Wichmann
@license: GNU GPL
"""

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
    message = str(input())
    s.send(bytes(message, 'utf-8'))
    data = s.recv(BUFFER_SIZE)    
    print("received data: {}".format(data))
s.close()

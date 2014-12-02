#!/usr/bin/env python3

"""
Echo-Server

Quelle: http://wiki.python.org/moin/TcpCommunication

@author: Christian Wichmann
@license: GNU GPL
"""

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address: {}'.format(addr))
while True:
    data = conn.recv(BUFFER_SIZE)
    if data:
        print("received data: {}".format(data))
        conn.send(data)  # echo
conn.close()

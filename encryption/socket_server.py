#!/usr/bin/env python3

"""
Server code to use TLS connection over low-level socket.

Source: http://stackoverflow.com/questions/15820634/tls-echo-server-and-echoclient-in-python-crashes

@author: Christian Wichmann
@license: GNU GPL
"""

import socket
import ssl


def main():
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allow reusing the port to prevent TIME_WAIT state for TCP connection (only while developing!)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind to an unused port on the local machine
    HOST, PORT = '127.0.0.1', 1717
    server_socket.bind((HOST, PORT))

    # listen for connection
    server_socket.listen (1)
    tls_server = ssl.wrap_socket(server_socket, ssl_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE,
                                server_side=True, keyfile='./server.key', certfile='./server.crt')

    print('Server started')

    # accept connection
    try:
        connection, client_address = tls_server.accept()
    except ssl.SSLError as error:
        print('Error in SSL library:', error)
        return
    print ('Connection from ', client_address)

    finished = False
    while not finished:
        # send and receive data from the client socket
        message = connection.recv(1024).decode('utf8')
        print('Client send: ', message)
        if message=='quit':
            finished= True
        connection.send(message.encode('utf8'))

    # close connections and socket
    connection.shutdown(socket.SHUT_RDWR)
    connection.close()
    tls_server.shutdown(socket.SHUT_RDWR)
    tls_server.close()
    #server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()


if __name__ == "__main__":
    main()

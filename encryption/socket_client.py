#!/usr/bin/env python3

"""
Client to use TLS connection over low-level socket.

Source: http://stackoverflow.com/questions/15820634/tls-echo-server-and-echoclient-in-python-crashes

@author: Christian Wichmann
@license: GNU GPL
"""

import socket
import ssl


def main():
    # create socket and wrap it in TLS connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tls_client = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLSv1_2,
                                cert_reqs=ssl.CERT_REQUIRED, ca_certs="./server.crt")
    # Note:
    # In this snippet only the server is validated by the client using the
    # servers certificate. Additionally the server could use a client certificate
    # to validate its authenticity. Change the certificate file from server.crt to
    # server2.crt to see that authentification is done!

    # connect to the server on localhost
    HOST, PORT = '127.0.0.1', 1717
    try:
        tls_client.connect((HOST, PORT))
    except ssl.SSLError as error:
        print('Error in SSL library:', error)
        return

    finished = False
    while not finished:
        message = input('Enter message ("quit" to exit program): ')
        # send message out, explicitly encoded as UTF-8
        tls_client.send(message.encode('utf8'))
        # receive data from server and print it on screen
        response = tls_client.recv(1024).decode('utf8')
        print('Received from client: ', response)
        if response == 'quit':
            finished = True

    # close the socket
    client_socket.close()


if __name__ == "__main__":
    main()

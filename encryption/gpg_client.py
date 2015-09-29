#!/usr/bin/env python3

"""
Client code to use manual GPG en/decryption.

To be working, the GnuPG executable has to be somewhere in the path.

THIS CODE SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS! YOU SHOULD
NEVER ATTEMPT TO DEVELOP YOUR OWN CRYPTO SYSTEM!!!

Source: https://pythonhosted.org/python-gnupg/

@author: Christian Wichmann
@license: GNU GPL
"""

import gnupg
import socket 


RECIPIENT = 'Bob Test'


def main(gpg):
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server on localhost
    HOST, PORT = '127.0.0.1', 1717
    client_socket.connect((HOST, PORT))

    finished = False
    while not finished:
        message = input('Enter message ("quit" to exit program): ')
        # send message out, explicitly encoded as UTF-8
        encrypted_data = gpg.encrypt(message, RECIPIENT)
        if message == 'quit':
            finished = True
        else:
            client_socket.send(str(encrypted_data).encode('ascii'))

    # close the socket
    client_socket.close()


if __name__ == "__main__":
    gpg = gnupg.GPG(gnupghome='./gpg/')
    main(gpg)

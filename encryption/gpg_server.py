#!/usr/bin/env python3

"""
Server code to use manual GPG en/decryption.

To be working, the GnuPG executable has to be somewhere in the path.

THIS CODE SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS! YOU SHOULD
NEVER ATTEMPT TO DEVELOP YOUR OWN CRYPTO SYSTEM!!!

Source: https://pythonhosted.org/python-gnupg/

@author: Christian Wichmann
@license: GNU GPL
"""

import gnupg
import socket 


KEY_OWNER = 'Bob Test'
DEBUG = False


def prepare_keys(gpg):
    # create keys and store them locally
    input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, name_real=KEY_OWNER)
    key = gpg.gen_key(input_data)
    public_keys = gpg.list_keys()
    private_keys = gpg.list_keys(True)
    if DEBUG:
        print('Public keys:', public_keys)
        print('Private keys:', private_keys)


def main(gpg):
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allow reusing the port to prevent TIME_WAIT state for TCP connection (only while developing!)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind to an unused port on the local machine
    HOST, PORT = '127.0.0.1', 1717
    server_socket.bind((HOST, PORT))

    # listen for connection
    server_socket.listen (1)
    print('Server started')

    # accept connection
    connection, client_address = server_socket.accept()
    print('Connection from ', client_address)

    finished = False
    while not finished:
        # send and receive data from the client socket
        data = connection.recv(2048)
        if not data:
            break
        decrypted_data = str(gpg.decrypt(data))
        print('Client send: ', decrypted_data)
        if decrypted_data == u'quit':
            finished= True

    # close connections and socket
    connection.shutdown(socket.SHUT_RDWR)
    connection.close()
    server_socket.close()


if __name__ == "__main__":
    gpg = gnupg.GPG(gnupghome='./gpg/')
    # preparing key ring (only necessary at first run!)
    prepare_keys(gpg)
    main(gpg)

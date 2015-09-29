# Secure Connections with Python

## Generating key and certificate

    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
    openssl pkcs12 -export -in server.crt -inkey server.key -out server.p12
    openssl pkcs12 -in server.p12 -nodes -out server.pem

[Source](http://stackoverflow.com/questions/15820634/tls-echo-server-and-echoclient-in-python-crashes)

## Python scripts
All script were tested under Ubuntu Linux Vivid with Python 2.7 and Python 3.4
respectively.

### TLS over low-level socket
Using a simple socket connection and encapsulating it in a TLS secured
connection.

    ./socket_server.py
    ./socket_client.py
    
### Secure connection using Twisted
Twisted is an event-driven networking engine written in Python. This high-level
API makes writing network code easier and less error-prone. To install twisted
library use the command:

    pip install twisted

After that the server and client can be executed: 

    ./twisted_server.py
    ./twisted_client.py

### Manual en/decryption with GnuPG
This script uses low-level sockets to transport GnuPG encrypted data from
client to the server. It works only if the GnuPG executable is somewhere in the
path. The script encryptes the data before sending it through the socket and
decryptes it, when receiving it.

The necessary keys are generated when the server is started for the first time!

THIS CODE SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS! YOU SHOULD NEVER
ATTEMPT TO DEVELOP YOUR OWN CRYPTO SYSTEM. USE PUBLIC STANDARDS!

    ./gpg_server.py
    ./gpg_client.py

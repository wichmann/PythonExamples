#!/usr/bin/env python

"""
Server code to use Twisted library for secure connection.

Source: http://twistedmatrix.com/documents/current/core/howto/ssl.html

@author: Christian Wichmann
@license: GNU GPL
"""

import sys

from twisted.internet import ssl, protocol, task, defer
from twisted.internet.protocol import Protocol
from twisted.python import log
from twisted.python.modules import getModule


class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.transport.write(data)


def main(reactor):
    HOST, PORT = 'localhost', 1717
    log.startLogging(sys.stdout)
    certData = getModule(__name__).filePath.sibling('server.pem').getContent()
    certificate = ssl.PrivateCertificate.loadPEM(certData)
    factory = protocol.Factory.forProtocol(Echo)
    reactor.listenSSL(PORT, factory, certificate.options())
    return defer.Deferred()


if __name__ == '__main__':
    task.react(main)

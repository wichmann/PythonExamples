#!/usr/bin/env python

"""
Client code to use Twisted library for secure connection.

Source: http://twistedmatrix.com/documents/current/core/howto/ssl.html

@author: Christian Wichmann
@license: GNU GPL
"""

from __future__ import print_function

from twisted.internet import ssl, task, protocol, endpoints, defer
from twisted.python.modules import getModule
from twisted.protocols.basic import LineReceiver


class EchoClient(LineReceiver):
    end = u"quit"

    def inputMessage(self):
        message = raw_input("Message: ").decode('utf8')
        self.sendLine(message.encode('utf8'))

    def connectionMade(self):
        self.inputMessage()

    def lineReceived(self, line):
        line = line.decode('utf8')
        print("Received from server:", line)
        if line == self.end:
            self.transport.loseConnection()
        else:
            self.inputMessage()


@defer.inlineCallbacks
def main(reactor):
    HOST, PORT = 'localhost', 1717
    factory = protocol.Factory.forProtocol(EchoClient)
    certData = getModule(__name__).filePath.sibling('server.pem').getContent()
    authority = ssl.Certificate.loadPEM(certData)
    options = ssl.optionsForClientTLS(u'example.com', authority)
    endpoint = endpoints.SSL4ClientEndpoint(reactor, HOST, PORT, options)
    echoClient = yield endpoint.connect(factory)

    done = defer.Deferred()
    echoClient.connectionLost = lambda reason: done.callback(None)
    yield done


if __name__ == '__main__':
    task.react(main)

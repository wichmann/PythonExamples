"""
Einfacher ECHO-Server, der alle zum Server gesendeten Daten direkt zurück
schickt.

Zum Starten des Programms:

    python3 echo_server3.py

Der Echo-Server kann wie folgt getestet werden:

    telnet 127.0.0.1 15000
"""
from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'Empfangen: ' + line)

print('Echo-Server starten...')
try:
    serv = TCPServer(('', 15000), EchoHandler)
    serv.serve_forever()
except KeyboardInterrupt:
    print('Echo-Server beendet!')

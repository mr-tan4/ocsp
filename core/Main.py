import sys
sys.path.append('/usr/src/app/ocsp')
from threading import Thread, Lock
from core.server.service.OCSPResponder import OCSPHandler
from http.server import HTTPServer
from core.rebbitMQClient.subScribe import ampqClient


class startHttpd(Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        if not isinstance(self.port, int):
            raise TypeError('port must by int type')
        httpd = HTTPServer(("0.0.0.0", self.port), OCSPHandler)
        httpd.serve_forever()


class startRebbitmq(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        ampqClient()


def start(port):
    startHttpd(port).start()
    startRebbitmq().start()


start(8000)

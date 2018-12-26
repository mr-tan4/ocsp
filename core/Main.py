import sys
from threading import Thread, Lock

sys.path.append("/Users/robert/PycharmProjects/ocsp")
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


if __name__ == '__main__':
    start(8000)

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
    port = int(sys.argv[1])
    if port < 8000 or port > 8999:
        raise ValueError('端口号在 8000-8999 之间')
    start(port)

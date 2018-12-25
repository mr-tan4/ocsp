from http.client import HTTPConnection


class BasicConnect(object):

    def __init__(self, url, port):
        self.url = url
        self.port = port

    def connection(self, func, value):
        value = func.format(value)
        connect = HTTPConnection(self.url, self.port)
        connect.request("GET", value)
        response = connect.getresponse()
        return response

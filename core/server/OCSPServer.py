from http.server import HTTPServer


class OCSPServer(object):

    def start(self, server_addr, clazz):
        httpd = HTTPServer(server_addr, clazz)
        httpd.serve_forever()

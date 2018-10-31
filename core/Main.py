from core.server.service.OCSPResponder import OCSPHandler
from http.server import HTTPServer

httpd = HTTPServer(("localhost",8080),OCSPHandler)
httpd.serve_forever()
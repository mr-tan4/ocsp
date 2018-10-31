from http.server import BaseHTTPRequestHandler
from asn1crypto import ocsp


class OCSPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])
        if content_type == 'application/ocsp-request':
            body = self.rfile.read(content_length)
            request = ocsp.OCSPRequest.load(body)
            tbs_request = request['tbs_request']
            request_list = tbs_request['request_list']
            single_request = request_list[0]
            req_cert = single_request['req_cert']


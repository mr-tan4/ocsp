from http.server import BaseHTTPRequestHandler
from asn1crypto import ocsp
from core.utils import utils as util
from core.OCSPResponseBuilder import OCSPResponseBuilder
from datetime import datetime, timezone
import base64
from core.redisClient.redisResultCache import Cache
from modules.configuration import Config


class OCSPHandler(BaseHTTPRequestHandler):
    logger = Config.getLogger(__name__, Config.log_file, Config.DEBUG)

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
            serial_number = req_cert['serial_number'].native
            self.logger.info('获取序列号为 %s 的ocsp请求' % str(serial_number))
            self.send_response(200)
            self.send_header("Content-type", 'application/ocsp-response')
            self.end_headers()
            self.write(serial_number=serial_number)

    def check(self, serial_number):
        ca_info = util().get_up_ca_info(serial_number=serial_number)
        ca_info = util().parse(ca_info)
        ca = ca_info['ca']
        ca_serial_number = ca_info['ca_serialNumber']
        certificate = util().get_my_data(serial_number=serial_number)
        status = util().check_all_up_ca_status(ca_serial_number=ca_serial_number)
        my_status = util().check_my_status(serial_number=serial_number)
        responder_info = util().get_responder(ca_serial_number)
        revocation_date = None
        if status == 'true' and my_status == 'Active':
            certificate_status = 'good'
        elif util().check_in_data_table(serial_number=serial_number) == '0':
            certificate_status = 'unknown'
        else:
            certificate_status = 'revoked'
            revocation_date = datetime.now(timezone.utc)

        ocsp_response = OCSPResponseBuilder(response_status='successful', certificate=certificate,
                                            certificate_status=certificate_status,
                                            revocation_date=revocation_date, issuer=ca).build(
            responder_certificate=responder_info['responder_cert'],
            responder_private_key=responder_info['responder_privatekey'])
        return ocsp_response

    def write(self, serial_number=None):
        if Cache().is_active(key=str(serial_number)):
            self.logger.info('序列号为 %s 的响应消息在缓存中已存在' % str(serial_number))
            ocsp_response = base64.b64decode(Cache().__get__(str(serial_number)))
        else:
            self.logger.info('序列号为 %s 的响应消息在缓存中不存在' % str(serial_number))
            ocsp_response = self.check(serial_number).dump()
            self.logger.debug('序列号为 %s 的响应消息成功生成' % str(serial_number))
            Cache().__set__(key=str(serial_number),
                            value=base64.b64encode(ocsp_response).decode('utf-8'))
        self.wfile.write(ocsp_response)
        self.logger.info('已响应了序列号为 %s 的ocsp请求' % str(serial_number))

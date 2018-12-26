import json
import base64
from core.restClient.restClient import BasicConnect
from asn1crypto import keys, x509
from modules.configuration import Config
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
import pymysql


class utils(object):

    def get_up_ca_info(self, serial_number=None):
        if serial_number is not None:
            connect = BasicConnect(Config.rest_server_url, Config.rest_server_port)
            response = connect.connection(Config.getUpCAData, serial_number)
            data = response.read().decode('utf-8')
            data = json.loads(data)
            certificate_data = base64.b64decode(data['certificate_data'])
            private_key_data = base64.b64decode(data['private_key'])
            data['certificate_data'] = certificate_data
            data['private_key_data'] = private_key_data
            return data

    def parse(self, data):
        serial_number = None
        # 得到ca证书信息
        ca = x509.Certificate().load(data['certificate_data'])
        for k, v in ca.native['tbs_certificate'].items():
            if k == 'serial_number':
                serial_number = v
        # 获取ca私钥信息
        ca_privateKey = keys.PrivateKeyInfo().load(data['private_key_data'])
        ca_info = {
            'ca': ca,
            'ca_privateKey': ca_privateKey,
            'ca_serialNumber': serial_number
        }
        return ca_info

    def check_all_up_ca_status(self, ca_serial_number=None):
        if ca_serial_number is not None:
            connect = BasicConnect(Config.rest_server_url, Config.rest_server_port)
            response = connect.connection(Config.checkAllUpCAStatus, ca_serial_number)
            data = response.read().decode('utf-8')
            response.close()
            return data

    def get_my_data(self, serial_number=None):
        if serial_number is not None:
            connect = BasicConnect(Config.rest_server_url, Config.rest_server_port)
            response = connect.connection(Config.getMyData, serial_number)
            data = response.read().decode('utf-8')
            certificate_data = base64.b64decode(data)
            return x509.Certificate().load(certificate_data)

    def check_my_status(self, serial_number=None):
        if serial_number is not None:
            connect = BasicConnect(Config.rest_server_url, Config.rest_server_port)
            response = connect.connection(Config.checkMyStatus, serial_number)
            data = response.read().decode('utf-8')
            return data

    def check_in_data_table(self, serial_number=None):
        connect = BasicConnect(Config.rest_server_url, Config.rest_server_port)
        response = connect.connection(Config.checkInDataTable, serial_number)
        data = response.read().decode('utf-8')
        return data

    def get_responder(self, serialNumber):
        connect = pymysql.connect(host=Config.db_url, port=Config.port, user=Config.user_name, password=Config.password,
                                  db=Config.db)
        cur = connect.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute(Config.sql.format(str(serialNumber) + '_responser'))
        rest = cur.fetchall()
        connect.commit()
        cur.close()
        connect.close()
        cert_data = base64.b64decode(rest[0]['cert'])
        responder_cert = x509.Certificate().load(cert_data)
        private_key_data = load_pem_private_key(rest[0]['privatekey'], password=b'trustasia-cloudpki',
                                                backend=default_backend())
        private_key_data = private_key_data.private_bytes(
            encoding=Encoding.DER,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption())
        responder_privatekey = keys.PrivateKeyInfo().load(private_key_data)
        responder_info = {
            'responder_cert': responder_cert,
            'responder_privatekey': responder_privatekey
        }
        return responder_info

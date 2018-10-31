import json
import base64
from OpenSSL.crypto import (load_certificate, dump_certificate, dump_privatekey, X509, X509Name, PKey, load_privatekey)
from OpenSSL.crypto import (TYPE_DSA, TYPE_RSA, FILETYPE_PEM, FILETYPE_ASN1)
from datetime import datetime
import textwrap

from core.restClient.restClient import BasicConnect
from core.restClient.restClientImpl import Client

if __name__ == '__main__':
    connect = BasicConnect('192.168.10.133', 8889)
    response = connect.connection('getUpCAData', '1540373954167')
    data = response.read().decode('utf-8')
    data = json.loads(data)
    certificate_data = base64.b64decode(data['certificate_data'])
    private_key_data = base64.b64decode(data['private_key'])
    x509 = load_certificate(FILETYPE_ASN1, certificate_data)
    privatekey = load_privatekey(FILETYPE_ASN1, private_key_data)
    print(privatekey)

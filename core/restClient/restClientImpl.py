from asn1crypto import x509, keys
from oscrypto import asymmetric
import base64


class Client(object):

    def __init__(self):
        pass


    def get_private_key(self, value):
        if value is not None:
            is_oscrypto = isinstance(value, asymmetric.PrivateKey)
            if not isinstance(value, keys.PrivateKeyInfo) and is_oscrypto:
                raise ValueError("%s" % value)
            elif is_oscrypto:
                value = value.asn1
        return value

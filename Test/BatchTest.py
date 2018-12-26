from unittest import TestCase, main
from asn1crypto import keys
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend


class batchTest(TestCase):

    @classmethod
    def tearDownClass(self):
        print('测试结束')

    @classmethod
    def setUp(self):
        print('开始测试')

    def test_decrypt(self):
        with open('/Users/robert/test.pri', 'r') as file:
            privateKey_data = file.read()
        print(privateKey_data.encode('utf-8'))
        data = load_pem_private_key(privateKey_data.encode('utf-8'), password=b'trustasia-cloudpki', backend=default_backend())
        privateKey = data.private_bytes(
            encoding=Encoding.DER,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption())
        private_key = keys.PrivateKeyInfo().load(privateKey)
        print(private_key.native)

if __name__ == '__main__':
    main()

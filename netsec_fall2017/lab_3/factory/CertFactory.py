import random, hashlib

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.x509.oid import NameOID

from playground.common import CipherUtil


class CertFactory(object):

    def __init__(self):
        super(CertFactory, self).__init__()
        self._path_prefix = '/Users/qiyanggu/Documents/keys/netsec/'
        # self._path_prefix = '/Users/ming/Desktop/netsec_keys/'
        # self._path_prefix = '/home/team6/ming/keys/'

    def getPrivateKeyForAddr(self, addr):
        return self.getContent(self._path_prefix + 'bb8_prik.pem')

    def getCertsForAddr(self, addr):
        chain = []
        chain.append(self.getContent(self._path_prefix + 'bb8.cert'))
        chain.append(self.getRootCert())
        return chain

    def getRootCert(self):
        return self.getContent(self._path_prefix + 'root.crt')

    def getPublicKeyForAddr(self, addr):
        return self.getContent((self._path_prefix + 'bb8_pubk.pem'))

    def getPreKey(self):
        seed = random.randint(0, 2 ** 64).to_bytes(8, byteorder='big')
        return hashlib.sha1(seed).digest()[:16]

    def getPubkFromCert(self, cert):
        cert_object = x509.load_pem_x509_certificate(cert, default_backend())
        return cert_object.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    @staticmethod
    def getContent(addr):
        content = b''
        with open(addr, 'rb') as fp:
            content = fp.read()
        if len(content) == 0:
            raise ValueError('No Content!')
        else:
            return content

    def GetCommonName(self, certBytes):
        cert = CipherUtil.getCertFromBytes(certBytes)
        commonNameList = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if len(commonNameList) != 1:
            return None
        commonNameAttr = commonNameList[0]
        return commonNameAttr.value


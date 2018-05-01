import random, hashlib

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID

from playground.common import CipherUtil

from ..contants import PATH_PREFIX


class CertFactory(object):

    def __init__(self):
        super(CertFactory, self).__init__()

    @classmethod
    def getPrivateKeyForAddr(cls, addr):
        pem_data = cls.getContent(PATH_PREFIX + 'r2d2.pem')
        return serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())

    @classmethod
    def getCertsForAddr(cls, addr):
        chain = []
        chain.append(cls.getContent(PATH_PREFIX + 'r2d2.crt'))
        chain.append(cls.getContent(PATH_PREFIX + 'bb8.crt'))
        chain.append(cls.getRootCert())
        return chain

    @classmethod
    def getRootCert(cls):
        return cls.getContent(PATH_PREFIX + 'root.crt')

    @classmethod
    def getPreKey(cls):
        seed = random.randint(0, 2 ** 64).to_bytes(8, byteorder='big')
        return hashlib.sha1(seed).digest()[:16]

    @classmethod
    def getPubkFromCert(cls, cert):
        cert_object = x509.load_pem_x509_certificate(cert, default_backend())
        # return cert_object.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
        return cert_object.public_key()

    @classmethod
    def getContent(cls, path):
        content = b''
        with open(path, 'rb') as fp:
            content = fp.read()
        if len(content) == 0:
            raise ValueError('No Content!')
        else:
            return content
    
    @classmethod
    def GetCommonName(cls, certBytes):
        cert = CipherUtil.getCertFromBytes(certBytes)
        commonNameList = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if len(commonNameList) != 1:
            return None
        commonNameAttr = commonNameList[0]
        return commonNameAttr.value


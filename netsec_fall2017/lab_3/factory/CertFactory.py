import random, hashlib
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from netsec_fall2017.lab_3.utils import CipherUtil
from cryptography.x509.oid import NameOID



class CertFactory(object):

    def __init__(self):
        super(CertFactory, self).__init__()
        # self._path_prefix = '/Users/qiyanggu/Documents/keys/netsec/'
        # self._path_prefix = '/Users/ming/Desktop/netsec_keys/'
        self._path_prefix = '/home/team6/ming/keys/'

    def getPrivateKeyForAddr(self, addr):
        # return self.getContent(self._path_prefix + 'bb8_prik.pem')
        return self.getContent(self._path_prefix + addr)

    def getCertsForAddr(self, addr):
        chain = []
        chain.append(self.getContent(self._path_prefix + addr))
        chain.append(self.getContent(self._path_prefix + 'bb8.cert'))
        chain.append(self.getRootCert())
        return chain

    def getRootCert(self):
        return self.getContent(self._path_prefix + 'root.crt')

    def getPublicKeyForAddr(self, addr):
        # return self.getContent((self._path_prefix + 'bb8_pubk.pem'))
        return self.getContent((self._path_prefix + addr))

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
        if len(commonNameList) != 1: return None
        commonNameAttr = commonNameList[0]
        return commonNameAttr.value

    def VerifyCertSignature(self, cert, issuer):
        try:
            issuer.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except:
            return False

    def comparename(self, peername, commonname):
        i = 0
        while i < len(commonname):
            if peername[i] != commonname[i]:
                return False
            i += 1
        return True


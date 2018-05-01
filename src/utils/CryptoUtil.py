import hmac

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class AESEngine:
    def __init__(self, key, IV):
        cipher = Cipher(algorithms.AES(key), modes.CTR(IV), backend=default_backend())
        self.encryptor = cipher.encryptor()
        self.decryptor = cipher.decryptor()

    def encrypt(self, data):
        return self.encryptor.update(data)

    def decrypt(self, data):
        return self.decryptor.update(data)

class HMACEngine:
    def __init__(self, key):
        self.__key = key

    def mac(self, data):
        mac = hmac.new(self.__key, digestmod="sha1")
        mac.update(data)
        return mac.digest()

    def verifyMac(self, data, verification_code):
        mac = self.mac(data)
        return mac == verification_code


class CryptoUtil(object):

    def __init__(self):
        super(CryptoUtil, self).__init__()

    @classmethod
    def RSAEncrypt(cls, pubk, plain_text):
        cipher_text = pubk.encrypt(
            plain_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return cipher_text

    @classmethod
    def RSADecrypt(cls, prik, cipher_text):
        plain_text = prik.decrypt(
            cipher_text,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm = hashes.SHA1(),
                label = None
            )
        )
        return plain_text

    @classmethod
    def AESEngine(cls, key, IV):
        # IV_asCtr = Counter.new(128, initial_value=int.from_bytes(IV, byteorder='big'))
        # return AES.new(key, counter=IV_asCtr, mode=AES.MODE_CTR)
        return AESEngine(key, IV)

    @classmethod
    def HMACEngine(self, key):
        # return HMAC.new(key, digestmod=SHA)
        return HMACEngine(key)
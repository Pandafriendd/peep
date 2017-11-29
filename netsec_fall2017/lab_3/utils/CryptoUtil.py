import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5, AES
from Crypto.Hash import HMAC, SHA
from Crypto.PublicKey import RSA
from Crypto.Util import Counter


class CryptoUtil(object):

    def __init__(self):
        super(CryptoUtil, self).__init__()

    @classmethod
    def RSAEncrypt(cls, key, plain_text):
        rsa_key = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(plain_text))
        return cipher_text

    @classmethod
    def RSADecrypt(cls, key, cipher_text):
        random_generator = Random.new().read
        rsa_key = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        plain_text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
        return plain_text

    @classmethod
    def AESCryptoEngine(cls, key, IV):
        IV_asCtr = Counter.new(128, initial_value=int.from_bytes(IV, byteorder='big'))
        return AES.new(key, counter=IV_asCtr, mode=AES.MODE_CTR)

    @classmethod
    def HMACEngine(self, key):
        return HMAC.new(key, digestmod=SHA)
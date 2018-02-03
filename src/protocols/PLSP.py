import random, hashlib

from playground.network.common import StackingProtocol
from playground.common import CipherUtil

from ..packets.PLSPacket import PLSPacket, PlsHello, PlsKeyExchange, PlsHandshakeDone, PlsData, PlsClose
from ..factory.CertFactory import CertFactory
from ..transport.PLSTransport import PLSTransport
from ..utils.CryptoUtil import CryptoUtil


class PLSP(StackingProtocol):

    def __init__(self):
        super(PLSP, self).__init__()
        # variables for transport
        self.transport = None
        self._deserializer = PLSPacket.Deserializer()
        # cert factory and cert vars
        self._private_key = None
        self._public_key = None
        self._pubk_for_other_side = None
        self._pre_key = None
        self._pre_key_for_other_side = None
        self._certs = []
        self._certs_for_other_side = []
        # vars for handshake
        self._nonce = None
        self._nonce_for_other_side = None
        self._state = 0
        self._messages_for_handshake = []
        self._hash_for_handshake = None
        # engines for data transmission
        self._encryption_engine = None
        self._decryption_engine = None
        self._MAC_engine_key = None
        self._verification_engine_key = None
        # self._MAC_engine = None
        # self._verification_engine = None


    def data_received(self, data):
        self._deserializer.update(data)
        for packet in self._deserializer.nextPackets():
            if isinstance(packet, PlsData):
                cipher_text = packet.Ciphertext
                verification_code = packet.Mac
                verification_engine = CryptoUtil.HMACEngine(self._verification_engine_key)
                verification_engine.update(cipher_text)
                if verification_engine.digest() == verification_code:
                    plain_text = self._decryption_engine.decrypt(cipher_text)
                    self.higherProtocol().data_received(plain_text)
                else:
                    # pass
                    self.terminate_connection("validation error")
            elif isinstance(packet, PlsHello):
                '''
                1. store certs from the other side (?)
                2. get the other side's pubk from the certs
                3. store the other side's nonce
                4. store this message for SHA1
                '''
                self._certs_for_other_side = list(packet.Certs)
                self._nonce_for_other_side = packet.Nonce
                self._pubk_for_other_side = CertFactory.getPubkFromCert(packet.Certs[0])
                self._messages_for_handshake.append(packet.__serialize__())

                '''
                verify certs
                '''
                tmp_cert_list = []
                for cert_for_other_side in self._certs_for_other_side:
                    tmp_cert_list.append(CipherUtil.getCertFromBytes(cert_for_other_side))
                peer_name = self.transport.get_extra_info("peername")[0]
                common_name = CertFactory.GetCommonName(packet.Certs[0])

                root = CipherUtil.getCertFromBytes(CertFactory.getRootCert())
                issuer = CipherUtil.RSA_SIGNATURE_MAC(root.public_key())

                if str(peer_name).startswith(common_name) and CipherUtil.ValidateCertChainSigs(tmp_cert_list) and (packet.Certs[-1] == CertFactory.getRootCert() or issuer.verify(packet.Certs[-1], root.signature)):
                    if self._state == 0:
                        # start to send plshello
                        self._nonce = random.randint(0, 2 ** 64)
                        pls_hello = PlsHello(Nonce=self._nonce, Certs=self._certs)
                        pls_hello_bytes = pls_hello.__serialize__()
                        self.transport.write(pls_hello_bytes)
                        self._state = 2
                        self._messages_for_handshake.append(pls_hello_bytes)
                    elif self._state == 1:
                        self._pre_key = CertFactory.getPreKey()
                        pls_key_exchange = PlsKeyExchange(PreKey=CryptoUtil.RSAEncrypt(self._pubk_for_other_side, self._pre_key), NoncePlusOne=self._nonce_for_other_side + 1)
                        pls_key_exchange_bytes = pls_key_exchange.__serialize__()
                        self.transport.write(pls_key_exchange_bytes)
                        self._state = 3
                        self._messages_for_handshake.append((pls_key_exchange_bytes))
                    else:
                        # pass
                        self.terminate_connection("Status error")
                else:
                    # pass
                    self.terminate_connection("PlsHello error")

            elif isinstance(packet, PlsKeyExchange):
                if packet.NoncePlusOne == self._nonce + 1:
                    self._pre_key_for_other_side = CryptoUtil.RSADecrypt(self._private_key, packet.PreKey)
                    self._messages_for_handshake.append(packet.__serialize__())
                    if self._state == 2:
                        self._pre_key = CertFactory.getPreKey()
                        pls_key_exchange = PlsKeyExchange(
                            PreKey=CryptoUtil.RSAEncrypt(self._pubk_for_other_side, self._pre_key),
                            NoncePlusOne=self._nonce_for_other_side + 1)
                        pls_key_exchange_bytes = pls_key_exchange.__serialize__()
                        self.transport.write(pls_key_exchange_bytes)
                        self._state = 4
                        self._messages_for_handshake.append(pls_key_exchange_bytes)
                    elif self._state == 3:
                        m = hashlib.sha1()
                        m.update(self._messages_for_handshake[0] + self._messages_for_handshake[1] +
                                 self._messages_for_handshake[2] + self._messages_for_handshake[3])
                        self._hash_for_handshake = m.digest()
                        pls_handshake_done = PlsHandshakeDone(ValidationHash=self._hash_for_handshake)
                        self.transport.write(pls_handshake_done.__serialize__())
                        self._state = 5
                    else:
                        # pass
                        self.terminate_connection("Status error")
                else:
                    # pass
                    self.terminate_connection("PlsKeyExchange error")


            elif isinstance(packet, PlsHandshakeDone):
                validation_hash = packet.ValidationHash
                if self._state == 4:
                    m = hashlib.sha1()
                    m.update(self._messages_for_handshake[0] + self._messages_for_handshake[1] +
                             self._messages_for_handshake[2] + self._messages_for_handshake[3])
                    self._hash_for_handshake = m.digest()
                    if self._hash_for_handshake == validation_hash:
                        pls_handshake_done = PlsHandshakeDone(ValidationHash=self._hash_for_handshake)
                        self.transport.write(pls_handshake_done.__serialize__())
                        self._state = 6
                        # ------------ set symmetric variables ------------
                        self.set_symmetric_variables(False)
                        # ------------ connect to higher protocol ------------
                        self.higherProtocol().connection_made(PLSTransport(self.transport, self))
                    else:
                        # pass
                        self.terminate_connection("PlsHandshakeDone validation error")

                elif self._state == 5:
                    if self._hash_for_handshake == validation_hash:
                        self.set_symmetric_variables(True)
                        self.higherProtocol().connection_made(PLSTransport(self.transport, self))
                        self._state = 6
                    else:
                        # pass
                        self.terminate_connection("PlsHandshakeDone validation error")
                else:
                    # pass
                    self.terminate_connection("status error")

            elif isinstance(packet, PlsClose):
                print("connection closed by the other side")
                self.transport.close()
            else:
                print('PLSP is waiting for a PLS packet.')

    def set_symmetric_variables(self, is_client):
        self._public_key = CertFactory.getPubkFromCert(self._certs[0])
        nonce_comb = None
        prek_comb = None
        if is_client:
            nonce_comb = self._nonce.to_bytes(8, byteorder='big') + self._nonce_for_other_side.to_bytes(8, byteorder='big')
            # pubk_comb = self._public_key + self._pubk_for_other_side
            prek_comb = self._pre_key + self._pre_key_for_other_side
        else:
            nonce_comb = self._nonce_for_other_side.to_bytes(8, byteorder='big') + self._nonce.to_bytes(8, byteorder='big')
            # pubk_comb = self._pubk_for_other_side + self._public_key
            prek_comb = self._pre_key_for_other_side + self._pre_key

        seed = b'PLS1.0' + nonce_comb + prek_comb

        block_0 = hashlib.sha1(seed).digest()
        block_1 = hashlib.sha1(block_0).digest()
        block_2 = hashlib.sha1(block_1).digest()
        block_3 = hashlib.sha1(block_2).digest()
        block_4 = hashlib.sha1(block_3).digest()

        block = block_0 + block_1 + block_2 + block_3 + block_4

        if is_client:
            self._encryption_engine = CryptoUtil.AESCryptoEngine(block[:16], block[32:48])
            self._decryption_engine = CryptoUtil.AESCryptoEngine(block[16:32], block[48:64])
            # self._MAC_engine = CryptoUtil.HMACEngine(block[64:80])
            self._MAC_engine_key = block[64:80]
            # self._verification_engine = CryptoUtil.HMACEngine(block[80:96])
            self._verification_engine_key = block[80:96]
        else:
            self._encryption_engine = CryptoUtil.AESCryptoEngine(block[16:32], block[48:64])
            self._decryption_engine = CryptoUtil.AESCryptoEngine(block[:16], block[32:48])
            # self._MAC_engine = CryptoUtil.HMACEngine(block[80:96])
            self._MAC_engine_key = block[80:96]
            self._verification_engine_key = block[64:80]            
            # self._verification_engine = CryptoUtil.HMACEngine(block[64:80])

    def process_data(self, data):
        cipher_text = self._encryption_engine.encrypt(data)
        mac_engine = CryptoUtil.HMACEngine(self._MAC_engine_key)
        mac_engine.update(cipher_text)
        verification_code = mac_engine.digest()
        pls_data = PlsData(Ciphertext=cipher_text, Mac=verification_code)
        self.transport.write(pls_data.__serialize__())

    def terminate_connection(self, info):
        print(info)
        pls_close = PlsClose(Error=info)
        pls_close_bytes = pls_close.__serialize__()
        self.transport.write(pls_close_bytes)
        self.transport.close()



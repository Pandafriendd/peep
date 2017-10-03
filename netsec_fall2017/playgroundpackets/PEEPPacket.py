import random, zlib
from playground.network.packet.fieldtypes.attributes import Optional
from playground.network.packet.fieldtypes import UINT8, UINT16, UINT32, BUFFER
from playground.network.packet import PacketType
from playground.common import CustomConstant as Constant


class PEEPPacket(PacketType):
    DEFINITION_IDENTIFIER = 'peep.packet'
    DEFINITION_VERSION = '1.0'

    FIELDS = [
        ('Type', UINT8),
        ('SequenceNumber', UINT32({Optional: True})),
        ('Checksum', UINT16),
        ("Acknowledgement", UINT32({Optional: True})),
        ("Data", BUFFER({Optional: True}))
    ]

    SYN = Constant(intValue=0, strValue='SYN')
    SYN_ACK = Constant(intValue=1, strValue='SYN-ACK')
    ACK = Constant(intValue=2, strValue='ACK')
    RIP = Constant(intValue=3, strValue='RIP')
    RIP_ACK = Constant(intValue=4, strValue='RIP-ACK')
    DATA = Constant(intValue=5, strValue='DATA')

    PACKET_TYPES = [SYN, SYN_ACK, ACK, RIP_ACK, DATA]

    def calculateChecksum(self):
        original_checksum = self.Checksum
        self.Checksum = 0
        bytes = self.__serialize__()
        self.Checksum = original_checksum
        return zlib.adler32(bytes) & 0xffff

    def updateChecksum(self):
        self.Checksum = self.calculateChecksum()

    def verifyChecksum(self):
        return self.Checksum == self.calculateChecksum()

    @classmethod
    def Create_SYN(cls):
        seq_number = random.randint(0, 2**16)
        packet = cls(Type=cls.SYN, SequenceNumber=seq_number, Checksum=0)
        packet.updateChecksum()
        return packet

    @classmethod
    def Create_SYN_ACK(cls, client_seq):
        seq_number = random.randint(0, 2**16)
        packet = cls(Type=cls.SYN_ACK, SequenceNumber=seq_number, Checksum=0, Acknowledgement=client_seq+1)
        packet.updateChecksum()
        return packet

    @classmethod
    def Create_ACK(cls, server_seq, client_seq):
        seq_number = client_seq + 1
        packet = cls(Type=cls.ACK, SequenceNumber=seq_number, Checksum=0, Acknowledgement=server_seq+1)
        packet.updateChecksum()
        return packet

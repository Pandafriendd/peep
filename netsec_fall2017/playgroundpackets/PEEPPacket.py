from playground.network.packet.fieldtypes.attributes import Optional
from playground.network.packet.fieldtypes import UINT8, UINT16, UINT32, BUFFER
from playground.network.packet import PacketType


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
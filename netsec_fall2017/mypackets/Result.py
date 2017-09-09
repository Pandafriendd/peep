from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, UINT32


class Result(PacketType):
    DEFINITION_IDENTIFIER = 'lab1b.Qiyang.Result'
    DEFINITION_VERSION = '0.1'

    FIELDS = [
        ('ID', UINT8),
        ('price', UINT32)
    ]

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import ListFieldType, UINT32, STRING


class ListTest(PacketType):
    DEFINITION_IDENTIFIER = 'lab1b.Qiyang.lt'
    DEFINITION_VERSION = '0.1'

    FIELDS = [
        ('ID', UINT32),
        ('ls', ListFieldType(UINT32)),
        ('s', STRING)
    ]

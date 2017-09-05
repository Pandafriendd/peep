from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32


class RequestMenu(PacketType):
    DEFINITION_IDENTIFIER = 'lab1b.Qiyang.RequestMenu'
    DEFINITION_VERSION = '0.1'

    FIELDS = []

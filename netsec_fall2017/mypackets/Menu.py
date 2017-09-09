from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, STRING


class Menu(PacketType):
    DEFINITION_IDENTIFIER = 'lab1b.Qiyang.Menu'
    DEFINITION_VERSION = '0.1'

    FIELDS = [
        ('ID', UINT8),
        ('setMealA', STRING),
        ('setMealB', STRING),
        ('setMealC', STRING)
    ]

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, STRING


class Order(PacketType):
    DEFINITION_IDENTIFIER = 'lab1b.Qiyang.Order'
    DEFINITION_VERSION = '0.1'

    FIELDS = [
        ('ID', UINT8),
        ('setMeal', STRING)
    ]

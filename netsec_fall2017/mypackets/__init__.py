from playground.network.packet import PacketType

from .RequestMenu import RequestMenu
from .Menu import Menu
from .Order import Order
from .Result import Result
from .ListTest import ListTest


def init_packet(packet, attr_list):
    if not isinstance(packet, PacketType):
        raise TypeError('Init an non-packet object')
    else:
        for index in range(len(packet.FIELDS)):
            packet.__setattr__(packet.FIELDS[index][0], attr_list[index])

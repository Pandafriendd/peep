import asyncio

from playground.network.packet import PacketType
# from ..mypackets import RequestMenu, Menu, Order, Result


class OrderingClientProtocol(asyncio.Protocol):

    def __init__(self, packet, loop):
        if isinstance(packet, PacketType):
            self.transport = None
            self.packet = packet
            self.loop = loop
        else:
            raise ValueError('This is not a packet')

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.packet.__serialize__())
        pass

    def data_received(self, data):
        pass

    def connection_lost(self, exc):
        print('over')
        self.transport = None
        pass

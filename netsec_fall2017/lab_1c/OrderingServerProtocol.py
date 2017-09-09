import asyncio

from playground.network.packet import PacketType


class OrderingServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.received = []

    def connection_made(self, transport):
        self.transport = transport
        pass

    def data_received(self, data):
        message = PacketType.Deserialize(data)
        print(message)
        self.received.append(message)

    def connection_lost(self, exc):
        self.transport = None

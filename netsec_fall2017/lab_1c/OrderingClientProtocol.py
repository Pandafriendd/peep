import asyncio


class OrderingClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        pass

    def data_received(self, data):
        pass

    def connection_lost(self, exc):
        pass

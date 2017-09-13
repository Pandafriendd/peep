import asyncio
import playground

from playground.network.packet import PacketType
from netsec_fall2017.mypackets import Result, init_packet


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        rs = Result()
        init_packet(rs, [1, 10])
        transport.write(rs.__serialize__())
        print('Data sent: {!r}'.format(rs))

    def data_received(self, data):
        message = PacketType.Deserialize(data)
        print('Data received: {!r}'.format(data))

    def connection_lost(self, exc):
        print('The server closed the connection')


loop = asyncio.get_event_loop()
# coro = loop.create_connection(lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888)
coro = playground.getConnector().create_playground_connection(lambda: EchoClientProtocol(), '4.5.3.9596', 9000)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()

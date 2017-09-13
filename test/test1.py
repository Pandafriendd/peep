import asyncio
import playground

from playground.network.packet import PacketType


class EchoServer(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))

    def data_received(self, data):
        message = PacketType.Deserialize(data)
        print('Data Received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


es = EchoServer()
loop = asyncio.get_event_loop()
# coro = loop.create_server(lambda: es, '127.0.0.1', 8888)
coro = playground.connect.getConnector().create_playground_server(lambda: es, 9000)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].gethostname()))
loop.run_forever()
loop.close()





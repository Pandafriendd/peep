import asyncio
import playground
from ..lab_1c import OrderingServerProtocol

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    sp = OrderingServerProtocol()
    coro = playground.connect.getConnector().create_playground_server(lambda: sp, 900)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].gethostname()))
    loop.run_forever()

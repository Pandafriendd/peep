import asyncio
import playground
from playground.network.common import StackingProtocolFactory

from ..lab_1c import OrderingServerProtocol
from ..lab_1e import PassThrough1, PassThrough2

'''

You should run by `python -m netsec_fall2017.lab_1d.server` in top level dir

'''

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    ptConnector = playground.Connector(protocolStack=f)

    playground.setConnector('pt', ptConnector)

    coro = playground.getConnector('pt').create_playground_server(lambda: OrderingServerProtocol(), 101)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].gethostname()))
    loop.run_forever()

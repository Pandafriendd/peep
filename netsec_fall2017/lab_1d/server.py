import asyncio
import playground
import logging

from playground.network.common import StackingProtocolFactory

from ..lab_1c import OrderingServerProtocol
from ..lab_1e import PassThrough1, PassThrough2
from ..lab_2.protocols import PEEPServer, PassThroughProtocol


logging.getLogger().setLevel(logging.NOTSET)
logging.getLogger().addHandler(logging.StreamHandler())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)

    # f = StackingProtocolFactory(lambda: PassThroughProtocol(), lambda: PEEPServer())
    # f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    # ptConnector = playground.Connector(protocolStack=f)

    # playground.setConnector('pt', ptConnector)

    coro = playground.getConnector('lab2_protocol').create_playground_server(lambda: OrderingServerProtocol(), 101)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].gethostname()))
    loop.run_forever()

import asyncio
import logging
import sys
import playground

# from playground.network.common import StackingProtocolFactory

from ..lab_1c import OrderingClientProtocol
# from ..lab_1e import PassThrough1, PassThrough2
# from ..lab_2.protocols import PassThroughProtocol, PEEPClient
from ..mypackets import RequestMenu, Order
from ..mypackets import init_packet

# logging.getLogger().setLevel(logging.NOTSET)
# logging.getLogger().addHandler(logging.StreamHandler())


def generate_order(menu):
    order = Order()
    init_packet(order, [menu.ID, menu.setMealA])
    return order


if __name__ == '__main__':
    mode = sys.argv[1]
    loop = asyncio.get_event_loop()
    # loop.set_debug(enabled=True)
    cp = OrderingClientProtocol(lambda: RequestMenu(), generate_order)

    # f = StackingProtocolFactory(lambda: PassThroughProtocol(), lambda: PEEPClient())
    # f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    # ptConnector = playground.Connector(protocolStack=f)

    # playground.setConnector('pt', ptConnector)

    coro = playground.getConnector('lab2_protocol').create_playground_connection(lambda: cp, mode, 101)
    loop.run_until_complete(coro)
    loop.run_forever()

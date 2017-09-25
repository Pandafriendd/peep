import asyncio
import sys
import playground

from playground.network.common import StackingProtocolFactory

from ..lab_1c import OrderingClientProtocol
from ..lab_1e import PassThrough1, PassThrough2
from ..mypackets import RequestMenu, Order
from ..mypackets import init_packet

'''

You should run by `python -m netsec_fall2017.lab_1d.client` in top level dir

'''


def generate_order(menu):
    order = Order()
    init_packet(order, [menu.ID, menu.setMealA])
    return order


if __name__ == '__main__':
    mode = sys.argv[1]
    loop = asyncio.get_event_loop()
    cp = OrderingClientProtocol(lambda: RequestMenu(), generate_order)

    f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    ptConnector = playground.Connector(protocolStack=f)

    playground.setConnector('pt', ptConnector)

    coro = playground.getConnector('pt').create_playground_connection(lambda: cp, mode, 101)
    loop.run_until_complete(coro)
    loop.run_forever()

import asyncio
import playground

from ..lab_1c import OrderingClientProtocol
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
    loop = asyncio.get_event_loop()
    cp = OrderingClientProtocol(lambda: RequestMenu(), generate_order)
    coro = playground.getConnector().create_playground_connection(lambda: cp, '4.5.3.9596', 101)
    loop.run_until_complete(coro)
    loop.run_forever()

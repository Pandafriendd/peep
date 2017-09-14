import asyncio
import playground

from ..lab_1c import OrderingClientProtocol
from ..mypackets import RequestMenu, Menu, Order
from ..mypackets import init_packet


def generate_order(menu):
    order = Order()
    init_packet(order, [menu.ID, menu.setMealA])
    return order


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    cp = OrderingClientProtocol(lambda: RequestMenu(), generate_order)
    coro = playground.connect.getConnector().create_playground_connection(lambda: cp, '4.5.3.9596', 900)
    loop.run_until_complete(coro)
    loop.run_forever()

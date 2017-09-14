import asyncio

from playground.network.packet import PacketType

from ..mypackets import RequestMenu, Menu, Order, Result
from ..mypackets import init_packet


class OrderingServerProtocol(asyncio.Protocol):
    ORDER_NUMBER = 0

    def __init__(self, menu_dict={'A': 5, 'B': 10, 'C': 15}):
        self.transport = None
        self.menu_dict = menu_dict
        self.receiving_state = 0
        self.received_message = []

    def connection_made(self, transport):
        print("Received a connection from {}".format(transport.get_extra_info("peername")))
        self.transport = transport

    def data_received(self, data):
        data_after_deserialization = None
        deserializer = PacketType.Deserializer()

        while len(data) > 0:
            chunk, data = data[:8], data[8:]
            deserializer.update(chunk)
            for packet in deserializer.nextPackets():
                data_after_deserialization = packet
                self.received_message.append(data_after_deserialization)

        if isinstance(data_after_deserialization, RequestMenu):
            if self.receiving_state == 0:
                print('Server receives a request menu message with state %s' % self.receiving_state)
                menu = self.generate_packet_of_menu()
                print('Server sends a menu message')
                self.receiving_state += 1
                self.transport.write(menu.__serialize__())
            else:
                raise ValueError('Wrong state when server receives request menu message')

        elif isinstance(data_after_deserialization, Order):
            if self.receiving_state == 1:
                print('Server receive an Order message with state %s' % self.receiving_state)
                result = self.generate_packet_of_result(data_after_deserialization.ID, data_after_deserialization.setMeal)
                print('Server sends a Result message')
                self.receiving_state = -1
                self.transport.write(result.__serialize__())
            else:
                raise ValueError('Wrong state when server receives order message')
        else:
            raise TypeError('Receive incorrect packet')

    def connection_lost(self, exc):
        self.transport = None

    def generate_packet_of_menu(self):
        menu = Menu()
        set_meals = [k for k in self.menu_dict.keys()]
        init_packet(menu, [OrderingServerProtocol.ORDER_NUMBER] + set_meals)
        OrderingServerProtocol.ORDER_NUMBER += 1
        return menu

    def generate_packet_of_result(self, packet_id, set_meal):
        result = Result()
        price = self.menu_dict[set_meal]
        init_packet(result, [packet_id, price])
        return result


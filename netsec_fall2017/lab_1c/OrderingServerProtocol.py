import asyncio

from playground.network.packet import PacketType

from ..mypackets import RequestMenu, Menu, Order, Result
from ..mypackets import init_packet


class OrderingServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.order_number = 0
        self.menu_dict = self.get_menu_val()
        self.received_message = []

    def connection_made(self, transport):
        self.transport = transport
        pass

    def data_received(self, data):
        data_after_deserialization = None
        deserializer = PacketType.Deserializer()

        while len(data) > 0:
            chunk, data = data[:8], data[8:]
            deserializer.update(chunk)
            for packet in deserializer.nextPackets():
                print('Server received {!r}'.format(packet))
                data_after_deserialization = packet
                self.received_message.append(data_after_deserialization)

        if isinstance(data_after_deserialization, RequestMenu):
            print('Server receive a RequestMenu message')
            menu = self.generate_packet_of_menu()
            self.transport.write(menu.__serialize__())

        elif isinstance(data_after_deserialization, Order):
            print('Server receive an Order message')
            result = self.generate_packet_of_result(data_after_deserialization.ID, data_after_deserialization.setMeal)
            self.transport.write(result.__serialize__())

        else:
            raise ValueError('Receive incorrect packet')

    def connection_lost(self, exc):
        self.transport = None

    def generate_packet_of_menu(self):
        menu = Menu()
        set_meals = [k for k in self.menu_dict.keys()]
        init_packet(menu, [self.order_number] + set_meals)
        self.order_number += 1
        return menu

    def generate_packet_of_result(self, packet_id, set_meal):
        result = Result()
        price = self.menu_dict[set_meal]
        init_packet(result, [packet_id, price])
        return result

    @staticmethod
    def get_menu_val():
        return {
            'A': 5,
            'B': 10,
            'C': 15
        }

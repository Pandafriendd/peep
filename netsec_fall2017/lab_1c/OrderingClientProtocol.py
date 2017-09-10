import asyncio
import random

from playground.network.packet import PacketType

from ..mypackets import RequestMenu, Menu, Order, Result
from ..mypackets import init_packet


class OrderingClientProtocol(asyncio.Protocol):

    def __init__(self, for_test=True):
        self.transport = None
        self.received_message = []
        self.for_test = for_test

    def connection_made(self, transport, rm=RequestMenu()):
        if not isinstance(rm, RequestMenu):
            raise TypeError('Init with an incorrect packet')
        self.transport = transport
        print('Client sends a RequestMenu message')
        self.transport.write(rm.__serialize__())

    def data_received(self, data):
        data_after_deserialization = None
        deserializer = PacketType.Deserializer()

        while len(data) > 0:
            chunk, data = data[:8], data[8:]
            deserializer.update(chunk)
            for packet in deserializer.nextPackets():
                data_after_deserialization = packet
                self.received_message.append(data_after_deserialization)

        if isinstance(data_after_deserialization, Menu):
            print('Client receives a Menu message')
            set_meals = [
                data_after_deserialization.setMealA,
                data_after_deserialization.setMealB,
                data_after_deserialization.setMealC
            ]
            order = self.generate_packet_of_order(data_after_deserialization.ID, set_meals)
            print('Clients sends an Order message')
            self.transport.write(order.__serialize__())

        elif isinstance(data_after_deserialization, Result):
            if not self.for_test:
                self.transport.close()
        else:
            raise TypeError('Receive incorrect packet')

    def connection_lost(self, exc):
        print('over')
        self.transport = None

    @staticmethod
    def generate_packet_of_order(packet_id, set_meals):
        order = Order()
        init_packet(order, [packet_id, set_meals[random.randint(0, 2)]])
        return order

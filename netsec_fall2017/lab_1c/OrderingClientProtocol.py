import asyncio

from playground.network.packet import PacketType
from ..mypackets import RequestMenu, Menu, Order, Result


class OrderingClientProtocol(asyncio.Protocol):

    def __init__(self, cb1, cb2):
        self.transport = None
        self.receiving_state = 0
        self.received_message = []
        self._cb1 = cb1
        self._cb2 = cb2

    def connection_made(self, transport):
        self.transport = transport
        packet = self._cb1()
        if isinstance(packet, RequestMenu):
            print('Client sends a request menu message')
            self.transport.write(packet.__serialize__())
        else:
            raise TypeError('Send a packet which is not a RequestMenu packet')

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
            if self.receiving_state == 0:
                print('Client receives a menu message')
                self.receiving_state += 1
                packet = self._cb2(data_after_deserialization)
                if isinstance(packet, Order):
                    print('Client sends an order message')
                    self.transport.write(packet.__serialize__())
                else:
                    raise TypeError('Send a packet which is not a RequestMenu packet')
            else:
                raise ValueError('Wrong state when client receives a menu message')

        elif isinstance(data_after_deserialization, Result):
            if self.receiving_state == 1:
                print('Client receives a result message')
                self.receiving_state = -1
                self.transport.close()
            else:
                raise ValueError('Wrong state when client receives a result message')
        else:
            raise TypeError('Receive incorrect packet')

    def connection_lost(self, exc):
        print('Connection is over.')
        self.transport = None

    def send_request_menu(self, packet):
        if isinstance(packet, RequestMenu):
            print('Client sends a request menu message')
            self.transport.write(packet.__serialize__())
        else:
            raise TypeError('Send a packet which is not a RequestMenu packet')

    def send_order(self, packet):
        if isinstance(packet, Order):
            print('Client sends a order message')
            self.transport.write(packet.__serialize__())
        else:
            raise TypeError('Send a packet which is not a Order packet')

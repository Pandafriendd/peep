import unittest

from playground.network.testing import MockTransportToProtocol

from ..mypackets import RequestMenu, Menu, Order, Result
from ..mypackets import init_packet

from .OrderingServerProtocol import OrderingServerProtocol as ServerProtocol
from .OrderingClientProtocol import OrderingClientProtocol as ClientProtocol

"""
    You should NOT run the code directly by `python submission.py`.
    You should go to the top level of file dir, and use `python -m netsec_fall2017.lab_1c.submission`.
    There is a .sh script file in top level dir, you could also use `./start.sh 1c` to run the code.
"""


class MockTransportTestCase1(unittest.TestCase):

    server_protocol = None
    client_protocol = None

    @classmethod
    def setUpClass(cls):
        cls.server_protocol = ServerProtocol()

        cb1 = lambda: RequestMenu()
        cb2 = cls.generate_order

        cls.client_protocol = ClientProtocol(cb1, cb2)
        ct, st = MockTransportToProtocol.CreateTransportPair(cls.server_protocol, cls.client_protocol)
        cls.server_protocol.connection_made(ct)
        cls.client_protocol.connection_made(st)

    def test_t01_valueEqual_RequestMenu(self):
        request_menu = RequestMenu()
        self.assertEqual(MockTransportTestCase1.server_protocol.received_message[0], request_menu)

    def test_t02_valueEqual_Menu(self):
        menu = Menu()
        init_packet(menu, [0, 'A', 'B', 'C'])
        self.assertEqual(MockTransportTestCase1.client_protocol.received_message[0], menu)

    def test_t03_valueEqual_Order(self):
        menu_id = MockTransportTestCase1.client_protocol.received_message[0].ID
        order = Order()
        init_packet(order, [menu_id, 'A'])
        self.assertEqual(MockTransportTestCase1.server_protocol.received_message[1], order)

    def test_t04_valueEqual_Result(self):
        menu_id = MockTransportTestCase1.client_protocol.received_message[0].ID
        result = Result()
        init_packet(result, [menu_id, 5])
        self.assertEqual(MockTransportTestCase1.client_protocol.received_message[1], result)

    def test_t05_valueEqual_state_whenProcessEnds(self):
        self.assertEqual(MockTransportTestCase1.server_protocol.receiving_state, -1)
        self.assertEqual(MockTransportTestCase1.client_protocol.receiving_state, -1)

    def test_t06_exception_sendPacketWhenTransportCloses(self):
        rm = RequestMenu()
        with self.assertRaises(AttributeError):
            MockTransportTestCase1.client_protocol.send_request_menu(rm)

    @staticmethod
    def generate_order(menu):
        order = Order()
        order.ID = menu.ID
        order.setMeal = menu.setMealA
        return order

#
#
#

'''
@unittest.skip('These tests are invalid now.')
class MockTransportTestCase2(unittest.TestCase):

    server_protocol = None
    client_protocol = None

    @classmethod
    def setUpClass(cls):
        print('--------- -------------- ---------')
        print('--------- New Test Class ---------')
        print('--------- -------------- ---------')
        cls.server_protocol = ServerProtocol()
        cls.client_protocol = ClientProtocol()
        st, ct = MockTransportToProtocol.CreateTransportPair(cls.server_protocol, cls.client_protocol)
        cls.server_protocol.connection_made(st)
        cls.client_protocol.connection_made(ct)

    def test_t07_valueEqual_automaticallyIncreasingID(self):
        self.assertEqual(MockTransportTestCase2.server_protocol.ORDER_NUMBER, 1)

    def test_t08_exception_sendInValidPacket(self):
        with self.assertRaises(TypeError):
            MockTransportTestCase2.client_protocol.send_request_menu('Test')

    def test_t09_exception_sendPacketAtWrongState(self):
        order = Order()
        init_packet(order, [1, 'A'])
        with self.assertRaises(ValueError):
            MockTransportTestCase2.client_protocol.send_order(order)

    def test_t10_exception_returnPacketAtWrongState(self):
        result = Result()
        init_packet(result, [1, 5])
        with self.assertRaises(ValueError):
            MockTransportTestCase2.client_protocol.data_received(result.__serialize__())
'''

if __name__ == '__main__':
    unittest.main()

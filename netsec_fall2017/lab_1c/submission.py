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


class MockTransportTestCase(unittest.TestCase):

    server_protocol = None
    client_protocol = None

    @classmethod
    def setUpClass(cls):
        print('================================================')
        cls.server_protocol = ServerProtocol()
        cls.client_protocol = ClientProtocol()

        ts = MockTransportToProtocol(cls.server_protocol)
        tc = MockTransportToProtocol(cls.client_protocol)

        cls.server_protocol.connection_made(tc)
        cls.client_protocol.connection_made(ts)
        print('================================================')

    def test_mock_transport_valueEqual_RequestMenu(self):
        request_menu = RequestMenu()
        self.assertEqual(MockTransportTestCase.server_protocol.received_message[0], request_menu)

    def test_mock_transport_valueEqual_Menu(self):
        menu = Menu()
        init_packet(menu, [0, 'A', 'B', 'C'])
        self.assertEqual(MockTransportTestCase.client_protocol.received_message[0], menu)

    def test_mock_transport_valueEqual_Order(self):
        order1 = Order()
        order2 = Order()
        order3 = Order()
        init_packet(order1, [0, 'A'])
        init_packet(order2, [0, 'B'])
        init_packet(order3, [0, 'C'])
        self.assertIn(MockTransportTestCase.server_protocol.received_message[1], [order1, order2, order3])

    def test_mock_transport_valueEqual_Result(self):
        menu_dict = {
            'A': 5,
            'B': 10,
            'C': 15
        }
        result = Result()
        init_packet(result, [0, menu_dict[MockTransportTestCase.server_protocol.received_message[1].setMeal]])
        self.assertEqual(MockTransportTestCase.client_protocol.received_message[1], result)

    def test_mock_transport_error_ClientInit(self):
        sp = ServerProtocol()
        cp = ClientProtocol()

        ts = MockTransportToProtocol(sp)
        tc = MockTransportToProtocol(cp)

        sp.connection_made(tc)
        with self.assertRaises(TypeError):
            cp.connection_made(ts, 'Test')

    def test_mock_transport_error_ServerReceive(self):
        with self.assertRaises(TypeError):
            MockTransportTestCase.server_protocol.data_received('Test')

    def test_mock_transport_error_ClientReceive(self):
        with self.assertRaises(TypeError):
            MockTransportTestCase.client_protocol.data_received('Test')


if __name__ == '__main__':
    unittest.main()

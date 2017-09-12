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
        cls.server_protocol = ServerProtocol()
        cls.client_protocol = ClientProtocol()

        ts = MockTransportToProtocol(cls.server_protocol)
        tc = MockTransportToProtocol(cls.client_protocol)

        cls.server_protocol.connection_made(tc)
        cls.client_protocol.connection_made(ts)

    def test_1_valueEqual_RequestMenu(self):
        request_menu = RequestMenu()
        MockTransportTestCase.client_protocol.send_request_menu(request_menu)
        self.assertEqual(MockTransportTestCase.server_protocol.received_message[0], request_menu)

    def test_2_valueEqual_Menu(self):
        menu = Menu()
        init_packet(menu, [0, 'A', 'B', 'C'])
        self.assertEqual(MockTransportTestCase.client_protocol.received_message[0], menu)

    def test_3_valueEqual_Order(self):
        menu_id = MockTransportTestCase.client_protocol.received_message[0].ID
        order = Order()
        init_packet(order, [menu_id, 'A'])
        MockTransportTestCase.client_protocol.send_order(order)
        self.assertEqual(MockTransportTestCase.server_protocol.received_message[1], order)

    def test_4_valueEqual_Result(self):
        menu_id = MockTransportTestCase.client_protocol.received_message[0].ID
        result = Result()
        init_packet(result, [menu_id, 5])
        self.assertEqual(MockTransportTestCase.client_protocol.received_message[1], result)

    def test_5_valueEqual_state_whenProcessEnds(self):
        self.assertEqual(MockTransportTestCase.server_protocol.receiving_state, -1)
        self.assertEqual(MockTransportTestCase.client_protocol.receiving_state, -1)
        print('============= Test cases above are normal process when client interacts with server =============')
        print('============= Test cases below are abnormal process when client interacts with server =============')

    def test_6_exception_sendPacketAtWrongState(self):
        rm = RequestMenu()
        with self.assertRaises(ValueError):
            MockTransportTestCase.client_protocol.send_request_menu(rm)

    def test_7_exception_returnPacketAtWrongState(self):
        MockTransportTestCase.server_protocol.receiving_state = 0
        MockTransportTestCase.server_protocol.received_message = []
        with self.assertRaises(ValueError):
            rm = RequestMenu()
            MockTransportTestCase.server_protocol.data_received(rm.__serialize__())

    def test_8_exception_sendingInValidPacket(self):
        MockTransportTestCase.client_protocol.received_message = []
        MockTransportTestCase.client_protocol.receiving_state = 0
        with self.assertRaises(TypeError):
            MockTransportTestCase.client_protocol.send_request_menu('Test')


if __name__ == '__main__':
    unittest.main()

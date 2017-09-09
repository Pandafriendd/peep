import asyncio
import unittest

from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol

from ..mypackets import Result

from .OrderingServerProtocol import OrderingServerProtocol as ServerProtocol
from .OrderingClientProtocol import OrderingClientProtocol as ClientProtocol


class MyTestCase(unittest.TestCase):

    # loop_mock = TestLoopEx()
    # transport_mock = MockTransportToProtocol()

    def test_basic_mock_transport(self):
        sp = ServerProtocol()

        result = Result()
        self.initPacket(result, [1, 10])
        cp = ClientProtocol(result, None)

        ts = MockTransportToProtocol(sp)
        tc = MockTransportToProtocol(cp)

        sp.connection_made(tc)
        cp.connection_made(ts)

        self.assertEqual(sp.received[0], result)

    @staticmethod
    def initPacket(packet, attr_list):
        for index in range(len(packet.FIELDS)):
            packet.__setattr__(packet.FIELDS[index][0], attr_list[index])


if __name__ == '__main__':
    unittest.main()

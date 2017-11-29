import unittest

from ..mypackets import RequestMenu, Menu, Order, Result, ListTest
from ..playgroundpackets import PEEPPacket
from playground.network.packet import PacketType
from playground.network.packet.encoders.PacketEncodingError import PacketEncodingError

"""
    You should NOT run the code directly by `python submission.py`.
    You should go to the top level of file dir, and use `python -m netsec_fall2017.lab_1b.submission`.
    There is a .sh script file in top level dir, you could also use `./start.sh 1b` to run the code.
"""


@unittest.skip('no reason')
class MyPacketsTestCase(unittest.TestCase):

    def test_packetOfRequestMenu(self):
        request_menu_before = RequestMenu()
        request_menu_ser = request_menu_before.__serialize__()
        request_menu_after = RequestMenu.Deserialize(request_menu_ser)
        self.assertEqual(request_menu_before, request_menu_after)

    def test_packetOfMenu(self):
        menu_before = Menu()
        self.initPacket(menu_before, [1, 'A', 'B', 'C'])
        menu_ser = menu_before.__serialize__()
        menu_after = Menu.Deserialize(menu_ser)
        self.assertEqual(menu_before, menu_after)

    def test_packetOfOrder(self):
        order_before = Order()
        self.initPacket(order_before, [1, 'B'])
        order_ser = order_before.__serialize__()
        order_after = Order.Deserialize(order_ser)
        self.assertEqual(order_before, order_after)

    def test_packetOfResult(self):
        result_before = Result()
        self.initPacket(result_before, [1, 10])
        result_ser = result_before.__serialize__()
        result_after = Result.Deserialize(result_ser)
        self.assertEqual(result_before, result_after)

    def test_negativeUINT(self):
        result = Result()
        with self.assertRaises(ValueError):
            result.ID = -1

    def test_unSetValue(self):
        result = Result()
        result.ID = 1
        with self.assertRaises(PacketEncodingError):
            result.__serialize__()

    def test_deserializer(self):
        menu = Menu()
        order = Order()
        result = Result()
        self.initPacket(menu, [2, 'A234', 'B323', 'C967'])
        self.initPacket(order, [2, 'A234'])
        self.initPacket(result, [2, 100])
        pkt_bytes = menu.__serialize__() + order.__serialize__() + result.__serialize__()
        deserializer = PacketType.Deserializer()

        i = 0
        while len(pkt_bytes) > 0:
            chunk, pkt_bytes = pkt_bytes[:8], pkt_bytes[8:]
            deserializer.update(chunk)
            for packet in deserializer.nextPackets():
                if i == 0:
                    i += 1
                    self.assertEqual(packet, menu)
                elif i == 1:
                    i += 1
                    self.assertEqual(packet, order)
                else:
                    self.assertEqual(packet, result)

    def test_listTest(self):
        lt = ListTest()
        self.initPacket(lt, [1, [1, 2, 3], 'abc'])
        lt_ser = lt.__serialize__()
        lt_deser = lt.Deserialize(lt_ser)
        self.assertEqual(list(lt.ls), list(lt_deser.ls))

    @staticmethod
    def initPacket(packet, attr_list):
        for index in range(len(packet.FIELDS)):
            packet.__setattr__(packet.FIELDS[index][0], attr_list[index])


class PEEPTestCase(unittest.TestCase):

    def test_packet(self):
        pp = PEEPPacket.Create_SYN()
        li = [2, 3, 4]
        self.assertEqual(li[pp.Type], 2)


if __name__ == '__main__':
    unittest.main()

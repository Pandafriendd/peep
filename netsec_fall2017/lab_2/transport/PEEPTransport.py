from playground.network.common import StackingTransport

from ...playgroundpackets import PEEPPacket


class PEEPTransport(StackingTransport):

    def __init__(self, lowerTransport, seq_number):
        super().__init__(lowerTransport)
        self._protocol = None
        self.__sequence_number_for_last_packet = seq_number
        self._size_for_last_packet = 1

    def write(self, data):
        packet = PEEPPacket.Create_DATA(self.__sequence_number_for_last_packet, data, self._size_for_last_packet)
        packet_bytes = packet.__serialize__()
        self.lowerTransport().write(packet_bytes)
        self.__sequence_number_for_last_packet = packet.SequenceNumber
        self._size_for_last_packet = len(packet_bytes)

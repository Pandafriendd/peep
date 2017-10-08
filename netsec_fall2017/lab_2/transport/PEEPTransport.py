from playground.network.common import StackingTransport

from ...playgroundpackets import PEEPPacket


class PEEPTransport(StackingTransport):

    def __init__(self, lowerTransport, seq_number,protocol):
        super().__init__(lowerTransport)
        self._protocol = protocol
        self.__sequence_number_for_last_packet = seq_number
        self._size_for_last_packet = 1

    def write(self, data):
        for block in self.chunk(data):
            packet = PEEPPacket.Create_DATA(self.__sequence_number_for_last_packet, block, self._size_for_last_packet)
            self._protocol.pass_packet(packet)
            self.__sequence_number_for_last_packet = packet.SequenceNumber
            self._size_for_last_packet = len(packet_bytes)

    @staticmethod
    def chunk(data):
        for i in range(0, len(data), 1024):
            yield l[i:i + 1024]
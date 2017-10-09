from playground.network.common import StackingTransport

from ...playgroundpackets import PEEPPacket


class PEEPTransport(StackingTransport):

    def __init__(self, lowerTransport, portocol):
        super().__init__(lowerTransport)
        self._protocol = portocol

    def write(self, data):
        for block in self.chunk(data):
            packet = PEEPPacket.Create_DATA(self._protocol.ret_sequencenum(), block)
            self._protocol.pass_packet(packet)

    @staticmethod
    def chunk(data):
        for i in range(0, len(data), 1024):
            yield data[i:i + 1024]
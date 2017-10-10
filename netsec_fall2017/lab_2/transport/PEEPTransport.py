from playground.network.common import StackingTransport
import asyncio
from ...playgroundpackets import PEEPPacket


class PEEPTransport(StackingTransport):

    def __init__(self, lowerTransport, portocol):
        super().__init__(lowerTransport)
        self._protocol = portocol
        self.sendpace = self.sendpace = asyncio.get_event_loop()

    def write(self, data):
        print(data)
        for block in self.chunk(data):
            packet = PEEPPacket.Create_DATA(self._protocol.ret_sequencenum(), block)
            # print(self.sendpace.time())
            self._protocol.pass_packet(packet)
            # self.sendpace.call_later(1, self._protocol.pass_packet, packet)
            # self.sendpace.run_until_complete(coro)

    @staticmethod
    def chunk(data):
        for i in range(0, len(data), 10):
            yield data[i:i + 10]
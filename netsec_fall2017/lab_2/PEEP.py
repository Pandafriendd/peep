from playground.network.common import StackingProtocol

from .PEEPTransport import PEEPTransport


class PEEP(StackingProtocol):

    def __init__(self):
        super().__init__()
        self.data = None

        # The state is to identify whether the packet type.
        self.state = -1

    def connection_made(self, transport):
        self.transport = transport
        self.higherProtocol().connection_made(PEEPTransport(self.transport))
        pass

    def data_received(self, data):
        pass

    def connection_lost(self, exc):
        pass

    def process_data(self, data):
        if self.state == 0:
            pass

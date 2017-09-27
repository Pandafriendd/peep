from playground.network.common import StackingProtocol

from .PEEPTransport import PEEPTransport


class PEEP(StackingProtocol):

    def __init__(self):
        super().__init__()
        self.data = None

        # The state is to identify whether the packet type.
        self.state = -1

    def connection_made(self, transport):
        print('--- peep connect ---')
        self.transport = transport
        self.transport.set_protocol(self)
        self.higherProtocol().connection_made(PEEPTransport(self.transport))

    def data_received(self, data):
        if self.state == -1:
            # if data == b'hello get':
                # self.transport.write(self.data)
            if data == b'hello':
                self.transport.write(b'hello get')
                self.state = 1
        elif self.state == 0:
            if data == b'hello get':
                self.state = 1
                self.transport.write(self.data)
        else:
            self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def process_data(self, data):
        if self.state == -1:
            self.data = data
            self.transport.write(b'hello')
            self.state = 0
            print(self.state)
        else:
            self.transport.write(data)

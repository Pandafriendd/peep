from playground.network.common import StackingProtocol, StackingTransport


class PassThrough2(StackingProtocol):

    def __init__(self):
        super.__init__

    def connection_made(self, transport):
        print('pt2 conn made')
        self.transport = transport
        self.higherProtocol().connection_made(StackingTransport(self.transport))

    def data_received(self, data):
        print('pt2 receive data')
        self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        print('pt2 conn lost')
        self.higherProtocol().connection_lost(exc)

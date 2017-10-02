from playground.network.common import StackingTransport


class PEEPTransport(StackingTransport):

    def __init__(self, lowerTransport):
        super().__init__(lowerTransport)

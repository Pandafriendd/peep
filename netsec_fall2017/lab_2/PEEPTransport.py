from playground.network.common import StackingTransport


class PEEPTransport(StackingTransport):

    def __init__(self, lower_transport):
        super().__init__(lower_transport)

    def write(self, data):
        self.lowerTransport().get_protocol().process_data(data)

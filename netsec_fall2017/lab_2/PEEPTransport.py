from playground.network.common import StackingTransport


class PEEPTransport(StackingTransport):

    def __init__(self, lowerTransport):
        self._protocol = None
        super().__init__(lowerTransport)

    def write(self, data):
        lt = self.lowerTransport()
        if isinstance(lt, PEEPTransport):
            lt.get_protocol().process_data(data)
        else:
            lt.write(data)

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        if self._protocol:
            return self._protocol
        else:
            return None

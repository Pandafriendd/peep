from .PLSP import PLSP
from ..factory.CertFactory import CertFactory

class PLSPServer(PLSP):

    def __init__(self):
        super(PLSPServer, self).__init__()

    def connection_made(self, transport):
        address, port = transport.get_extra_info("sockname")
        self._private_key = CertFactory.getPrivateKeyForAddr(address)
        self._certs = CertFactory.getCertsForAddr(address)
        self.transport = transport

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)
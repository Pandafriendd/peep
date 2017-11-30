from playground.network.common import StackingProtocolFactory

from ...lab_2.protocols import PEEPServer, PEEPClient, PassThroughProtocol
from  ..protocols import PLSPServer, PLSPClient

def get_lab3_server_factory():
    return StackingProtocolFactory(lambda: PEEPServer(), lambda: PLSPServer())
    # return StackingProtocolFactory(lambda: PLSPServer(), lambda: PassThroughProtocol())

def get_lab3_client_factory():
    return StackingProtocolFactory(lambda: PEEPClient(), lambda: PLSPClient())
    # return StackingProtocolFactory(lambda: PLSPClient(), lambda: PassThroughProtocol())

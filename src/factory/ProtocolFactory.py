from playground.network.common import StackingProtocolFactory
from ..protocols import PLSPClient, PLSPServer, PEEPClient, PEEPServer, PassThroughProtocol


def get_lab2_client_factory():
    return StackingProtocolFactory(lambda: PEEPClient(), lambda: PassThroughProtocol())

def get_lab2_server_factory():
    return StackingProtocolFactory(lambda: PEEPServer(), lambda: PassThroughProtocol())

def get_lab3_client_factory():
    return StackingProtocolFactory(lambda: PEEPClient(), lambda: PLSPClient())

def get_lab3_server_factory():
    return StackingProtocolFactory(lambda: PEEPServer(), lambda: PLSPServer())


import playground

from .factory.ProtocolFactory import get_lab2_client_factory, get_lab2_server_factory, get_lab3_client_factory, get_lab3_server_factory

lab2_connector = playground.Connector(protocolStack=(get_lab2_client_factory(), get_lab2_server_factory()))
lab3_connector = playground.Connector(protocolStack=(get_lab3_client_factory(), get_lab3_server_factory()))

playground.setConnector('peep', lab2_connector)
playground.setConnector('pls', lab3_connector)

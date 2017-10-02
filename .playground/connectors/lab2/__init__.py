import playground
from netsec_fall2017.lab_2.factorys import get_client_factory, get_server_factory

cf = get_client_factory()
sf = get_server_factory()
lab2_connector = playground.Connector(protocolStack=(cf, sf))

playground.setConnector('lab2_protocol', lab2_connector)


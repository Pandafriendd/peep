from playground.network.common import StackingProtocol
from playground.network.packet.PacketType import PacketType

from ...playgroundpackets import PEEPPacket, packet_deserialize
from ..transport import PEEPTransport

class PEEPServer(StackingProtocol):

    def __init__(self):
        super().__init__()
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self._sequence_number = None
        self._state = 0

    def connection_made(self, transport):
        print('---- PEEP server connected ----')
        self.transport = transport

    def data_received(self, data):
        data_packet = packet_deserialize(self._deserializer, data)
        if isinstance(data_packet, PEEPPacket):
            if self._state == 0:
                if data_packet.Type == 0:
                    print('Server received SYN')
                    self.handshake_synack(data_packet)
                    print('Server send SYN-ACK')
                else:
                    raise TypeError('Not a SYN packet')
            elif self._state == 1:
                if data_packet.Type == 2:
                    self.higher_protocol_connection_made(data_packet)
                else:
                    raise TypeError('Not a ACK packet')
            elif self._state == 2:
                data_field = data_packet.Data
                self.higherProtocol().data_received(data_field)
            else:
                raise ValueError('PEEP server wrong state')
        else:
            raise TypeError('Not a PEEP packet')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def handshake_synack(self, data_packet):
        if data_packet.verifyChecksum():
            print('PEEP server received SYN.')
            handshake_packet = PEEPPacket.Create_SYN_ACK(data_packet.SequenceNumber)
            self.transport.write(handshake_packet.__serialize__())
            print('PEEP server sent SYN-ACK')
            self._sequence_number = handshake_packet.SequenceNumber
            self._state = 1
        else:
            raise ValueError('SYN incorrect checksum.')

    def higher_protocol_connection_made(self, data_packet):
        if data_packet.verifyChecksum():
            if data_packet.Acknowledgement == self._sequence_number + 1:
                print('Server received ACK')
                self.higherProtocol().connection_made(PEEPTransport(self.transport, self._sequence_number))
                self._state = 2
            else:
                raise ValueError('Incorrect sequence number.')
        else:
            raise ValueError('ACK incorrect checksum')
import random
from playground.network.common import StackingProtocol, StackingTransport
from playground.network.packet.PacketType import PacketType

from ...playgroundpackets import PEEPPacket, packet_deserialize


class PEEPClient(StackingProtocol):

    def __init__(self):
        super().__init__()
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self._sequence_number_for_last_packet = None
        self._state = 0

    def connection_made(self, transport):
        print('---- PEEP client connected ----')
        self.transport = transport
        self.handshake_syn()

    def data_received(self, data):
        data_packet = packet_deserialize(self._deserializer, data)
        if isinstance(data_packet, PEEPPacket):
            if self._state == 1:
                if data_packet.Type == 1:
                    self.handshake_ack(data_packet)
                    self.higherProtocol().connection_made(StackingTransport(self.transport))
                else:
                    raise TypeError('Not a SYN-ACK packet.')
            elif self._state == 2:
                self.higherProtocol().data_received(data)
            else:
                raise ValueError('PEEP client wrong state.')
        else:
            raise TypeError('Not a PEEP packet.')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def handshake_syn(self):
        handshake_packet = PEEPPacket.Create_SYN()
        self.transport.write(handshake_packet.__serialize__())
        print('PEEP client sent SYN.')
        self._sequence_number_for_last_packet = handshake_packet.SequenceNumber
        self._state = 1

    def handshake_ack(self, data_packet):
        if data_packet.verifyChecksum():
            if data_packet.Acknowledgement == self._sequence_number_for_last_packet + 1:
                print('PEEP client received SYN-ACK.')
                handshake_packet = PEEPPacket.Create_ACK(data_packet.SequenceNumber, self._sequence_number_for_last_packet)
                self.transport.write(handshake_packet.__serialize__())
                print('PEEP client sent ACK')
                self._sequence_number_for_last_packet += 1
                self._state = 2
            else:
                raise ValueError('Incorrect sequence number.')
        else:
            raise ValueError('SYN-ACK incorrect checksum.')
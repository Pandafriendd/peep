import random
from playground.network.common import StackingProtocol, StackingTransport
from playground.network.packet.PacketType import PacketType

from ...playgroundpackets import PEEPPacket, packet_deserialize


class PEEPClient(StackingProtocol):

    def __init__(self):
        super().__init__()
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self._sequence_number = random.randint(1000, 9999)
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
                    print('Client received SYN-ACK.')
                    self.handshake_ack(data_packet.SequenceNumber)
                    print('Client sent ACK')
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
        handshake_packet = PEEPPacket(Type=0, SequenceNumber=self._sequence_number, Checksum=0)
        self.transport.write(handshake_packet.__serialize__())
        self._sequence_number += 1
        self._state = 1

    def handshake_ack(self, seq):
        handshake_packet = PEEPPacket(Type=2, SequenceNumber=self._sequence_number, Checksum=0, Acknowledgement=seq+1)
        self.transport.write(handshake_packet.__serialize__())
        self._sequence_number += 1
        self._state = 2

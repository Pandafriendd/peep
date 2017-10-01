import random
from playground.network.common import StackingProtocol, StackingTransport
from playground.network.packet.PacketType import PacketType

from ...playgroundpackets import PEEPPacket, packet_deserialize


class PEEPServer(StackingProtocol):

    def __init__(self):
        super().__init__()
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self._sequence_number = random.randint(1000, 9999)
        self._state = 0

    def connection_made(self, transport):
        print('---- PEEP server connected ----')
        self.transport = transport

    def data_received(self, data):
        data_packet = packet_deserialize(self._deserializer, data)
        print(data_packet)
        if isinstance(data_packet, PEEPPacket):
            if self._state == 0:
                if data_packet.Type == 0:
                    print('Server received SYN')
                    self.handshake_synack(data_packet.SequenceNumber)
                    print('Server sent SYN-ACK')
                else:
                    raise TypeError('Not a SYN packet')
            elif self._state == 1:
                if data_packet.Type == 2:
                    print('Server received ACK')
                    self.higherProtocol().connection_made(StackingTransport(self.transport))
                    self._state = 2
                else:
                    raise TypeError('Not a ACK packet')
            elif self._state == 2:
                self.higherProtocol().data_received(data)
            else:
                raise ValueError('PEEP server wrong state')
        else:
            raise TypeError('Not a PEEP packet')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def handshake_synack(self, seq):
        handshake_packet = PEEPPacket(Type=1, SequenceNumber=self._sequence_number, Checksum=0, Acknowledgement=seq+1)
        self.transport.write(handshake_packet.__serialize__())
        self._sequence_number += 1
        self._state = 1

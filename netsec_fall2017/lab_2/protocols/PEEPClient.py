# import asyncio
from playground.network.common import StackingProtocol
from playground.network.packet.PacketType import PacketType

from ...playgroundpackets import PEEPPacket, packet_deserialize
from ..transport.PEEPTransport import PEEPTransport

class PEEPClient(StackingProtocol):

    TIMEOUT_SECONDS = 5

    def __init__(self):
        super().__init__()
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        # self._timeout_handler = None
        self._sequence_number = None
        self._state = 0

    def connection_made(self, transport):
        print('---- PEEP client connected ----')
        self.transport = transport
        self.transport.protocol = self
        self.handshake_syn()

    def data_received(self, data):
        data_packet = packet_deserialize(self._deserializer, data)
        if isinstance(data_packet, PEEPPacket):
            if self._state == 1:
                if data_packet.Type == 1:
                    # self._timeout_handler.cancel()
                    self.handshake_ack(data_packet)
                    self.higherProtocol().connection_made(PEEPTransport(self.transport, self._sequence_number))
                else:
                    print('PEEP client is waiting for a SYN-ACK packet.')
            elif self._state == 2:
                # self._timeout_handler.cancel()
                data_field = data_packet.Data
                self.higherProtocol().data_received(data_field)
            else:
                raise ValueError('PEEP client wrong state.')
        else:
            print('PEEP client is waiting for a PEEP packet.')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def handshake_syn(self):
        handshake_packet = PEEPPacket.Create_SYN()
        self.transport.write(handshake_packet.__serialize__())
        print('PEEP client sent SYN.')
        self._sequence_number = handshake_packet.SequenceNumber
        self._state = 1
        # self._timeout_handler = asyncio.get_event_loop().call_later(PEEPClient.TIMEOUT_SECONDS, self.handshake_syn)

    def handshake_ack(self, data_packet):
        if data_packet.verifyChecksum():
            if data_packet.Acknowledgement == self._sequence_number + 1:
                print('PEEP client received SYN-ACK.')
                self._sequence_number += 1
                handshake_packet = PEEPPacket.Create_ACK(data_packet.SequenceNumber, self._sequence_number)
                self.transport.write(handshake_packet.__serialize__())
                print('PEEP client sent ACK')
                self._state = 2
                # self._timeout_handler = asyncio.get_event_loop().call_later(PEEPClient.TIMEOUT_SECONDS, self.handshake_ack)
            else:
                print('Incorrect sequence number.')
        else:
            print('SYN-ACK incorrect checksum.')


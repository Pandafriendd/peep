import asyncio

from ...playgroundpackets import PEEPPacket, packet_deserialize
from ..constants import TIMEOUT_SECONDS
from ..transport.PEEPTransport import PEEPTransport
from .PEEP import PEEP


class PEEPServer(PEEP):

    def __init__(self):
        super(PEEPServer, self).__init__()
        self._timeout_handler = None

    def connection_made(self, transport):
        print('---- PEEP server connected ----')
        self.transport = transport

    def data_received(self, data):
        data_packet = packet_deserialize(self._deserializer, data)
        if isinstance(data_packet, PEEPPacket):
            if self._state == 0:
                if data_packet.Type == 0:
                    self.handshake_syn_received(data_packet)
                    self._timeout_handler = asyncio.get_event_loop().call_later(TIMEOUT_SECONDS, self.forcefully_termination)
                else:
                    print('PEEP server is waiting for a SYN packet')
            elif self._state == 1:
                if data_packet.Type == 2:
                    self._timeout_handler.cancel()
                    self.handshake_ack_received(data_packet)
                else:
                    print('PEEP server is waiting for a ACK packet')
            elif self._state == 2:
                if data_packet.Type == 2:
                    self.ack_received(data_packet)
                elif data_packet.Type == 5:
                    self.data_packet_received(data_packet)
                else:
                    print('PEEP server is waiting for a ACK/DATA packet')

            else:
                raise ValueError('PEEP server wrong state')
        else:
            print('PEEP server is waiting for a PEEP packet')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def handshake_syn_received(self, data_packet):
        if data_packet.verifyChecksum():
            print('PEEP server received SYN.')
            handshake_packet = PEEPPacket.Create_SYN_ACK(data_packet.SequenceNumber)
            self.transport.write(handshake_packet.__serialize__())
            print('PEEP server sent SYN-ACK with seq num %s' % handshake_packet.SequenceNumber)
            self._seq_num_for_handshake = handshake_packet.SequenceNumber
            self._state = 1
            self._seq_num_for_next_expected_packet = handshake_packet.Acknowledgement
            print('expected next pack with seq num %s' % self._seq_num_for_next_expected_packet)
        else:
            print('SYN incorrect checksum.')

    def handshake_ack_received(self, data_packet):
        if data_packet.verifyChecksum():
            if data_packet.Acknowledgement == self._seq_num_for_handshake + 1:
                print('PEEP Server received ACK')
                self.higherProtocol().connection_made(PEEPTransport(self.transport, self))
                self._state = 2
            else:
                print('Incorrect sequence number.')
        else:
            print('ACK incorrect checksum')

    def forcefully_termination(self):
        print('Timeout session')
        self.transport.close()

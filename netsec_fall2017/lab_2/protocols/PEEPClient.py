from ...playgroundpackets import PEEPPacket, packet_deserialize
from ..transport.PEEPTransport import PEEPTransport
from .PEEP import PEEP

class PEEPClient(PEEP):

    def __init__(self):
        super(PEEPClient, self).__init__()

    def connection_made(self, transport):
        print('---- PEEP client connected ----')
        self.transport = transport
        self.handshake_init()

    def data_received(self, data):
        self._deserializer.update(data)
        for data_packet in self._deserializer.nextPackets():
            if isinstance(data_packet, PEEPPacket):
                if self._state == 1:
                    if data_packet.Type == 1:
                        self.handshake_synack_received(data_packet)
                    else:
                        print('PEEP client is waiting for a SYN-ACK packet.')
                elif self._state == 2:
                    if data_packet.Type == 2:
                        self.ack_received(data_packet)
                    elif data_packet.Type == 5:
                        self.data_packet_received(data_packet)
                    else:
                        print('PEEP client is waiting for a ACK/DATA packet')
                else:
                    raise ValueError('PEEP client wrong state.')
            else:
                print('PEEP client is waiting for a PEEP packet.')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def handshake_init(self):
        handshake_packet = PEEPPacket.Create_SYN()
        self.transport.write(handshake_packet.__serialize__())
        print('PEEP client sent SYN with seq num %s.' % handshake_packet.SequenceNumber)
        self._seq_num_for_handshake = handshake_packet.SequenceNumber
        self._state = 1

    def handshake_synack_received(self, data_packet):
        if data_packet.verifyChecksum():
            if data_packet.Acknowledgement == self._seq_num_for_handshake + 1:
                print('PEEP client received SYN-ACK.')
                handshake_packet = PEEPPacket.Create_handshake_ACK(data_packet.SequenceNumber, self._seq_num_for_handshake)
                self.transport.write(handshake_packet.__serialize__())
                print('PEEP client sent ACK')
                self._seq_num_for_next_expected_packet = handshake_packet.Acknowledgement
                self._state = 2
                print('expected next packet with seq num %s' % self._seq_num_for_next_expected_packet)
                self.higherProtocol().connection_made(PEEPTransport(self.transport, self))
            else:
                print('Incorrect sequence number.')
        else:
            print('SYN-ACK incorrect checksum.')


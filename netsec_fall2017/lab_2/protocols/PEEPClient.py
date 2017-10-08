import asyncio
import heapq
from playground.network.common import StackingProtocol
from playground.network.packet.PacketType import PacketType
from ...playgroundpackets import PEEPPacket, packet_deserialize
from ..transport.PEEPTransport import PEEPTransport


class PEEPClient(StackingProtocol):

    TIMEOUT_SECONDS = 5
    P_WINDOW = 5

    def __init__(self):
        super().__init__()
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self._timeout_handler = None
        self._sequence_number = None
        self._state = 0
        self._passed_list = []
        self._backlog_list = []
        self._data_list = []

    def connection_made(self, transport):
        print('---- PEEP client connected ----')
        self.transport = transport
        self.transport.protocol = self
        self.handshake_syn()

    def data_received(self, data):
        data_packet = packet_deserialize(self._deserializer, data)
        print("client received data")
        if isinstance(data_packet, PEEPPacket):
            if self._state == 1:
                if data_packet.Type == 1:
                    self._timeout_handler.cancel()
                    self.handshake_ack(data_packet)
                    self.higherProtocol().connection_made(PEEPTransport(self.transport, self._sequence_number, self))
                else:
                    print('PEEP client is waiting for a SYN-ACK packet.')
            elif self._state == 2:
                if data_packet.Type == 2:
                    self._timeout_handler.cancel()
                    self.ack_received(data_packet)
                elif data_packet.Type == 5:
                    self._timeout_handler.cancel()
                    self.ack_received(data_packet)
            else:
                raise ValueError('PEEP client wrong state.')
        else:
            print('PEEP client is waiting for a PEEP packet.')

    def connection_lost(self, exc):
        self.higherProtocol().connection_lost(exc)

    def resend(self, state):
        if state == self._state:
            print("should resend")
            self.handshake_syn()

    def handshake_syn(self):
        handshake_packet = PEEPPacket.Create_SYN()
        self.transport.write(handshake_packet.__serialize__())
        print('PEEP client sent SYN.')
        self._sequence_number = handshake_packet.SequenceNumber
        self._state = 1
        self._timeout_handler = asyncio.get_event_loop().call_later(PEEPClient.TIMEOUT_SECONDS, self.handshake_syn)

    def handshake_ack(self, data_packet):
        if data_packet.verifyChecksum():
            if data_packet.Acknowledgement == self._sequence_number + 1:
                print('PEEP client received SYN-ACK.')
                self._sequence_number += 1
                handshake_packet = PEEPPacket.Create_ACK(data_packet.SequenceNumber, self._sequence_number)
                self.transport.write(handshake_packet.__serialize__())
                print('PEEP client sent ACK')
                self._state = 2
                self._timeout_handler = asyncio.get_event_loop().call_later(PEEPClient.TIMEOUT_SECONDS, self.handshake_ack)
            else:
                print('Incorrect sequence number.')
        else:
            raise ValueError('SYN-ACK incorrect checksum.')

    def pass_packet(self, packet):
        if len(self._passed_list) < PEEPClient.P_WINDOW:
            heapq.heappush(self._passed_list, packet)
            self._sequence_number = packet.SequenceNumber
            packet_bytes = packet.__serialize__()
            self.transport.write(packet_bytes)
        else:
            heapq.heappush(self._backlog_list, packet)

    def send_backlog(self):
        if len(self._passed_list) < 5 and len(self._backlog_list) > 0:
            packet = heapq.heappop(self._backlog_list)
            heapq.heappush(self._passed_list, packet)
            packet_bytes = packet.__serialize__()
            self.transport.write(packet_bytes)

    def send_ack(self):

    def ack_received(self,data_packet):
        if data_packet.verifyChecksum():
            print('PEEP client received ack packet')
            seq = data_packet.Acknowledgement
            for packets in self._passed_list:
                if packets.SequenceNumber == seq:
                    while self._passed_list[0] != seq:
                        heapq.heappop(self._passed_list)
                        self.send_backlog()
                    break
        else: print("ack check sum is not valid")

    def data_reorder(self,data_packet):
        if data_packet.verifyChecksum():
            print('PEEP client received data packet')
            if data_packet.SequenceNumber



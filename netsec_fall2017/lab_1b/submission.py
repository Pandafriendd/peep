from playground.network.packet import PacketType
from mypackets.RequestMenu import RequestMenu

packet1 = RequestMenu()
packet1.counter = 1

packet2 = RequestMenu()
packet2.counter = 2

packet3 = RequestMenu()
packet3.counter = 3

pktBytes = packet1.__serialize__() + packet2.__serialize__() + packet3.__serialize__()

deserializer = PacketType.Deserializer()
while len(pktBytes) > 0:
    chunk, pktBytes = pktBytes[:10], pktBytes[10:]
    deserializer.update(chunk)
    for packet in deserializer.nextPackets():
        if packet == packet1:
            print('1')
        elif packet == packet2:
            print('2')
        elif packet == packet3:
            print('3')
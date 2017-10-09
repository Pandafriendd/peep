from .PEEPPacket import PEEPPacket


def packet_deserialize(deserializer, data):
    data_after_deserialization = None
    while len(data) > 0:
        chunk, data = data[:10], data[10:]
        deserializer.update(chunk)
        for packet in deserializer.nextPackets():
            data_after_deserialization = packet
    return data_after_deserialization

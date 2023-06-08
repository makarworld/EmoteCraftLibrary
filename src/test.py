import struct

networkingVersion = 0

def read(byte_buffer):
    version = struct.unpack('i', byte_buffer[:4])[0]
    if version > networkingVersion:
        raise Exception("Can't read newer version")
    #data.purpose = PacketTask.getTaskFromID(struct.unpack('b', byte_buffer[4:5])[0])

    count = struct.unpack('b', byte_buffer[5:6])[0]

    byte_buffer = byte_buffer[6:]
    for i in range(count):
        id = struct.unpack('b', byte_buffer[:1])[0]
        sub_version = struct.unpack('b', byte_buffer[1:2])[0]
        size = struct.unpack('i', byte_buffer[2:6])[0]
        current_pos = len(byte_buffer)
        #if id in subPackets:
            #sub_packet = subPackets[id]
        #    if not sub_packet.read(byte_buffer, data, sub_version):
        #        raise Exception("Invalid " + type(sub_packet).__name__ + " sub-packet received")
        #    if len(byte_buffer) != size + current_pos:
        #        byte_buffer = byte_buffer[current_pos + size:]
        #else:
        #    byte_buffer = byte_buffer[current_pos + size:]
            # Skip unknown sub-packets...

    #if data.prepare_and_validate():
    #    return data
    #else:
    #    return None
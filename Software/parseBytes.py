import struct


def int16(bytes: bytearray):
    return struct.unpack("<h", bytes)[0]


def float(bytes: bytearray):
    return struct.unpack("f", bytes)[0]

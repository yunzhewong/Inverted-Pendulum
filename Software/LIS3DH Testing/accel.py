import struct

class AccelerometerMeasurement():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"X: {self.x:6.2f}, Y: {self.y:6.2f}, Z: {self.z:6.2f}"
    
def parse_float(bytes: bytearray):
    return struct.unpack("f", bytes)[0]

def parse_accelerometer(data: bytearray):
    if len(data) != 12:
        return None
    
    x = parse_float(data[0:4])
    y = parse_float(data[4:8])
    z = parse_float(data[8:12])
    return AccelerometerMeasurement(x, y, z)
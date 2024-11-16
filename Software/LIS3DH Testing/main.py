import struct

from realtimeplotting.plot import RealTimePlot
from realtimeplotting.read import SerialReader
from realtimeplotting.sensordata import SensorData


def parse_float(bytes: bytearray):
    return struct.unpack("f", bytes)[0]


def parse_accelerometer(data: bytearray):
    if len(data) != 12:
        return None

    x = parse_float(data[0:4])
    y = parse_float(data[4:8])
    z = parse_float(data[8:12])
    return [x, y, z]


if __name__ == "__main__":
    latestSensorData = SensorData()

    serialReader = SerialReader(latestSensorData, parse_accelerometer)
    realTimePlot = RealTimePlot(latestSensorData, 3)

    serialReader.startReadingThread()
    realTimePlot.startFillingThread()

    try:
        realTimePlot.drawAndBlock()
    except KeyboardInterrupt:
        latestSensorData.stop = True

    serialReader.waitCompletion()
    realTimePlot.waitCompletion()

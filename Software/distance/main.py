import struct
import time

from realtimeplotting.plot import RealTimePlot
from realtimeplotting.read import SerialReader
from realtimeplotting.sensordata import SensorData


def parseInt16(bytes: bytearray):
    return struct.unpack("<h", bytes)[0]


def parse_distance(data: bytearray):
    if len(data) != 2:
        return None

    return [parseInt16(data)]


if __name__ == "__main__":
    latestSensorData = SensorData([-1])

    serialReader = SerialReader(latestSensorData, parse_distance)
    realTimePlot = RealTimePlot(latestSensorData, 1)

    try:
        readingThread = serialReader.startReadingThread()
        fillingThread = realTimePlot.startFillingThread()

        realTimePlot.drawAndBlock()
    except Exception as e:
        print(e)
        with latestSensorData.lock:
            latestSensorData.stop = True

    readingThread.join()
    fillingThread.join()

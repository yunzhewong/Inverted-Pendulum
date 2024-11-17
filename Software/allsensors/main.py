import struct

import serial

from realtimeplotting.plot import (
    RealTimePlot,
    ThreadSharedPlottingData,
    createFillingThread,
)
from realtimeplotting.read import createReadingThread
from realtimeplotting.sensordata import ThreadSharedSensorData


def parseFloat(bytes: bytearray):
    return struct.unpack("f", bytes)[0]


def parseInt16(bytes: bytearray):
    return struct.unpack("<h", bytes)[0]


def parse_all(data: bytearray):
    if len(data) != (2 + 12):
        return None

    return [
        parseInt16(data[0:2]),
        parseFloat(data[2:6]),
        parseFloat(data[6:10]),
        parseFloat(data[10:14]),
    ]


DATA_LENGTH = 4


if __name__ == "__main__":
    socket = serial.Serial("COM3", 115200)

    sensorData = ThreadSharedSensorData([-1, 0, 0, 0])
    plottingData = ThreadSharedPlottingData(DATA_LENGTH)

    readingThread = createReadingThread(socket, "UU", parse_all, sensorData)
    fillingThread = createFillingThread(sensorData, plottingData)

    realTimePlot = RealTimePlot(DATA_LENGTH)

    try:
        realTimePlot.drawAndBlock(sensorData, plottingData)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        with sensorData.lock:
            sensorData.stop = True
    readingThread.join()
    fillingThread.join()

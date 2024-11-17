import struct

import serial
import parseBytes

from realtimeplotting.plot import (
    RealTimePlot,
    ThreadSharedPlottingData,
    createFillingThread,
)
from realtimeplotting.read import createReadingThread
from realtimeplotting.sensordata import ThreadSharedSensorData


def parse_gyroscope(data: bytearray):
    if len(data) != 12:
        return None

    rollRate = parseBytes.float(data[0:4])
    pitchRate = parseBytes.float(data[4:8])
    yawRate = parseBytes.float(data[8:12])

    return [rollRate, pitchRate, yawRate]


DATA_LENGTH = 3

if __name__ == "__main__":
    socket = serial.Serial("COM3", 115200)

    sensorData = ThreadSharedSensorData([0, 0, 0])
    plottingData = ThreadSharedPlottingData(DATA_LENGTH)

    readingThread = createReadingThread(socket, "UU", parse_gyroscope, sensorData)
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

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


def parse_distance(data: bytearray):
    if len(data) != 2:
        return None

    return [parseBytes.int16(data)]


DATA_LENGTH = 1


if __name__ == "__main__":
    socket = serial.Serial("COM3", 115200)

    sensorData = ThreadSharedSensorData([-1])
    plottingData = ThreadSharedPlottingData(DATA_LENGTH)

    readingThread = createReadingThread(socket, "UU", parse_distance, sensorData)
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

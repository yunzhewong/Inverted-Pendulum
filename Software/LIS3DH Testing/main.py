import struct
import threading

import matplotlib.pyplot as plt

from realtimeplotting.plot import PeriodicDataFiller, Plot, PlottingData
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
    plottingData = PlottingData(3)

    reader = SerialReader(latestSensorData, parse_accelerometer)
    filler = PeriodicDataFiller(latestSensorData, plottingData)

    reading_thread = threading.Thread(target=reader.start)
    reading_thread.start()

    filling_thread = threading.Thread(target=filler.start)
    filling_thread.start()

    plot = Plot(3, plottingData)

    try:
        plot.start()
    except KeyboardInterrupt:
        latestSensorData.stop = True

    reading_thread.join()
    filling_thread.join()

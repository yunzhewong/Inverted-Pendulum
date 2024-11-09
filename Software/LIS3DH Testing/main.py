import threading
from data import LatestSensorData
from read import SerialReader
from plot import PeriodicDataFiller, Plot, PlottingData
import matplotlib.pyplot as plt

if __name__ == "__main__":

    latestSensorData = LatestSensorData()
    plottingData = PlottingData()

    reader = SerialReader(latestSensorData)
    filler = PeriodicDataFiller(latestSensorData, plottingData)

    reading_thread = threading.Thread(target=reader.start)
    reading_thread.start()

    filling_thread = threading.Thread(target=filler.start)
    filling_thread.start()

    plot = Plot(plottingData)

    try:
        plot.start()
    except KeyboardInterrupt:
        latestSensorData.stop = True

    reading_thread.join()
    filling_thread.join()

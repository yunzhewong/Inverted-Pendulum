import threading
import time
from typing import List
from realtimeplotting.sensordata import SensorData
import matplotlib.pyplot as plt


class PlottingData:
    def __init__(self, numberOfRows: int):
        self.lock = threading.Lock()
        self.t: List[float] = []
        self.data: List[List[float]] = [[] for _ in range(numberOfRows)]
        self.stop = False

    def add_reading(self, time: float, reading: List[float]):
        with self.lock:
            self.t.append(time)

            for index in range(len(reading)):
                self.data[index].append(reading[index])


class Plot:
    def __init__(self, numberOfRows: int, plottingData: PlottingData):
        self.fig, self.ax = plt.subplots()
        self.lines: List[plt.Line2D] = []

        for _ in range(numberOfRows):
            (line,) = self.ax.plot([], [], lw=1)
            self.lines.append(line)

        self.plottingData = plottingData

    def start(self):
        while True:
            with self.plottingData.lock:
                if self.plottingData.stop:
                    return

                t = self.plottingData.t

                for i in range(len(self.lines)):
                    self.lines[i].set_data(t, self.plottingData.data[i])

                self.ax.set_xlim(min(t), max(t))

                minY = min([min(data) for data in self.plottingData.data])
                maxY = max([max(data) for data in self.plottingData.data])
                self.ax.set_ylim(minY, maxY)

            plt.draw()
            plt.pause(1 / 30)
            time.sleep(1 / 30)


class PeriodicDataFiller:
    def __init__(self, sensorData: SensorData, plottingData: PlottingData):
        self.plottingData = plottingData
        self.latestData = sensorData

    def start(self):
        startTime = time.perf_counter()
        while True:
            with self.latestData.lock:
                if self.latestData.stop:
                    return

                if self.latestData.accelData is None:
                    continue

                with self.plottingData.lock:
                    currentTime = time.perf_counter() - startTime
                    self.plottingData.t.append(currentTime)
                    self.plottingData.x.append(self.latestData.accelData.x)
                    self.plottingData.y.append(self.latestData.accelData.y)
                    self.plottingData.z.append(self.latestData.accelData.z)

            time.sleep(1 / 50)

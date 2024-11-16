import threading
import time
from typing import List
from realtimeplotting.sensordata import SensorData
import matplotlib.pyplot as plt


DRAW_PAUSE = 1 / 50


class RealTimePlot:
    def __init__(self, sensorData: SensorData, numberOfRows: int):
        plottingData = PlottingData(numberOfRows)

        self.filler = PeriodicDataFiller(sensorData, plottingData)
        self.plot = Plot(numberOfRows, plottingData)

    def startFillingThread(self):
        filling_thread = threading.Thread(target=self.filler.start)
        filling_thread.start()
        return filling_thread

    def drawAndBlock(self):
        self.plot.drawAndBlock()


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

    def drawAndBlock(self):
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
            plt.pause(DRAW_PAUSE)
            time.sleep(DRAW_PAUSE)


class PeriodicDataFiller:
    def __init__(self, sensorData: SensorData, plottingData: PlottingData):
        self.plottingData = plottingData
        self.sensorData = sensorData

    def start(self):
        startTime = time.perf_counter()
        while True:
            with self.sensorData.lock:
                if self.sensorData.stop:
                    return

                currentTime = time.perf_counter() - startTime
                self.plottingData.add_reading(currentTime, self.sensorData.data)

            time.sleep(DRAW_PAUSE)

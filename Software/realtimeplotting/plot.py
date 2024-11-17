import threading
import time
from typing import List
from realtimeplotting.sensordata import ThreadSharedSensorData
import matplotlib.pyplot as plt


DRAW_PAUSE = 1 / 50


class ThreadSharedPlottingData:
    def __init__(self, rowCount: int):
        self.lock = threading.Lock()
        self.t: List[float] = []
        self.lineValues: List[List[float]] = [[] for _ in range(rowCount)]


def createFillingThread(
    sensorData: ThreadSharedSensorData, plottingData: ThreadSharedPlottingData
):
    filling_thread = threading.Thread(
        target=fillPlottingData,
        args=(
            sensorData,
            plottingData,
        ),
    )
    filling_thread.start()
    return filling_thread


def fillPlottingData(
    sensorData: ThreadSharedSensorData, plottingData: ThreadSharedPlottingData
):
    startTime = time.perf_counter()
    while True:
        currentTime = time.perf_counter() - startTime

        with sensorData.lock:
            if sensorData.stop:
                return

            with plottingData.lock:
                plottingData.t.append(currentTime)
                for i in range(len(plottingData.lineValues)):
                    plottingData.lineValues[i].append(sensorData.data[i])
        time.sleep(DRAW_PAUSE)


class RealTimePlot:
    def __init__(self, rowCount: int):
        self.fig, self.ax = plt.subplots()
        self.lines: List[plt.Line2D] = []
        for _ in range(rowCount):
            (line,) = self.ax.plot([], [], lw=1)
            self.lines.append(line)

    def drawAndBlock(
        self, sensorData: ThreadSharedSensorData, plottingData: ThreadSharedPlottingData
    ):
        while True:
            with sensorData.lock:
                if sensorData.stop:
                    return

            with plottingData.lock:
                t = plottingData.t

                for i in range(len(self.lines)):
                    self.lines[i].set_data(t, plottingData.lineValues[i])

                self.ax.set_xlim(min(t), max(t))

                minY = min([min(values) for values in plottingData.lineValues])
                maxY = max([max(values) for values in plottingData.lineValues])
                self.ax.set_ylim(minY, maxY)

            plt.draw()
            plt.pause(DRAW_PAUSE)
            time.sleep(DRAW_PAUSE)

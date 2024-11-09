import threading
import time
from data import LatestSensorData
from accel import AccelerometerMeasurement
import matplotlib.pyplot as plt


class PlottingData:
    def __init__(self):
        self.lock = threading.Lock()
        self.t = []
        self.x = []
        self.y = []
        self.z = []
        self.stop = False

    def add_reading(self, time: float, accelData: AccelerometerMeasurement):
        with self.lock:
            self.t.append(time)
            self.x.append(accelData.x)
            self.y.append(accelData.y)
            self.z.append(accelData.z)


class Plot:
    def __init__(self, plottingData: PlottingData):
        self.fig, self.ax = plt.subplots()

        (self.xline,) = self.ax.plot([], [], lw=1)
        (self.yline,) = self.ax.plot([], [], lw=1)
        (self.zline,) = self.ax.plot([], [], lw=1)

        self.plottingData = plottingData

    def start(self):
        while True:
            with self.plottingData.lock:
                if self.plottingData.stop:
                    return

                t = self.plottingData.t
                x = self.plottingData.x
                y = self.plottingData.y
                z = self.plottingData.z
                self.xline.set_data(t, x)
                self.yline.set_data(t, y)
                self.zline.set_data(t, z)

                self.ax.set_xlim(min(t), max(t))
                self.ax.set_ylim(
                    min(min(x), min(y), min(z)), max(max(x), max(y), max(z))
                )

            plt.draw()
            plt.pause(1 / 30)
            time.sleep(1 / 30)


class PeriodicDataFiller:
    def __init__(self, latestData: LatestSensorData, plottingData: PlottingData):
        self.plottingData = plottingData
        self.latestData = latestData

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

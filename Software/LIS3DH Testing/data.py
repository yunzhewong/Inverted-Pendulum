import threading
from accel import AccelerometerMeasurement


class LatestSensorData():
  def __init__(self):
    self.lock = threading.Lock()
    self.accelData: AccelerometerMeasurement | None = None 
    self.stop = False



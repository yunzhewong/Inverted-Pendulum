import threading
from typing import List


class SensorData:
    def __init__(self):
        self.lock = threading.Lock()
        self.data: List[float] = []
        self.stop = False

import threading
from typing import List


class SensorData:
    def __init__(self, init_data: List[float]):
        self.lock = threading.Lock()
        self.data: List[float] = init_data
        self.stop = False

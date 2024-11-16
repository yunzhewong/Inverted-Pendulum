from typing import Callable, List

import serial

from realtimeplotting.delimitedparser import DelimitedParser
from realtimeplotting.sensordata import SensorData


class SerialReader:
    def __init__(
        self, sensorData: SensorData, parse: Callable[[bytearray], None | List[float]]
    ):
        self.conn = serial.Serial("COM3", 115200)
        self.parse = parse
        self.parser = DelimitedParser("UU")
        self.sensorData = sensorData

    def start(self):
        try:
            while True:
                with self.sensorData.lock:
                    if self.sensorData.stop:
                        return

                if (
                    self.conn.in_waiting > 0
                ):  # Check if there is data waiting to be read
                    byte = self.conn.read()  # Read a single byte
                    self.parser.add_data(byte)
                    self.parser.check(self.callback)
        except KeyboardInterrupt:
            print("Exiting program.")
            self.conn.close()  # Close the serial connection

    def callback(self, data: bytearray):
        parsed_data = self.parse(data)
        if parsed_data is None:
            return

        with self.sensorData.lock:
            self.sensorData.data = parsed_data

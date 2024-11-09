from accel import parse_accelerometer
from delimitedparser import DelimitedParser
from data import LatestSensorData
import serial

class SerialReader():
    def __init__(self, latestSensorData: LatestSensorData):
        self.conn = serial.Serial('COM3', 115200)
        self.parser = DelimitedParser("UU")
        self.data = latestSensorData

    def start(self):
        try:
            while True:
                with self.data.lock:
                    if self.data.stop:
                        return

                if self.conn.in_waiting > 0:  # Check if there is data waiting to be read
                    byte = self.conn.read()  # Read a single byte
                    self.parser.add_data(byte)
                    self.parser.check(self.callback)
        except KeyboardInterrupt:
            print("Exiting program.")
            self.conn.close()  # Close the serial connection

    def callback(self, data: bytearray):
        parsed_data = parse_accelerometer(data)
        if parsed_data is None:
            return

        with self.data.lock:
            self.data.accelData = parse_accelerometer(data)


 








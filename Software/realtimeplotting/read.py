import threading
from typing import Callable, List

import serial

from realtimeplotting.DelimitedSectioner import DelimitedSectioner
from realtimeplotting.sensordata import ThreadSharedSensorData


def createReadingThread(
    socket: serial.Serial,
    delimiter: str,
    parse: Callable[[bytearray], None | List[float]],
    sensorData: ThreadSharedSensorData,
):
    reader = SerialReader(socket, delimiter, parse)
    reading_thread = threading.Thread(target=reader.readFromSocket, args=(sensorData,))
    reading_thread.start()
    return reading_thread


class SerialReader:
    def __init__(
        self,
        socket: serial.Serial,
        delimiter: str,
        parse: Callable[[bytearray], None | List[float]],
    ):
        self.socket = socket
        self.delimitedSectioner = DelimitedSectioner(delimiter)
        self.parse = parse

    def readFromSocket(self, sensorData: ThreadSharedSensorData):
        while True:
            with sensorData.lock:
                if sensorData.stop:
                    self.socket.close()  # Close the serial connection
                    return

            if self.socket.in_waiting == 0:
                continue

            byte = self.socket.read()  # Read a single byte
            parsedData = self.handleData(byte)

            if parsedData is None:
                continue

            with sensorData.lock:
                sensorData.data = parsedData

    def handleData(self, data: bytearray):
        self.delimitedSectioner.addData(data)
        sections = self.delimitedSectioner.collapseSections()

        if len(sections) == 0:
            return None

        lastSection = sections[-1]

        parsedData = self.parse(lastSection)
        if parsedData is None:
            return None

        return parsedData

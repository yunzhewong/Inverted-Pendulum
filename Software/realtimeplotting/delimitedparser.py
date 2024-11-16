from typing import Callable
import unittest


class DelimitedParser:
    def __init__(self, delimiter: str):
        self.delimiter_bytes = bytearray(delimiter.encode("utf-8"))
        self.data = bytearray([])

    def add_data(self, data: bytes):
        self.data += bytearray(data)

    def check(self, on_data: Callable[[bytearray], None]):
        indexes = []
        for i in range(len(self.data)):
            if self.data[i : i + len(self.delimiter_bytes)] == self.delimiter_bytes:
                indexes.append(i)

        if len(indexes) == 0 or len(indexes) == 1:
            return

        for i in range(len(indexes) - 1):
            section = self.data[indexes[i] + len(self.delimiter_bytes) : indexes[i + 1]]
            on_data(section)

        self.data = self.data[indexes[-1] :]


class TestDelimitedParser(unittest.TestCase):
    def test_single(self):
        parser = DelimitedParser("UU")

        output = []

        def callback(data):
            output.append(1)

        parser.add_data("UUA".encode("utf-8"))
        parser.add_data("UUB".encode("utf-8"))
        parser.check(callback)

        self.assertEqual(len(output), 1)

    def test_odd_spacing(self):
        parser = DelimitedParser("UU")

        output = []

        def callback(data):
            if data == bytearray("C".encode("utf-8")):
                output.append(1)

        parser.add_data("UUC".encode("utf-8"))
        parser.add_data("UU".encode("utf-8"))
        parser.check(callback)

        self.assertEqual(len(output), 1)

    def test_even_spacing(self):
        parser = DelimitedParser("UU")

        output = []

        def callback(data):
            if data == bytearray("ABCD".encode("utf-8")):
                output.append(1)

        parser.add_data("UUABCD".encode("utf-8"))
        parser.add_data("UU".encode("utf-8"))
        parser.check(callback)

        self.assertEqual(len(output), 1)


if __name__ == "__main__":
    unittest.main()

from typing import Callable, List
import unittest


class DelimitedSectioner:
    def __init__(self, delimiter: str):
        self.delimiter_bytes = bytearray(delimiter.encode("utf-8"))
        self.data = bytearray([])

    def addData(self, data: bytes):
        self.data += bytearray(data)

    def collapseSections(self):
        indexes = []
        for i in range(len(self.data)):
            if self.data[i : i + len(self.delimiter_bytes)] == self.delimiter_bytes:
                indexes.append(i)

        if len(indexes) == 0 or len(indexes) == 1:
            return []

        sections = []
        for i in range(len(indexes) - 1):
            sections.append(
                self.data[indexes[i] + len(self.delimiter_bytes) : indexes[i + 1]]
            )
        self.data = self.data[indexes[-1] :]
        return sections


class TestDelimitedSectioner(unittest.TestCase):
    def test_single(self):
        parser = DelimitedSectioner("UU")

        output = []

        def callback(data):
            output.append(1)

        parser.collapseSections("UUA".encode("utf-8"))
        parser.collapseSections("UUB".encode("utf-8"))
        parser.check(callback)

        self.assertEqual(len(output), 1)

    def test_odd_spacing(self):
        parser = DelimitedSectioner("UU")

        output = []

        def callback(data):
            if data == bytearray("C".encode("utf-8")):
                output.append(1)

        parser.collapseSections("UUC".encode("utf-8"))
        parser.collapseSections("UU".encode("utf-8"))
        parser.check(callback)

        self.assertEqual(len(output), 1)

    def test_even_spacing(self):
        parser = DelimitedSectioner("UU")

        output = []

        def callback(data):
            if data == bytearray("ABCD".encode("utf-8")):
                output.append(1)

        parser.collapseSections("UUABCD".encode("utf-8"))
        parser.collapseSections("UU".encode("utf-8"))
        parser.check(callback)

        self.assertEqual(len(output), 1)


if __name__ == "__main__":
    unittest.main()

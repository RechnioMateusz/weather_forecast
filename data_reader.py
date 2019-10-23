import os
import sys
import time
import logging
from copy import deepcopy

from factories import ReaderFactory


class Reader:
    def __init__(self):
        self._log = logging.getLogger("reader")
        self._log.info("Initializing reader...")

        self.reader_factory = ReaderFactory()
        self.readers = None
        self.data = dict()

        self._log.info("Reader initialized")

    def get_readers(self):
        self.readers = self.reader_factory.get_all_readers()
        self._log.info("Got readers")

    def initialize_readers(self):
        for reader in self.readers:
            reader.initialize()

        self._log.info("Initialized readers")

    def get_data(self, repetitions=10, delay=.3):
        for reader in self.readers:
            for _ in range(repetitions):
                reader.read_data()
                time.sleep(delay)

            self.data.update(reader.get_data())

        self._log.info(f"Got data: {self.data}")

        return deepcopy(self.data)


if __name__ == "__main__":
    reader = Reader()
    reader.get_readers()
    reader.initialize_readers()
    print(reader.get_data())

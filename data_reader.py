"""Module containing 'Reader' class used to read data from all periferal
devices and store them in dictionary.
"""

import time
import logging
from copy import deepcopy

from factories import ReaderFactory
from resources.errors import ReaderException


class Reader:
    """Class used to initialize and read from periferal devices.

    **Attributes**
        :reader_factory: Devices readers factory. [factories.ReaderFactory]
        :readers: List of devices readers. [list]
        :data: Dictionary of read values. [dict]
    """

    def __init__(self):
        """Constructor for 'Reader' class."""

        self._log = logging.getLogger("reader")
        self._log.info("Initializing reader...")

        self.reader_factory = ReaderFactory()
        self.readers = list()
        self.data = dict()

        self._log.info("Reader initialized")

    def get_readers(self):
        """Gets all readers objects."""

        self.readers = self.reader_factory.get_all_readers()
        self._log.info("Got readers")

    def initialize_readers(self):
        """Initializes readers objects."""

        for reader in self.readers:
            reader.initialize()

        self._log.info("Initialized readers")

    def get_data(self, repetitions=10, delay=.3):
        """Starts reading data process.

        **Kwargs**
            :repetitions: How many times measurements should be done before
            calculating their average. [int]
            :delay: Delay before repetitions. [float]
        """

        if not isinstance(repetitions, int):
            raise ReaderException(
                msg="Repetitions are not int",
                desc=f"They are {type(repetitions)}"
            )

        if not isinstance(delay, (float, int)):
            raise ReaderException(
                msg="Delay is not int nor float",
                desc=f"They are {type(delay)}"
            )

        for reader in self.readers:
            for _ in range(repetitions):
                reader.read_data()
                time.sleep(delay)

            self.data.update(reader.get_data())

        self._log.info(f"Got data: {self.data}")

        return deepcopy(self.data)

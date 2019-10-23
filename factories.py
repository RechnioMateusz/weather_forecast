import logging

from adapters import BME280Adapter, TSL2561Adapter, YL83Adapter
from resources.errors import FactoryException


class ReaderFactory:
    __FACTORIES = 0

    def __init__(self):
        self._log = logging.getLogger("reader_factory")
        self._log.info("Reader factory initialization...")

        if self.__FACTORIES > 0:
            raise FactoryException(msg="Only 1 factory can be initialized.")
        else:
            self.__FACTORIES += 1

        self._readers = {
            "BME280": BME280Adapter,
            "TSL2561": TSL2561Adapter,
            "YL83": YL83Adapter,
        }

        self._log.info("Reader factory initialized")

    def get_reader(self, reader_name):
        if reader_name in self._readers:
            reader = self._readers.get(reader_name)
            return reader()

        raise FactoryException(
            msg="Invalid reader", desc=f"Reader {reader_name} does not exist"
        )

    def get_all_readers(self):
        return [reader() for _, reader in self._readers.items()]

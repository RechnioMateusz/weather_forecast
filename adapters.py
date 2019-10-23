import logging
from abc import ABC, abstractmethod

from hardware import BME280, TSL2561, YL83
from resources.errors import AdapterException
from resources.utils import average


class AbstractAdapter(ABC):
    def __init__(self):
        self.data_buffer = dict()

    @abstractmethod
    def initialize(self, *args, **kwargs):
        ...

    @abstractmethod
    def read_data(self, *args, **kwargs):
        ...

    def get_data(self):
        ret = dict().fromkeys(self.data_buffer)
        for key, value in self.data_buffer.items():
            ret.update({key: average(list_=value)})

        return ret


class BME280Adapter(AbstractAdapter):
    def __init__(self):
        self._log = logging.getLogger("BME280_adapter")
        self._log.info("Initializing BME280Adapter...")

        super().__init__()
        self.bme280 = None
        self.data_buffer.update(
            temperature=list(), pressure=list(), humidity=list()
        )

        self._log.info("BME280Adapter initialized...")

    def initialize(self, *args, **kwargs):
        self._log.info("Started initialization...")

        if not args and not kwargs:
            self.bme280 = BME280()
        elif len(args) == 1 and not kwargs:
            self.bme280 = BME280(*args)
        elif not args and len(kwargs) == 1 and "i2c_id" in kwargs:
            self.bme280 = BME280(**kwargs)
        else:
            raise AdapterException(
                msg="Invalid arguments.",
                desc=f"Passed arguments: {args}\t{kwargs}"
            )

        self._log.info("Initialization successfull")

    def read_data(self, *args, **kwargs):
        temperature = self.bme280.read_temperature()
        pressure = self.bme280.read_pressure()
        humidity = self.bme280.read_humidity()

        self._log.debug(f"Temperature: {temperature}")
        self._log.debug(f"Pressure: {pressure}")
        self._log.debug(f"Humidity: {humidity}")

        self.data_buffer.get("temperature").append(temperature)
        self.data_buffer.get("pressure").append(pressure)
        self.data_buffer.get("humidity").append(humidity)


class TSL2561Adapter(AbstractAdapter):
    def __init__(self):
        self._log = logging.getLogger("TSL2561_adapter")
        self._log.info("Initializing TSL2561Adapter...")

        super().__init__()
        self.tsl2561 = None
        self.data_buffer.update(light_intensity=list())

        self._log.info("TSL2561Adapter initialized...")

    def initialize(self, *args, **kwargs):
        self._log.info("Started initialization...")

        if not args and not kwargs:
            self.tsl2561 = TSL2561()
        elif len(args) == 1 and not kwargs:
            self.tsl2561 = TSL2561(*args)
        elif not args and len(kwargs) == 1 and "i2c_id" in kwargs:
            self.tsl2561 = TSL2561(**kwargs)
        else:
            raise AdapterException(
                msg="Invalid arguments.",
                desc=f"Passed arguments: {args}\t{kwargs}"
            )

        self._log.info("Initialization successfull")

    def read_data(self, *args, **kwargs):
        light_intensity = self.tsl2561.read_full_spectrum()

        self._log.debug(f"Light intensity: {light_intensity}")

        self.data_buffer.get("light_intensity").append(light_intensity)


class YL83Adapter(AbstractAdapter):
    def __init__(self):
        self._log = logging.getLogger("YL83_adapter")
        self._log.info("Initializing YL83Adapter...")

        super().__init__()
        self.yl83 = None
        self.data_buffer.update(precipitation=list())

        self._log.info("YL83Adapter initialized...")

    def initialize(self, *args, **kwargs):
        self._log.info("Started initialization...")

        if not args and not kwargs:
            self.yl83 = YL83()
        elif len(args) == 1 and not kwargs:
            self.yl83 = YL83(*args)
        elif not args and len(kwargs) == 1 and "i2c_id" in kwargs:
            self.yl83 = YL83(**kwargs)
        else:
            raise AdapterException(
                msg="Invalid arguments.",
                desc=f"Passed arguments: {args}\t{kwargs}"
            )

        self._log.info("Initialization successfull")

    def read_data(self, *args, **kwargs):
        precipitation = self.yl83.read_precipitation()

        self._log.debug(f"Precipitation: {precipitation}")

        self.data_buffer.get("precipitation").append(int(precipitation))

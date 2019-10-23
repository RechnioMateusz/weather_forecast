# !/usr/bin/env python
"""Module used to read data from BME280 board about temperature, pressure and
humidity. Requires RPi.bme280 `library
<https://pypi.org/project/RPi.bme280/>`_.
"""

import logging
from copy import deepcopy

import smbus2
import bme280 as bme280_lib


class BME280Exception(Exception):
    """Exception used only for bme2561_handler.py module.

    **Attributes**
        :msg: Exception message. [str]
        :desc: Exception description. [str]
    """

    def __init__(self, msg, desc=None):
        """Constructor for 'BME280Exception' exception.

        **Args**
            :msg: Exception message. [str]
        **Kwargs**
            :desc: Exception description. [str]
        """

        super().__init__(msg)
        self.msg = msg
        self.desc = desc

    def __str__(self):
        return f"Message: {self.msg}\nDescription: {self.desc}"


class BME280:
    """Class managing communication with BME280 board.

    **Attributes**
        :ADDRESS: Address of TS2561 board. [hex]
    """

    ADDRESS = 0x77

    def __init__(self, i2c_id=1):
        """Constructor for 'BME280' class.

        **Kwargs**
            :i2c_id: ID of I2C interface. [int]
        """

        if not isinstance(i2c_id, int) or i2c_id not in (0, 1):
            raise BME280Exception(
                msg="I2C ID is not int or is invalid",
                desc=f"I2C ID is {i2c_id} of type {type(i2c_id)}"
            )

        self._log = logging.getLogger("BME280")
        self._log.info("Initializing BME280 Board handler...")

        self._bus = smbus2.SMBus(i2c_id)
        self._calibration_params = bme280_lib.load_calibration_params(
            self._bus, self.ADDRESS
        )
        self._log.info("BME280 Board handler initialized")

    @property
    def calibration_params(self):
        """Getter for calibration parameters.

        **Returns**
            Deep copy of calibration parameters.
        """

        ret = deepcopy(self._calibration_params)
        self._log.debug(f"Got calibration parameters {ret}")
        return ret

    @property
    def data(self):
        """Getter for data.

        **Returns**
        """

        ret = bme280_lib.sample(
            self._bus, self.ADDRESS, self._calibration_params
        )
        self._log.debug(f"Got data {ret}")
        return ret

    def reload_calibration_params(self):
        """Reloads calibration parameters."""

        self._log.debug("Reloading calibration parameters...")
        self._calibration_params = bme280_lib.load_calibration_params(
            self._bus, self.ADDRESS
        )
        self._log.debug("Calibration parameters reloaded")

    def read_temperature(self):
        """Reads temperature.

        **Returns**
            Temperature in Celsius.
        """

        self._log.debug("Reading temperature...")
        return self.data.temperature

    def read_pressure(self):
        """Reads pressure.

        **Returns**
            Pressure in hecto Pascals.
        """

        self._log.debug("Reading pressure...")
        return self.data.pressure

    def read_humidity(self):
        """Reads humidity

        **Returns**
            Humidity in percents
        """

        self._log.debug("Reading humidity...")
        return self.data.humidity


if __name__ == "__main__":
    import time

    bme280 = BME280()
    while True:
        time.sleep(.5)
        temperature = bme280.read_temperature()
        pressure = bme280.read_pressure()
        humidity = bme280.read_humidity()
        print(f"Temperature C: {temperature}")
        print(f"Pressure hP: {pressure}")
        print(f"Humidity %rH: {humidity}\n")

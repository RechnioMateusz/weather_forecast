# !/usr/bin/env python
"""Module used to read data from YL83 board about precipitation."""

import logging
import RPi.GPIO as GPIO


class YL83Exception(Exception):
    """Exception used only for yl83_handler.py module.

    **Attributes**
        :msg: Exception message. [str]
        :desc: Exception description. [str]
    """

    def __init__(self, msg, desc=None):
        """Constructor for 'YL83Exception' exception.

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


class YL83:
    """Class managing communication with YL83 board.

    **Attributes**
        :DATA_IN_PIN: Address of data in pin. [int]
    """

    DATA_IN_PIN = 37

    def __init__(self):
        """Constructor for 'YL83' class"""

        self._log = logging.getLogger("YL83")
        self._log.info("Initializing YL83 Board handler...")

        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.DATA_IN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self._log.info("YL83 Board handler initialized")

    def read_precipitation(self):
        """Reads precipitation.

        **Returns**
            Boolean determining if rain is falling or not.
        """

        ret = not bool(GPIO.input(self.DATA_IN_PIN))
        self._log.debug(f"Precipitation: {ret}")
        return ret


if __name__ == "__main__":
    import time

    yl83 = YL83()
    while True:
        time.sleep(.5)
        print(f"Rain is falling down: {yl83.read_precipitation()}")

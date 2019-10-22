# !/usr/bin/env python
"""Module used to read data from YL83 board about precipitation."""

import RPi.GPIO as GPIO


class YL83:
    """Class managing communication with YL83 board.

    **Attributes**
        :DATA_IN_PIN: Address of data in pin. [int]
    """

    DATA_IN_PIN = 37

    def __init__(self):
        """Constructor for 'YL83' class"""

        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.DATA_IN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_precipitation(self):
        """Reads precipitation.

        **Returns**
            Boolean determining if rain is falling or not.
        """

        return not bool(GPIO.input(self.DATA_IN_PIN))


if __name__ == "__main__":
    import time

    yl83 = YL83()
    while True:
        time.sleep(.5)
        print(f"Rain is falling down: {yl83.read_precipitation()}")

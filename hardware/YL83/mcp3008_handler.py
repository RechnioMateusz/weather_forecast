# !/usr/bin/env python
"""Module used to read data from MCP3008 A/C converter."""

import spidev


class MCP3008Exception(Exception):
    """Exception used only for mcp3008_handler.py module.

    **Attributes**
        :msg: Exception message. [str]
        :desc: Exception description. [str]
    """

    def __init__(self, msg, desc=None):
        """Constructor for 'MCP3008Exception' exception.

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


class MCP3008:
    """Class managing communication with MCP3008 A/C converter.

    To use it properly::

        mcp3008 = MCP3008()
        mcp3008.set_spi_speed(speed=400_000)
        mcp3008.reference_voltage = 5000
        voltage = mcp3008.read_channel(channel=0)

    **Attributes**
        :START_BIT: Start bit of read command. [hex]
        :SINGLE_ENDED: Single ended bit with channel. [hex]
        :RESOLUTION: Resolution of A/C converter. [int]
    """

    START_BIT = 0x01
    SINGLE_ENDED = 0x08
    RESOLUTION = 1024

    def __init__(self, spi_ids=(0, 0)):
        """Constructor for 'MCP3008' class.

        **Kwargs**
            :spi_ids: IDs of SPI interface. [tuple/list]
        """

        if not isinstance(spi_ids, (tuple, list)):
            raise MCP3008Exception(
                msg="SPI IDs is not tuple nor list",
                desc=f"It's {type(spi_ids)}"
            )

        if spi_ids not in [(0, 0), (0, 1), (1, 1)]:
            raise MCP3008Exception(
                msg="Invalid SPI IDs",
                desc=f"SPI IDs is {spi_ids}"
            )

        self._reference_voltage = None
        self._spi = spidev.SpiDev()
        self._spi.open(*spi_ids)

    @property
    def reference_voltage(self):
        """Getter for reference voltage.

        **Returns**
            Reference voltage value.
        """

        return self._reference_voltage

    @reference_voltage.setter
    def reference_voltage(self, value):
        """Reference voltage setter."""

        if not isinstance(value, (int, float)):
            raise MCP3008Exception(
                msg="Reference voltage is not integer nor float",
                desc=f"It is {type(value)}"
            )

        self._reference_voltage = value

    def set_spi_speed(self, speed):
        """Sets SPI interface speed. For info about what speed to set look to
        MCP3008 `documentation
        <https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf>`_.

        **Args**
            :speed: SPI speed. [int]
        """

        if not isinstance(speed, int):
            raise MCP3008Exception(
                msg="SPI speed is not integer",
                desc=f"SPI speed is {type(speed)}"
            )

        self._spi.max_speed_hz = speed

    def read_channel(self, channel):
        """Reads voltage from specified channel.

        **Args**
            :channel: Channel to read from. [int]

        **Returns**
            Measured voltage.
        """

        if not 0 <= channel <= 7:
            raise MCP3008Exception(
                msg="Invalid channel. Should be between 0 and 7",
                desc=f"Channel is {channel}"
            )

        read_command = [self.START_BIT, self.SINGLE_ENDED | (channel << 4), 0]
        byte_result = self._spi.xfer2(read_command)
        raw_result = ((byte_result[1] & 0x03) << 8) | byte_result[2]
        return (raw_result / self.RESOLUTION) * self._reference_voltage


if __name__ == '__main__':
    import time

    mcp3008 = MCP32008()
    mcp3008.set_spi_speed(speed=400_000)
    mcp3008.reference_voltage = 5000
    while True:
        time.sleep(.5)
        for i in range(8):
            print(f"{mcp3008.read_channel(channel=i):.2f}", end="\t")
        print()

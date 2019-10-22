# !/usr/bin/env python
"""Module used to read data from BME280 board about light intensity."""

import smbus
import time


class TSL2561Exception(Exception):
    """Exception used only for tsl2561_handler.py module.

    **Attributes**
        :msg: Exception message. [str]
        :desc: Exception description. [str]
    """

    def __init__(self, msg, desc=None):
        """Constructor for 'TSL2561Exception' exception.

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


class TSL2561:
    """Class managing communication with TSL2561 board.
    Written based on this `file
    <https://github.com/ControlEverythingCommunity/TSL2561/blob/master/Python/TSL2561.py>`_
    from Github.

    **Attributes**
        :ADDRESS: Address of TS2561 board. [hex]
        :CHANNELS: Channel addresses. [dict]
        :CH_1: Second channel address. [hex]
        :CONTROL_REGISTER: Control register. [hex]
        :TIMING_REGISTER: Timing register. [hex]
        :COMMAND_REGISTER: Command register. [hex]
        :POWER_ON_MODE: Power on mode hex. [hex]
        :INTEGRATION: Integration hex. [hex]
    """

    ADDRESS = 0x29
    CHANNELS = {
        0: 0x0C,
        1: 0x0E,
    }
    CONTROL_REGISTER = 0x00
    TIMING_REGISTER = 0x01
    COMMAND_REGISTER = 0x80
    POWER_ON_MODE = 0x03
    INTEGRATION = 0x02

    def __init__(self, i2c_id=1):
        """Constructor for 'TSL2561' class.

        **Kwargs**
            :i2c_id: ID of I2C interface. [int]
        """

        if not isinstance(i2c_id, int) or i2c_id not in (0, 1):
            raise TSL2561Exception(
                msg="I2C ID is not int or is invalid",
                desc=f"I2C ID is {i2c_id} of type {type(i2c_id)}"
            )

        self._bus = smbus.SMBus(i2c_id)
        self._bus.write_byte_data(
            self.ADDRESS,
            self.CONTROL_REGISTER | self.COMMAND_REGISTER,
            self.POWER_ON_MODE
        )
        self._bus.write_byte_data(
            self.ADDRESS,
            self.TIMING_REGISTER | self.COMMAND_REGISTER,
            self.INTEGRATION
        )
        time.sleep(.5)

    def get_channel(self, channel_id):
        """Gets channel of current ID.

        **Args**
            :channel_id: ID of channel to get. [int]

        **Return**
            Hex value of channel ID.
        """

        if channel_id in self.CHANNELS:
            return self.CHANNELS.get(channel_id)

        raise TSL2561Exception(
            msg="Wrong channel ID", desc=f"{channel_id} doesn't exist"
        )

    def read_channel(self, channel):
        """Reads value from specified channel, converts it and returns
        it.

        **Args**
            :channel: ID of channel to read. [int]

        **Returns**
            Converted value readed from specified channel.
        """

        if not isinstance(channel, int):
            raise TSL2561Exception(
                msg="I2C ID is not int", desc=f"It's {type(channel_id)}"
            )

        channel_hex = self.get_channel(channel_id=channel)
        data = self._bus.read_i2c_block_data(
            self.ADDRESS,
            channel_hex | self.COMMAND_REGISTER,
            2
        )
        return data[1] * 256 + data[0]

    def read_full_spectrum(self):
        """Reads full light spectrum.

        **Returns**
            Full light spectrum value.
        """

        return self.read_channel(channel=0)

    def read_infrared_light(self):
        """Reads infrared light.

        **Returns**
            Infrared light value.
        """

        return self.read_channel(channel=1)

    def read_visible_light(self):
        """Reads visible light.

        **Returns**
            Visible light value.
        """

        return self.read_channel(channel=0) - self.read_channel(channel=1)


if __name__ == "__main__":
    tsl2561 = TSL2561()
    while True:
        time.sleep(.5)
        ch0 = tsl2561.read_channel(channel=0)
        ch1 = tsl2561.read_channel(channel=1)
        print(f"Full Spectrum(IR + Visible) :{ch0} lux")
        print(f"Infrared Value :{ch1} lux")
        print(f"Visible Value :{ch0 - ch1} lux\n")

"""Experimental FRAM Breakout Code.

Needs the basic built-in MicroPython.
"""
# pylint: disable=import-error, duplicate-code

from machine import I2C, Pin


class FRAM:
    """Driver for the FRAM breakout.
    """

    def __init__(self, i2c, address: int = 0x50):
        """Create an instance for a devices at a given address.
        We can have eight devices, from 0x50 - 0x57.
        """
        assert i2c
        assert address
        assert address >= 0x50
        assert address <= 0x57

        self._i2c = i2c
        self._address = address

    def write_byte(self, offset, byte_value) -> bool:
        """Writes a single value (expected to be a byte).
        For now it's assumed to be a +ve value (including zero), i.e. 0-127
        """
        # Max offset is 32K
        assert offset >= 0
        assert offset < 32_768
        assert byte_value >= 0
        assert byte_value < 128

        num_acks = self._i2c.writeto(self._address,
                                     bytes([offset >> 8, offset & 0xff, byte_value]))
        if num_acks != 3:
            print(f'Failed to write to FRAM at {self._address}.' +
                  f' Got {num_acks} acks, expected 3')

        return num_acks != 3
        
    def read_byte(self, offset) -> int:
        """Reads a single byte, assumed to be in the range 0-127,
        returning it as an int.
        """
        assert offset >= 0
        assert offset < 32_768

        num_acks = self._i2c.writeto(self._address,
                                     bytes([offset >> 8, offset & 0xff]))
        assert num_acks == 2
        got = self._i2c.readfrom(self._address, 1)
        assert got

        return int.from_bytes(got, 'big')


if __name__ == '__main__':

    # Configured I2C Pins
    _SCL: int = 17
    _SDA: int = 16

    # A MicroPython i2c object (for special/unsupported devices)
    _I2C: I2C = I2C(id=0, scl=Pin(_SCL), sda=Pin(_SDA))

    fram = FRAM(_I2C)
    fram.write_byte(0, 1)
    int_value = fram.read_byte(0)
    print(f'Got {int_value} from FRAM')

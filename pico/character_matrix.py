"""Experimental LTP305 dual 5x7 LED matrix code.

Here we expect MicroPython (on a Pico).
"""
# pylint: disable=import-error, duplicate-code

# The Pico/MicroPython may not have the typing module
try:
    from typing import List, Optional
except ImportError:
    pass

from machine import I2C, Pin  # type: ignore

# Configured I2C Pins
_SCL: int = 17
_SDA: int = 16

# A MicroPython i2c object (for special/unsupported devices)
_I2C: I2C = I2C(id=0, scl=Pin(_SCL), sda=Pin(_SDA))


class LTP305:
    """A simple class to control a LTP305 in MicroPython on a Pico. Based on
    Pimoroni's Raspberry Pi code at https://github.com/pimoroni/ltp305-python.
    Instead of using the Pi i2c library (which we can't use on the Pico)
    we use the MicroPython i2c library.

    The displays can use i2c address 0x61-0x63.
    """

    # LTP305 bitmaps for the basic 'ASCII' character set.
    font = {
        32: [0x00, 0x00, 0x00, 0x00, 0x00],  # (space)
        33: [0x00, 0x00, 0x5f, 0x00, 0x00],  # !
        34: [0x00, 0x07, 0x00, 0x07, 0x00],  # "
        35: [0x14, 0x7f, 0x14, 0x7f, 0x14],  # #
        36: [0x24, 0x2a, 0x7f, 0x2a, 0x12],  # $
        37: [0x23, 0x13, 0x08, 0x64, 0x62],  # %
        38: [0x36, 0x49, 0x55, 0x22, 0x50],  # &
        39: [0x00, 0x05, 0x03, 0x00, 0x00],  # '
        40: [0x00, 0x1c, 0x22, 0x41, 0x00],  # (
        41: [0x00, 0x41, 0x22, 0x1c, 0x00],  # )
        42: [0x08, 0x2a, 0x1c, 0x2a, 0x08],  # *
        43: [0x08, 0x08, 0x3e, 0x08, 0x08],  # +
        44: [0x00, 0x50, 0x30, 0x00, 0x00],  # ,
        45: [0x08, 0x08, 0x08, 0x08, 0x08],  # -
        46: [0x00, 0x60, 0x60, 0x00, 0x00],  # .
        47: [0x20, 0x10, 0x08, 0x04, 0x02],  # /
#        48: [0x3e, 0x51, 0x49, 0x45, 0x3e],  # 0
        48: [0x3e, 0x41, 0x41, 0x41, 0x3e],  # O
        49: [0x00, 0x42, 0x7f, 0x40, 0x00],  # 1
        50: [0x42, 0x61, 0x51, 0x49, 0x46],  # 2
        51: [0x21, 0x41, 0x45, 0x4b, 0x31],  # 3
        52: [0x18, 0x14, 0x12, 0x7f, 0x10],  # 4
        53: [0x27, 0x45, 0x45, 0x45, 0x39],  # 5
        54: [0x3c, 0x4a, 0x49, 0x49, 0x30],  # 6
        55: [0x01, 0x71, 0x09, 0x05, 0x03],  # 7
        56: [0x36, 0x49, 0x49, 0x49, 0x36],  # 8
        57: [0x06, 0x49, 0x49, 0x29, 0x1e],  # 9
        58: [0x00, 0x36, 0x36, 0x00, 0x00],  # :
        59: [0x00, 0x56, 0x36, 0x00, 0x00],  # ;
        60: [0x00, 0x08, 0x14, 0x22, 0x41],  # <
        61: [0x14, 0x14, 0x14, 0x14, 0x14],  # =
        62: [0x41, 0x22, 0x14, 0x08, 0x00],  # >
        63: [0x02, 0x01, 0x51, 0x09, 0x06],  # ?
        64: [0x32, 0x49, 0x79, 0x41, 0x3e],  # @
        65: [0x7e, 0x11, 0x11, 0x11, 0x7e],  # A
        66: [0x7f, 0x49, 0x49, 0x49, 0x36],  # B
        67: [0x3e, 0x41, 0x41, 0x41, 0x22],  # C
        68: [0x7f, 0x41, 0x41, 0x22, 0x1c],  # D
        69: [0x7f, 0x49, 0x49, 0x49, 0x41],  # E
        70: [0x7f, 0x09, 0x09, 0x01, 0x01],  # F
        71: [0x3e, 0x41, 0x41, 0x51, 0x32],  # G
        72: [0x7f, 0x08, 0x08, 0x08, 0x7f],  # H
        73: [0x00, 0x41, 0x7f, 0x41, 0x00],  # I
        74: [0x20, 0x40, 0x41, 0x3f, 0x01],  # J
        75: [0x7f, 0x08, 0x14, 0x22, 0x41],  # K
        76: [0x7f, 0x40, 0x40, 0x40, 0x40],  # L
        77: [0x7f, 0x02, 0x04, 0x02, 0x7f],  # M
        78: [0x7f, 0x04, 0x08, 0x10, 0x7f],  # N
        79: [0x3e, 0x41, 0x41, 0x41, 0x3e],  # O
        80: [0x7f, 0x09, 0x09, 0x09, 0x06],  # P
        81: [0x3e, 0x41, 0x51, 0x21, 0x5e],  # Q
        82: [0x7f, 0x09, 0x19, 0x29, 0x46],  # R
        83: [0x46, 0x49, 0x49, 0x49, 0x31],  # S
        84: [0x01, 0x01, 0x7f, 0x01, 0x01],  # T
        85: [0x3f, 0x40, 0x40, 0x40, 0x3f],  # U
        86: [0x1f, 0x20, 0x40, 0x20, 0x1f],  # V
        87: [0x7f, 0x20, 0x18, 0x20, 0x7f],  # W
        88: [0x63, 0x14, 0x08, 0x14, 0x63],  # X
        89: [0x03, 0x04, 0x78, 0x04, 0x03],  # Y
        90: [0x61, 0x51, 0x49, 0x45, 0x43],  # Z
        91: [0x00, 0x00, 0x7f, 0x41, 0x41],  # [
        92: [0x02, 0x04, 0x08, 0x10, 0x20],  # \
        93: [0x41, 0x41, 0x7f, 0x00, 0x00],  # ]
        94: [0x04, 0x02, 0x01, 0x02, 0x04],  # ^
        95: [0x40, 0x40, 0x40, 0x40, 0x40],  # _
        96: [0x00, 0x01, 0x02, 0x04, 0x00],  # `
        97: [0x20, 0x54, 0x54, 0x54, 0x78],  # a
        98: [0x7f, 0x48, 0x44, 0x44, 0x38],  # b
        99: [0x38, 0x44, 0x44, 0x44, 0x20],  # c
        100: [0x38, 0x44, 0x44, 0x48, 0x7f],  # d
        101: [0x38, 0x54, 0x54, 0x54, 0x18],  # e
        102: [0x08, 0x7e, 0x09, 0x01, 0x02],  # f
        103: [0x08, 0x14, 0x54, 0x54, 0x3c],  # g
        104: [0x7f, 0x08, 0x04, 0x04, 0x78],  # h
        105: [0x00, 0x44, 0x7d, 0x40, 0x00],  # i
        106: [0x20, 0x40, 0x44, 0x3d, 0x00],  # j
        107: [0x00, 0x7f, 0x10, 0x28, 0x44],  # k
        108: [0x00, 0x41, 0x7f, 0x40, 0x00],  # l
        109: [0x7c, 0x04, 0x18, 0x04, 0x78],  # m
        110: [0x7c, 0x08, 0x04, 0x04, 0x78],  # n
        111: [0x38, 0x44, 0x44, 0x44, 0x38],  # o
        112: [0x7c, 0x14, 0x14, 0x14, 0x08],  # p
        113: [0x08, 0x14, 0x14, 0x18, 0x7c],  # q
        114: [0x7c, 0x08, 0x04, 0x04, 0x08],  # r
        115: [0x48, 0x54, 0x54, 0x54, 0x20],  # s
        116: [0x04, 0x3f, 0x44, 0x40, 0x20],  # t
        117: [0x3c, 0x40, 0x40, 0x20, 0x7c],  # u
        118: [0x1c, 0x20, 0x40, 0x20, 0x1c],  # v
        119: [0x3c, 0x40, 0x30, 0x40, 0x3c],  # w
        120: [0x44, 0x28, 0x10, 0x28, 0x44],  # x
        121: [0x0c, 0x50, 0x50, 0x50, 0x3c],  # y
        122: [0x44, 0x64, 0x54, 0x4c, 0x44],  # z
        123: [0x00, 0x08, 0x36, 0x41, 0x00],  # {
        124: [0x00, 0x00, 0x7f, 0x00, 0x00],  # |
        125: [0x00, 0x41, 0x36, 0x08, 0x00],  # }
        126: [0x08, 0x08, 0x2a, 0x1c, 0x08],  # ~
    }

    MODE = 0b00011000
    OPTS = 0b00001110  # 1110 = 35mA, 0000 = 40mA
    UPDATE = 0x01

    CMD_BRIGHTNESS = 0x19
    CMD_MODE = 0x00
    CMD_UPDATE = 0x0C
    CMD_OPTIONS = 0x0D

    CMD_MATRIX_L = 0x0E
    CMD_MATRIX_R = 0x01

    def __init__(self, i2c, address : int = 0x61, brightness: float = 0.1):
        assert i2c
        assert address in [0x61, 0x62, 0x63]

        self._bus = i2c
        self._address: int = address

        self.set_brightness(brightness)
        self.clear()

    def clear(self) -> None:
        """Clear both LED matrices.

        Must call .show() to display changes.

        """
        self._buf_matrix_left = [0 for _ in range(8)]
        self._buf_matrix_right = [0 for _ in range(8)]

    def set_brightness(self, brightness: float, update: bool = False) -> None:
        """Set brightness of both LED matrices.
        """
        assert brightness >= 0.0
        assert brightness <= 1.0

        self._brightness = int(brightness * 127.0)
        self._brightness = min(127, max(0, self._brightness))
        if update:
            self._bus.writeto_mem(self._address,
                                  LTP305.CMD_BRIGHTNESS,
                                  self._brightness.to_bytes(1, 'big'))

    def set_decimal(self,
                    left: Optional[bool] = None,
                    right: Optional[bool] = None) -> None:
        """Set decimal of left and/or right matrix.

        You can provide the state of left and right decimal dot.
        True imopies left, False implies right. None means no dot.
        """
        if left is not None:
            if left:
                self._buf_matrix_left[7] |= 0b01000000
            else:
                self._buf_matrix_left[7] &= 0b10111111
        if right is not None:
            if right:
                self._buf_matrix_right[6] |= 0b10000000
            else:
                self._buf_matrix_right[6] &= 0b01111111

    def set_pixel(self, x_pos: int, y_pos: int, state: bool) -> None:
        """Set a single pixel on the matrix.

        The x position is from 0 to 9 (0-4 on left matrix, 5-9 on right).
        y is the y position and state is implied as on/off.
        """
        if x_pos < 5:
            # Left matrix
            if state:
                self._buf_matrix_left[x_pos] |= (0b1 << y_pos)
            else:
                self._buf_matrix_left[x_pos] &= ~(0b1 << y_pos)
        else:
            # Right matrix
            x_pos -= 5
            if state:
                self._buf_matrix_right[y_pos] |= (0b1 << x_pos)
            else:
                self._buf_matrix_right[y_pos] &= ~(0b1 << x_pos)

    def set_pair(self, chars: str) -> None:
        """Set a character pair.
        """
        assert isinstance(chars, str)
        assert len(chars) == 2

        self.set_character(0, chars[0])
        self.set_character(5, chars[1])

    def set_character(self, x_offset: int, char: str) -> None:
        """Set a single character.

        The charcater x position is 0 for left, 5 for right.
        The charcter is a string character or ordinal.
        """
        bitmap: List[int] = LTP305.font[ord(char)]
        for char_x in range(5):
            for char_y in range(8):
                state = (bitmap[char_x] & (0b1 << char_y)) != 0
                self.set_pixel(x_offset + char_x, char_y, state)

    def show(self) -> None:
        """Update the LED matrix from the buffer.
        """
        self._bus.writeto_mem(self._address, LTP305.CMD_MATRIX_L,
                              bytearray(self._buf_matrix_left))
        self._bus.writeto_mem(self._address, LTP305.CMD_MATRIX_R,
                              bytearray(self._buf_matrix_right))
        self._bus.writeto_mem(self._address, LTP305.CMD_MODE,
                              LTP305.MODE.to_bytes(1, 'big'))
        self._bus.writeto_mem(self._address, LTP305.CMD_OPTIONS,
                              LTP305.OPTS.to_bytes(1, 'big'))
        self._bus.writeto_mem(self._address, LTP305.CMD_BRIGHTNESS,
                              self._brightness.to_bytes(1, 'big'))
        self._bus.writeto_mem(self._address, LTP305.CMD_UPDATE,
                              LTP305.UPDATE.to_bytes(1, 'big'))


if __name__ == '__main__':

    display: LTP305 = LTP305(_I2C, brightness=1.0)
    display.set_character(0, '1')
    display.set_character(5, '2')
    display.show()

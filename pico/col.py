"""A simple program that uses the bh1745 Luminance/Colour Sensor breakout.
"""

# pylint: disable=import-error, global-statement, duplicate-code

# The Pico/MicroPython may not have the typing module
try:
    from typing import Dict, Tuple
except ImportError:
    pass
import time

from pimoroni_i2c import PimoroniI2C  # type: ignore
from breakout_bh1745 import BreakoutBH1745  # type: ignore

_PINS_PICO_EXPLORER: Dict[str, int] = {'sda': 20, 'scl': 21}

_I2C: PimoroniI2C = PimoroniI2C(**_PINS_PICO_EXPLORER)
_BH1745: BreakoutBH1745 = BreakoutBH1745(_I2C)

_ILLUMINATE: bool = False

if _ILLUMINATE:
    _BH1745.leds(True)

# Reading the sensor twice
_COUNT: int = 2
while _COUNT:

    print('---')

    rgb: Tuple[int, int, int, int] = _BH1745.rgbc_raw()
    print(f'Raw: {rgb[0]}, {rgb[1]}, {rgb[2]}, {rgb[3]}')

    rgb= _BH1745.rgbc_clamped()
    print(f'Clamped: {rgb[0]}, {rgb[1]}, {rgb[2]}, {rgb[3]}')

    rgb_scaled: Tuple[int, int, int, int] = _BH1745.rgbc_scaled()
    hex_str: str = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])  # pylint: disable=consider-using-f-string
    print(f'Scaled: {rgb[0]}, {rgb[1]}, {rgb[2]} ({hex_str})')

    _COUNT -= 1

    if _COUNT:
        time.sleep(5)

if _ILLUMINATE:
    _BH1745.leds(False)

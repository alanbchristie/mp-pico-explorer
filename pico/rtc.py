"""Experimental RV3028 RTC Breakout Code.

Here, you're expected to have installed the custom MicroPython firmware
on your Pico, which gives us you the pimoroni_i2c and breakout_rtc modules.

See also: https://www.hardill.me.uk/wordpress/category/projects/
"""
# pylint: disable=import-error, global-statement, duplicate-code

# The Pico/MicroPython may not have the typing module
try:
    from typing import Dict, List, NoReturn
except ImportError:
    pass
import time

from pimoroni_i2c import PimoroniI2C  # type: ignore
from breakout_rtc import BreakoutRTC  # type: ignore
_PINS_PICO_EXPLORER: Dict[str, int] = {'sda': 20, 'scl': 21}
_I2C: PimoroniI2C = PimoroniI2C(**_PINS_PICO_EXPLORER)
_RTC: BreakoutRTC = BreakoutRTC(_I2C)

# Days of the week (1 == Monday)
_DOTW: List[str] = ['-', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Setting the time...
# The set_time() function takes values in the order:
#
# - seconds (0-60)
# - minutes (0-60)
# - hours (0-23)
# - day of the week (1-7 -> mon-sun)
# - day of month (1-31)
# - month (1-12)
# - year (2000-2099)
#
# i.e. to set to 14:46 20-Dec-21...
#
# >>> _RTC.set_time(0, 46, 14, 1, 20, 12, 2021)
# >>> _RTC.set_backup_switchover_mode(3)


def _rtc() -> NoReturn:
    """Just call the RTC, printing the latest time whenever it changes.
    """
    global _RTC

    # The current time.
    # Bank to force a print on the first call.
    str_time_current: str = ''
    str_date_current: str = ''
    while True:

        if _RTC.update_time():
            new_time: str = _RTC.string_time()
            new_date: str = _RTC.string_date()
            # If the time or date's changed,
            # update our record of the current time and print it
            if new_time != str_time_current or new_date != str_date_current:
                str_time_current = new_time
                str_date_current = new_date
                dotw: str = _DOTW[_RTC.get_weekday()]
                print(f'{dotw} {str_date_current} {str_time_current}')

        # Sleep (less than a second)
        time.sleep(0.5)


if __name__ == '__main__':
    _rtc()

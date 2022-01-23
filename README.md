# mp-pico-explorer

[![lint](https://github.com/alanbchristie/mp-pico-explorer/actions/workflows/lint.yaml/badge.svg)](https://github.com/alanbchristie/mp-pico-explorer/actions/workflows/lint.yaml)

A repository of Raspberry Pi Pico [MicroPython] code
developed to experiment with the microcontroller and peripherals
using the **Pimoroni** [Pico Explorer] base board.

My explorer is fitted with the following additional hardware: -

1.  [RV3028] Real Time Clock (RTC) at address 0x52
2.  [BH1745] Luminance and Colour Sensor at address 0x38
3.  [LTP305] LED Dot Matrix Breakout at address 0x61 and 0x62
4.  [MB85RC256V] 32KByte FRAM module attached to the breadboard at address 0x50

This repository contains the following software demonstration files: -

- `pico/btn.py` for the explorer built-in buttons
- `pico/rtc.py` for the RV3028 RTC breakout
- `pico/character_matrix.py` for the dual LTP305 5x7 LED matrix
- `pico/col.py` for the BH1745 Luminance/Colour breakout
- `pico/fram.py` for the FRAM module

---

[bh1745]: https://shop.pimoroni.com/products/bh1745-luminance-and-colour-sensor-breakout
[mb85rc256v]: https://shop.pimoroni.com/products/adafruit-i2c-non-volatile-fram-breakout-256kbit-32kbyte
[ltp305]: https://shop.pimoroni.com/products/led-dot-matrix-breakout?variant=32274405621843
[micropython]: https://micropython.org/download/rp2-pico
[pico explorer]: https://shop.pimoroni.com/products/pico-explorer-base
[rv3028]: https://shop.pimoroni.com/products/rv3028-real-time-clock-rtc-breakout

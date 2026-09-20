# ==================================================
# KEYPAD
# ==================================================

import time

import hardware
from config import KEYPAD_ADDR, KEYS


def write_pcf(value):

    hardware.i2c.writeto(KEYPAD_ADDR, bytes([value]))


def read_pcf():

    return hardware.i2c.readfrom(KEYPAD_ADDR, 1)[0]


def scan():

    for r in range(4):

        out = ~(1 << r) & 0x0F

        write_pcf(0xF0 | out)

        time.sleep_us(50)

        value = (~read_pcf()) >> 4

        for c in range(4):

            if value & (1 << c):

                return KEYS[r][c]

    return None
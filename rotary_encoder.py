# ==================================================
# ROTARY ENCODER
# ==================================================

from machine import Pin
import time


class RotaryEncoder:

    CW = (
        (0, 2),
        (2, 3),
        (3, 1),
        (1, 0)
    )

    CCW = (
        (0, 1),
        (1, 3),
        (3, 2),
        (2, 0)
    )

    def __init__(self, clk_pin, dt_pin, sw_pin=None):

        self.clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)

        self.dt = Pin(dt_pin, Pin.IN, Pin.PULL_UP)

        if sw_pin is not None:

            self.sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)

        else:

            self.sw = None

        self.position = 100

        self.counter = 0

        self.last_time = 0

        self.last_state = (self.clk.value() << 1) | self.dt.value()

    def update(self):

        now = time.ticks_ms()

        if time.ticks_diff(now, self.last_time) < 2:

            return

        self.last_time = now

        current = (self.clk.value() << 1) | self.dt.value()

        if current == self.last_state:

            return

        transition = (self.last_state, current)

        if transition in self.CW:

            self.counter += 1

        elif transition in self.CCW:

            self.counter -= 1

        if self.counter >= 4:

            if self.position > 0:

                self.position -= 5

            self.counter = 0

        elif self.counter <= -4:

            if self.position < 100:

                self.position += 5

            self.counter = 0

        self.last_state = current

    def get_position(self):

        return self.position

    def pressed(self):

        if self.sw is None:

            return False

        return self.sw.value() == 0
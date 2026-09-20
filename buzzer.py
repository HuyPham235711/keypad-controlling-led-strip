# ==================================================
# BUZZER PLAYER
# ==================================================

from machine import Pin, PWM
import time


class BuzzerPlayer:

    def __init__(self, pin, vol=512):

        self.pin = pin

        self.vol = vol

        self.buzzer = None

        self.mode = None

        self.stop_time = 0

        self.song = []

        self.index = 0

        self.playing = False

        self.next_time = 0

    def create_pwm(self, freq):

        if self.buzzer is not None:

            self.buzzer.deinit()

            self.buzzer = None

        self.buzzer = PWM(Pin(self.pin), freq=freq, duty=self.vol)

    def stop(self):

        if self.buzzer is not None:

            self.buzzer.duty(0)

            self.buzzer.deinit()

            self.buzzer = None

        self.playing = False

    def beep(self, freq, duration=100):

        self.stop()

        self.create_pwm(freq)

        self.mode = "beep"

        self.playing = True

        self.stop_time = time.ticks_add(time.ticks_ms(), duration)

    def play(self, song):

        self.stop()

        self.song = song

        self.index = 0

        self.mode = "song"

        self.playing = True

        self.next_time = time.ticks_ms()

    def update(self):

        if not self.playing:

            return

        now = time.ticks_ms()

        if self.mode == "beep":

            if time.ticks_diff(now, self.stop_time) >= 0:

                self.stop()

            return

        if time.ticks_diff(now, self.next_time) < 0:

            return

        if self.index >= len(self.song):

            self.stop()

            return

        note, duration = self.song[self.index]

        if note == "silence":

            if self.buzzer is not None:

                self.buzzer.duty(0)

        else:

            self.create_pwm(note)

        self.next_time = time.ticks_add(now, int(duration * 1000))

        self.index += 1
# ==================================================
# LED STATE & BASIC COLOR CONTROL
# ==================================================

import hardware
from config import LED_COLORS

system_on = True

led_brightness = 100

# Màu mặc định đầu tiên là trắng
current_color = (255, 255, 255)


def apply_brightness(color):

    r, g, b = color

    return (
        r * led_brightness // 100,
        g * led_brightness // 100,
        b * led_brightness // 100
    )


def set_color(r, g, b):

    global current_color

    current_color = (r, g, b)

    color = apply_brightness(current_color)

    hardware.leds.fill(color)
    hardware.leds.write()


def refresh_current_color():

    color = apply_brightness(current_color)

    hardware.leds.fill(color)
    hardware.leds.write()


def turn_off_leds():

    hardware.leds.fill((0, 0, 0))
    hardware.leds.write()


def set_code_color(code):

    if code in LED_COLORS:

        color = LED_COLORS[code]

        set_color(color[0], color[1], color[2])
# ==================================================
# HARDWARE
# ==================================================

from machine import Pin, I2C
import neopixel
import ssd1306

from config import (
    LED_PIN,
    NUM_LEDS,
    I2C_SCL_PIN,
    I2C_SDA_PIN,
    OLED_ADDR,
    OLED_WIDTH,
    OLED_HEIGHT,
)

leds = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))

oled = None


def scan_i2c():
    """Quét bus I2C cho tới khi tìm thấy đủ thiết bị (OLED + keypad)."""

    global oled

    while True:

        devices = i2c.scan()

        print("I2C devices:", devices, ". Scanning..")

        if OLED_ADDR in devices:

            oled = ssd1306.SSD1306_I2C(
                OLED_WIDTH,
                OLED_HEIGHT,
                i2c,
                addr=OLED_ADDR
            )

            oled.fill(0)
            oled.text("SYSTEM ON", 0, 0)
            oled.show()

        if len(devices) == 2:

            print("found", len(devices), "devices")

            break
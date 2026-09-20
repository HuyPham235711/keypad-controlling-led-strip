# ==================================================
# SYSTEM POWER
# ==================================================

import hardware
import led_control
import led_effects


def turn_off_system():

    led_control.system_on = False

    led_effects.stop_all_effects()

    led_control.turn_off_leds()

    if hardware.oled is not None:

        hardware.oled.fill(0)
        hardware.oled.show()


def turn_on_system():

    led_control.system_on = True

    if hardware.oled is not None:

        hardware.oled.fill(0)
        hardware.oled.text("SYSTEM ON", 0, 0)
        hardware.oled.show()

    led_control.refresh_current_color()
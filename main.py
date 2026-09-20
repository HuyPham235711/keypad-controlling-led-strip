
import time

import hardware
import led_control
import led_effects
import system_control
import keypad
import music

from config import (
    BUZZER1_PIN,
    BUZZER2_PIN,
    ROTARY_CLK_PIN,
    ROTARY_DT_PIN,
    ROTARY_SWITCH_PIN,
    KEYBOARD_SOUND,
)
from rotary_encoder import RotaryEncoder
from buzzer import BuzzerPlayer


# ==================================================
# MAIN WORKER
# ==================================================

def worker():

    encoder = RotaryEncoder(
        clk_pin=ROTARY_CLK_PIN,
        dt_pin=ROTARY_DT_PIN,
        sw_pin=ROTARY_SWITCH_PIN
    )

    buzzer1_player = BuzzerPlayer(BUZZER1_PIN, vol=20)
    buzzer2_player = BuzzerPlayer(BUZZER2_PIN, vol=512)

    rotary_last = encoder.get_position()

    last_key = None

    last_switch = 1

    buffer = ""

    # Default color = WHITE
    led_control.set_color(255, 255, 255)

    while True:

        # ==========================================
        # ROTARY ENCODER
        # ==========================================

        encoder.update()

        # ==========================================
        # BRIGHTNESS
        # ==========================================

        pos = encoder.get_position()

        if pos != rotary_last:

            led_control.led_brightness = pos

            print("Brightness:", led_control.led_brightness, "%")

            if hardware.oled is not None:

                hardware.oled.fill(0)

                hardware.oled.text(
                    "BRIGHTNESS: " + str(led_control.led_brightness) + "%",
                    0,
                    0
                )

                hardware.oled.show()

            if led_control.system_on:

                if not led_effects.any_effect_active():

                    led_control.refresh_current_color()

            rotary_last = pos

        # ==========================================
        # ROTARY SWITCH
        # ==========================================

        switch = encoder.sw.value()

        if last_switch == 1 and switch == 0:

            if led_control.system_on:

                system_control.turn_off_system()

                print("SYSTEM OFF")

            else:

                system_control.turn_on_system()

                print("SYSTEM ON")

            time.sleep_ms(200)

        last_switch = switch

        # ==========================================
        # LED EFFECTS
        # ==========================================

        if led_control.system_on:

            led_effects.update_all_effects()

        # ==========================================
        # BUZZERS
        # ==========================================

        if led_control.system_on:

            buzzer1_player.update()

            buzzer2_player.update()

        # ==========================================
        # KEYPAD
        # ==========================================

        if led_control.system_on:

            key = keypad.scan()

        else:

            key = None

        # ==========================================
        # KEYPAD INPUT
        # ==========================================

        if key is not None and key != last_key:

            # ======================================
            # ENTER
            # ======================================

            if key == "*":

                print("string:", buffer)

                if hardware.oled is not None:

                    hardware.oled.fill(0)

                    hardware.oled.text(buffer, 0, 0)

                    hardware.oled.show()

                entered_code = buffer

                # C137 = DANCING SHADOW
                if buffer == "C137":

                    led_effects.stop_all_effects()

                    led_effects.start_dancing_shadow()

                # 12C1 = COLOR TWINKLES
                elif buffer == "12C1":

                    led_effects.stop_all_effects()

                    led_effects.start_colortwinkles()

                # D21 = HELLFIRE
                elif buffer == "D21":

                    led_effects.stop_all_effects()

                    led_effects.start_hellfire()

                # 101 = MATRIX
                elif buffer == "101":

                    led_effects.stop_all_effects()

                    led_effects.start_matrix()

                # 42 = COSMOS
                elif buffer == "42":

                    led_effects.stop_all_effects()

                    led_effects.start_cosmos()

                # Single key = color
                elif len(buffer) == 1:

                    led_effects.stop_all_effects()

                    led_control.set_code_color(buffer)

                buffer = ""

                if entered_code in music.CODE_SONGS:

                    song1, song2 = music.CODE_SONGS[entered_code]

                    buzzer1_player.play(song1)

                    buzzer2_player.play(song2)

                else:

                    buzzer1_player.play(music.SOUND1)

                    buzzer2_player.play(music.SOUND2)

            # ======================================
            # DELETE
            # ======================================

            elif key == "#":

                buffer = buffer[:-1]

                print("keypad:", buffer)

                if hardware.oled is not None:

                    hardware.oled.fill(0)

                    hardware.oled.text("Key pressed:", 0, 0)

                    hardware.oled.text(buffer, 0, 20)

                    hardware.oled.show()

                buzzer1_player.beep(200)

            # ======================================
            # NORMAL KEY
            # ======================================

            else:

                buffer += key

                print("keypad:", buffer)

                if hardware.oled is not None:

                    hardware.oled.fill(0)

                    hardware.oled.text("Key pressed:", 0, 0)

                    hardware.oled.text(buffer, 0, 20)

                    hardware.oled.show()

                buzzer2_player.beep(KEYBOARD_SOUND[key])

        last_key = key


# ==================================================
# START PROGRAM
# ==================================================

if __name__ == "__main__":

    hardware.scan_i2c()

    worker()

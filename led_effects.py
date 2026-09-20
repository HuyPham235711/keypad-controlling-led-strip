# ==================================================
# LED EFFECTS
# ==================================================


import random
import math
import time

import hardware
import led_control
from config import NUM_LEDS


# ==================================================
# DANCING SHADOW (green portal effect)
# ==================================================

dancing_shadow_active = False

dancing_shadow_position = 0

dancing_shadow_last_update = 0

SHADOW_LENGTH = 25

SHADOW_SPEED_MS = 20

SHADOW_BACKGROUND = (0, 15, 0)


def start_dancing_shadow():

    global dancing_shadow_active
    global dancing_shadow_position
    global dancing_shadow_last_update

    dancing_shadow_active = True

    dancing_shadow_position = -SHADOW_LENGTH

    dancing_shadow_last_update = time.ticks_ms()


def stop_dancing_shadow():

    global dancing_shadow_active

    dancing_shadow_active = False

    led_control.refresh_current_color()


def update_dancing_shadow():

    global dancing_shadow_position
    global dancing_shadow_last_update

    if not dancing_shadow_active:

        return

    now = time.ticks_ms()

    if time.ticks_diff(now, dancing_shadow_last_update) < SHADOW_SPEED_MS:

        return

    dancing_shadow_last_update = now

    # Background - dim swirling green base
    background = led_control.apply_brightness(SHADOW_BACKGROUND)

    hardware.leds.fill(background)

    # Portal band - bright acid green core fading to
    # yellow-green edges, with a flicker so it feels
    # unstable like a portal ring
    for i in range(SHADOW_LENGTH):

        led_index = dancing_shadow_position + i

        if 0 <= led_index < NUM_LEDS:

            fade = 1 - i / SHADOW_LENGTH

            flicker = random.randint(85, 100) / 100

            intensity = fade * flicker

            # Core is bright yellow-green, edges shift
            # toward deeper green
            r = int(60 * intensity)
            g = int(255 * intensity)
            b = int(30 * intensity)

            shadow_color = (
                r * led_control.led_brightness // 100,
                g * led_control.led_brightness // 100,
                b * led_control.led_brightness // 100
            )

            hardware.leds[led_index] = shadow_color

    hardware.leds.write()

    dancing_shadow_position += 1

    if dancing_shadow_position >= NUM_LEDS:

        dancing_shadow_position = -SHADOW_LENGTH


# ==================================================
# COLOR TWINKLES
# ==================================================

colortwinkles_active = False

colortwinkles_last_update = 0

colortwinkles_pixels = {}

TWINKLE_SPEED_MS = 30

TWINKLE_SPAWN_CHANCE = 25

TWINKLE_MAX_ACTIVE = 40

TWINKLE_FADE_STEP = 18


def start_colortwinkles():

    global colortwinkles_active
    global colortwinkles_pixels
    global colortwinkles_last_update

    colortwinkles_active = True

    colortwinkles_pixels = {}

    colortwinkles_last_update = time.ticks_ms()


def stop_colortwinkles():

    global colortwinkles_active
    global colortwinkles_pixels

    colortwinkles_active = False

    colortwinkles_pixels = {}

    led_control.refresh_current_color()


def random_twinkle_color():

    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def update_colortwinkles():

    global colortwinkles_last_update

    if not colortwinkles_active:

        return

    now = time.ticks_ms()

    if time.ticks_diff(now, colortwinkles_last_update) < TWINKLE_SPEED_MS:

        return

    colortwinkles_last_update = now

    hardware.leds.fill((0, 0, 0))

    # Spawn new twinkles
    if len(colortwinkles_pixels) < TWINKLE_MAX_ACTIVE:

        if random.randint(0, 100) < TWINKLE_SPAWN_CHANCE:

            index = random.randint(0, NUM_LEDS - 1)

            if index not in colortwinkles_pixels:

                colortwinkles_pixels[index] = {
                    "color": random_twinkle_color(),
                    "brightness": 255
                }

    # Update and draw existing twinkles
    dead = []

    for index in colortwinkles_pixels:

        twinkle = colortwinkles_pixels[index]

        r, g, b = twinkle["color"]

        scale = (
            twinkle["brightness"] * led_control.led_brightness
        ) / (255 * 100)

        hardware.leds[index] = (
            int(r * scale),
            int(g * scale),
            int(b * scale)
        )

        twinkle["brightness"] -= TWINKLE_FADE_STEP

        if twinkle["brightness"] <= 0:

            dead.append(index)

    for index in dead:

        del colortwinkles_pixels[index]

    hardware.leds.write()


# ==================================================
# HELLFIRE (full strip blazing fire)
# ==================================================

hellfire_active = False

hellfire_heat = []

hellfire_heat_buffer = []

hellfire_last_update = 0

FIRE_SPEED_MS = 25

FIRE_COOLING = 55

FIRE_SPARKING = 90

# How many ignition attempts happen across the WHOLE
# strip every single tick. High value = the entire
# strip stays lit and blazing instead of a single
# flame traveling from one end.
FIRE_SPARKS_PER_TICK = 25


def start_hellfire():

    global hellfire_active
    global hellfire_heat
    global hellfire_heat_buffer
    global hellfire_last_update

    hellfire_active = True

    hellfire_heat = [0] * NUM_LEDS

    hellfire_heat_buffer = [0] * NUM_LEDS

    hellfire_last_update = time.ticks_ms()


def stop_hellfire():

    global hellfire_active

    hellfire_active = False

    led_control.refresh_current_color()


def hellfire_color(heat):

    # Maps a heat value (0-255) to a hellfire color.
    # Stays red-toned at all heat levels — deep red
    # at low heat, bright red in the middle, hot
    # red-orange only at the very peak (never yellow).

    t192 = (heat * 191) // 255

    heatramp = t192 & 0x3F

    heatramp <<= 2

    if t192 & 0x80:

        return (255, heatramp // 6, 0)

    elif t192 & 0x40:

        return (200 + heatramp // 8, 0, 0)

    else:

        return (heatramp, 0, 0)


def update_hellfire():

    global hellfire_last_update
    global hellfire_heat
    global hellfire_heat_buffer

    if not hellfire_active:

        return

    now = time.ticks_ms()

    if time.ticks_diff(now, hellfire_last_update) < FIRE_SPEED_MS:

        return

    hellfire_last_update = now

    # Step 1: cool down every cell a little
    max_cooldown = ((FIRE_COOLING * 10) // NUM_LEDS) + 2

    for i in range(NUM_LEDS):

        cooldown = random.randint(0, max_cooldown)

        hellfire_heat[i] = max(0, hellfire_heat[i] - cooldown)

    # Step 2: heat diffuses symmetrically to both
    # neighbors, so flames flicker and lick upward
    # everywhere along the strip, not just from one end.
    for i in range(NUM_LEDS):

        left = hellfire_heat[i - 1] if i > 0 else hellfire_heat[i]

        right = (
            hellfire_heat[i + 1]
            if i < NUM_LEDS - 1
            else hellfire_heat[i]
        )

        hellfire_heat_buffer[i] = (
            left + (hellfire_heat[i] * 2) + right
        ) // 4

    hellfire_heat, hellfire_heat_buffer = (
        hellfire_heat_buffer,
        hellfire_heat
    )

    # Step 3: randomly ignite new sparks all across
    # the entire strip, not just near one base
    for _ in range(FIRE_SPARKS_PER_TICK):

        if random.randint(0, 255) < FIRE_SPARKING:

            spark = random.randint(0, NUM_LEDS - 1)

            hellfire_heat[spark] = min(
                255,
                hellfire_heat[spark] + random.randint(160, 255)
            )

    # Step 4: map heat to colors and draw
    scale = led_control.led_brightness / 100

    for i in range(NUM_LEDS):

        r, g, b = hellfire_color(hellfire_heat[i])

        hardware.leds[i] = (
            int(r * scale),
            int(g * scale),
            int(b * scale)
        )

    hardware.leds.write()


# ==================================================
# MATRIX (digital rain)
# ==================================================

matrix_active = False

matrix_drops = []

matrix_last_update = 0

MATRIX_SPEED_MS = 20

MATRIX_DROP_COUNT = 14

MATRIX_MIN_TRAIL = 10

MATRIX_MAX_TRAIL = 45

MATRIX_MIN_DELAY = 1

MATRIX_MAX_DELAY = 3


def new_matrix_drop():

    return {
        "pos": -random.randint(0, NUM_LEDS),
        "trail": random.randint(MATRIX_MIN_TRAIL, MATRIX_MAX_TRAIL),
        "delay": random.randint(MATRIX_MIN_DELAY, MATRIX_MAX_DELAY),
        "counter": 0
    }


def start_matrix():

    global matrix_active
    global matrix_drops
    global matrix_last_update

    matrix_active = True

    matrix_drops = [new_matrix_drop() for _ in range(MATRIX_DROP_COUNT)]

    matrix_last_update = time.ticks_ms()


def stop_matrix():

    global matrix_active

    matrix_active = False

    led_control.refresh_current_color()


def update_matrix():

    global matrix_last_update

    if not matrix_active:

        return

    now = time.ticks_ms()

    if time.ticks_diff(now, matrix_last_update) < MATRIX_SPEED_MS:

        return

    matrix_last_update = now

    hardware.leds.fill((0, 0, 0))

    scale = led_control.led_brightness / 100

    for drop in matrix_drops:

        drop["counter"] += 1

        if drop["counter"] >= drop["delay"]:

            drop["counter"] = 0

            drop["pos"] += 1

        trail = drop["trail"]

        head = drop["pos"]

        for i in range(trail):

            index = head - i

            if 0 <= index < NUM_LEDS:

                if i == 0:

                    color = (200, 255, 200)

                else:

                    fade = 255 * (trail - i) // trail

                    color = (0, fade, 0)

                hardware.leds[index] = (
                    int(color[0] * scale),
                    int(color[1] * scale),
                    int(color[2] * scale)
                )

        if head - trail > NUM_LEDS:

            new_drop = new_matrix_drop()

            drop["pos"] = new_drop["pos"]
            drop["trail"] = new_drop["trail"]
            drop["delay"] = new_drop["delay"]
            drop["counter"] = 0

    hardware.leds.write()


# ==================================================
# COSMOS
# ==================================================

cosmos_active = False

cosmos_offset = 0

cosmos_last_update = 0

cosmos_stars = {}

cosmos_palette = []

COSMOS_SPEED_MS = 40

COSMOS_WAVE_LENGTH = 60

COSMOS_STAR_CHANCE = 6

COSMOS_MAX_STARS = 15

COSMOS_STAR_FADE = 15


def build_cosmos_palette():

    global cosmos_palette

    cosmos_palette = []

    for i in range(COSMOS_WAVE_LENGTH):

        angle = i * (2 * math.pi / COSMOS_WAVE_LENGTH)

        wave = (math.sin(angle) + 1) / 2

        r = int(10 + wave * 70)
        g = 0
        b = int(60 + wave * 60)

        cosmos_palette.append((r, g, b))


def start_cosmos():

    global cosmos_active
    global cosmos_offset
    global cosmos_stars
    global cosmos_last_update

    if not cosmos_palette:

        build_cosmos_palette()

    cosmos_active = True

    cosmos_offset = 0

    cosmos_stars = {}

    cosmos_last_update = time.ticks_ms()


def stop_cosmos():

    global cosmos_active

    cosmos_active = False

    led_control.refresh_current_color()


def update_cosmos():

    global cosmos_offset
    global cosmos_last_update
    global cosmos_stars

    if not cosmos_active:

        return

    now = time.ticks_ms()

    if time.ticks_diff(now, cosmos_last_update) < COSMOS_SPEED_MS:

        return

    cosmos_last_update = now

    cosmos_offset += 1

    if cosmos_offset >= COSMOS_WAVE_LENGTH:

        cosmos_offset = 0

    # Spawn stars
    if len(cosmos_stars) < COSMOS_MAX_STARS:

        if random.randint(0, 100) < COSMOS_STAR_CHANCE:

            index = random.randint(0, NUM_LEDS - 1)

            if index not in cosmos_stars:

                cosmos_stars[index] = 255

    scale = led_control.led_brightness / 100

    for i in range(NUM_LEDS):

        palette_index = (i + cosmos_offset) % COSMOS_WAVE_LENGTH

        r, g, b = cosmos_palette[palette_index]

        if i in cosmos_stars:

            factor = cosmos_stars[i] / 255

            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)

        hardware.leds[i] = (
            int(r * scale),
            int(g * scale),
            int(b * scale)
        )

    dead = []

    for index in cosmos_stars:

        cosmos_stars[index] -= COSMOS_STAR_FADE

        if cosmos_stars[index] <= 0:

            dead.append(index)

    for index in dead:

        del cosmos_stars[index]

    hardware.leds.write()


# ==================================================
# HELPERS
# ==================================================

def stop_all_effects():
    """Tắt tất cả hiệu ứng đang chạy (dùng khi chuyển hiệu ứng hoặc tắt hệ thống)."""

    stop_dancing_shadow()
    stop_colortwinkles()
    stop_hellfire()
    stop_matrix()
    stop_cosmos()


def any_effect_active():

    return (
        dancing_shadow_active
        or colortwinkles_active
        or hellfire_active
        or matrix_active
        or cosmos_active
    )


def update_all_effects():
    """Gọi mỗi vòng lặp; mỗi update_*() tự bỏ qua nếu hiệu ứng không active."""

    update_dancing_shadow()
    update_colortwinkles()
    update_hellfire()
    update_matrix()
    update_cosmos()
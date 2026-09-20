# ==================================================
# MUSIC
# ==================================================

NOTES = {
    "C3": 131,
    "D3": 147,
    "E3": 165,
    "F3": 175,
    "G3": 196,
    "A3": 220,
    "B3": 247,
    "Db3": 139,
    "Bb3": 233,

    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "Db4": 277,
    "Bb4": 466,

    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
    "G5": 784,
    "A5": 880,
    "B5": 988,

    "C6": 1047,
    "D6": 1175,
    "E6": 1319,

    # extra notes used by CODE JINGLES below
    "Db5": 554,
    "Eb5": 622,
    "Gb5": 740,
    "Ab5": 831,
    "Gb4": 370,
    "Ab4": 415,
    "Eb4": 311,
    "Ab3": 208,
    "C2": 65,
    "Db2": 69,
    "D2": 73,
}


SOUND1 = [
    (NOTES["D5"], 0.16),
    (NOTES["E5"], 0.16),
    (NOTES["A5"], 0.16),
    (NOTES["A4"], 0.25)
]


SOUND2 = [
    (NOTES["D5"], 0.16),
    (NOTES["E5"], 0.16),
    (NOTES["A5"], 0.16),
    (NOTES["A4"], 0.25)
]


# ==================================================
# CODE JINGLES
# (original mood-matched compositions, not
# transcriptions of any copyrighted song. Each track
# runs roughly 7-10 seconds.)
# ==================================================

# --------------------------------------------------
# C137 - your riff (replaces old sci-fi portal theme)
# --------------------------------------------------

SONG_C137_1 = [  # buzzer1 - high e string melody
    (NOTES["Bb4"], 0.60), (NOTES["Db5"], 0.30),
    (NOTES["C5"], 0.30), (NOTES["Eb5"], 0.30),
    (NOTES["Ab4"], 0.30), (NOTES["Gb4"], 0.30),
    (NOTES["F4"], 0.70),
    ("silence", 0.30),
    (NOTES["F5"], 0.30),
    ("silence", 0.10),
    (NOTES["F5"], 0.30),
    ("silence", 0.30),
    (NOTES["Bb4"], 0.60),
    ("silence", 0.20),
    (NOTES["Db5"], 0.30), (NOTES["C5"], 0.30),
    (NOTES["Eb5"], 0.30), (NOTES["Ab5"], 0.30),
    (NOTES["Gb5"], 0.30), (NOTES["F5"], 0.30),
    ("silence", 0.30),
    (NOTES["Bb4"], 0.50), (NOTES["Db5"], 0.50),
    (NOTES["Eb5"], 0.30), (NOTES["C5"], 0.30),
    (NOTES["Eb5"], 0.30), (NOTES["Ab5"], 0.30),
    (NOTES["Gb5"], 0.30), (NOTES["F5"], 0.30),
]

SONG_C137_2 = [  # buzzer2 - B/G string harmony, fills the gaps
    (NOTES["F4"], 0.50),
    ("silence", 0.70),
    (NOTES["Gb4"], 0.30), (NOTES["F4"], 0.30),
    ("silence", 0.30),
    (NOTES["F4"], 0.30),
    ("silence", 0.7),
    (NOTES["Gb4"], 0.30),
    ("silence", 0.10),
    (NOTES["Gb4"], 0.30)
]


# --------------------------------------------------
# 12C1 - D/Gm shapes, capo 3 (sounds in F)
# --------------------------------------------------

_12c1_bar_d = [
    (NOTES["A4"], 0.30),   # e, fret 2
    (NOTES["C4"], 0.30),   # G, fret 2
    (NOTES["F4"], 0.30),   # B, fret 3
    (NOTES["C4"], 0.30),   # G, fret 2
    (NOTES["A4"], 0.30),   # e, fret 2
    (NOTES["C4"], 0.30),   # G, fret 2
    (NOTES["F4"], 0.30),   # B, fret 3
    (NOTES["C4"], 0.30),   # G, fret 2
]

_12c1_bar_gm = [
    (NOTES["A4"], 0.30),   # e, fret 2
    (NOTES["C4"], 0.30),   # G, fret 2
    (NOTES["F4"], 0.30),   # B, fret 3
    (NOTES["C4"], 0.30),   # G, fret 2
    (NOTES["Bb3"], 0.30),  # G, fret 0
    (NOTES["Db4"], 0.30),  # G, fret 3
    (NOTES["F4"], 0.30),   # B, fret 3
    (NOTES["G4"], 0.30),   # e, fret 0
]

SONG_12C1_1 = (_12c1_bar_d + _12c1_bar_gm) * 2

SONG_12C1_2 = []


# --------------------------------------------------
# 42 - slow-building synthwave pulse
# --------------------------------------------------

_42_swell = [
    (NOTES["A4"], 0.30), (NOTES["C5"], 0.30),
    (NOTES["E5"], 0.30), (NOTES["A5"], 0.60),
    ("silence", 0.15)
]

_42_swell_down = [
    (NOTES["E5"], 0.30), (NOTES["C5"], 0.30),
    (NOTES["A4"], 0.60), ("silence", 0.15)
]

_42_pulse = [
    (NOTES["A5"], 0.10), (NOTES["G5"], 0.10),
    (NOTES["A5"], 0.10), (NOTES["G5"], 0.10),
    (NOTES["A5"], 0.10), (NOTES["E5"], 0.10),
    (NOTES["A5"], 0.30), ("silence", 0.15)
]

_42_outro = [
    (NOTES["C5"], 0.30), (NOTES["E5"], 0.30),
    (NOTES["A5"], 1.00)
]

SONG_42_1 = (
    _42_swell
    + _42_swell_down
    + _42_pulse
    + _42_swell
    + _42_outro
)

_42_bass_swell = [
    (NOTES["A3"], 0.30), (NOTES["A3"], 0.30),
    (NOTES["A3"], 0.30), (NOTES["A3"], 0.60),
    ("silence", 0.15)
]

_42_bass_down = [
    (NOTES["E3"], 0.30), (NOTES["E3"], 0.30),
    (NOTES["A3"], 0.60), ("silence", 0.15)
]

_42_bass_pulse = [
    (NOTES["A3"], 0.10), (NOTES["A3"], 0.10),
    (NOTES["A3"], 0.10), (NOTES["A3"], 0.10),
    (NOTES["A3"], 0.10), (NOTES["E3"], 0.10),
    (NOTES["A3"], 0.30), ("silence", 0.15)
]

_42_bass_outro = [
    (NOTES["A3"], 0.30), (NOTES["E3"], 0.30),
    (NOTES["A3"], 1.00)
]

SONG_42_2 = (
    _42_bass_swell
    + _42_bass_down
    + _42_bass_pulse
    + _42_bass_swell
    + _42_bass_outro
)


# --------------------------------------------------
# 101 - dark, moody descending phrase
# --------------------------------------------------

SONG_101_1 = [
    (NOTES["G4"], 2.00),
    (NOTES["A4"], 2.00),
    (NOTES["Bb4"], 2.00),
    (NOTES["C5"], 2.00)
]

SONG_101_2 = [  # buzzer2 - drum-style beat (kick pattern)
    (NOTES["C3"], 0.08), ("silence", 0.42),   # beat 1
    (NOTES["C3"], 0.08), ("silence", 0.42),   # beat 2
    (NOTES["C3"], 0.08), ("silence", 0.16),   # beat 3 (short)
    (NOTES["C3"], 0.08), ("silence", 0.42),   # beat 4 (extra hit)
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.16),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.16),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.42),
    (NOTES["C3"], 0.08), ("silence", 0.16),
    (NOTES["C3"], 0.08), ("silence", 0.42),
]


# --------------------------------------------------
# D21 - aggressive, fast industrial stab
# --------------------------------------------------

SONG_D21_1 = [  # buzzer1 - melody
    (NOTES["Ab4"], 2.00),
    (NOTES["B4"], 0.50),
    (NOTES["G4"], 2.00),
    (NOTES["Ab4"], 0.60),
    (NOTES["E4"], 1.40),
    (NOTES["Eb4"], 1.20),
    (NOTES["D4"], 1.20),
    (NOTES["Db4"], 1.00),
]

SONG_D21_2 = [  # buzzer2 - sustained background pad
    (NOTES["Ab3"], 2.50),   # dưới Ab4+B4
    (NOTES["G3"], 2.60),    # dưới G4+Ab4
    (NOTES["C3"], 2.60),    # dưới E4+Eb4
    (NOTES["Db3"], 2.20),   # dưới D4+Db4
]


CODE_SONGS = {
    "C137": (SONG_C137_1, SONG_C137_2),
    "12C1": (SONG_12C1_1, SONG_12C1_2),
    "42": (SONG_42_1, SONG_42_2),
    "101": (SONG_101_1, SONG_101_2),
    "D21": (SONG_D21_1, SONG_D21_2)
}
"""Schematic valve/contraction timing, shared by every cardiac scene."""
from math import sin, pi

def cardiac_cycle(seconds):
    wave = sin(seconds * 2 * pi * 1.2)  # 72 beats/minute
    contraction = max(0.0, wave) ** 5
    semilunar = max(0.0, min(1.0, (wave - .05) * 3))
    atrioventricular = max(0.0, min(1.0, (-wave - .05) * 3))
    return contraction, atrioventricular, semilunar

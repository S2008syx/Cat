"""
Human Design Calculator - Gate Mapping Layer

Maps ecliptic longitudes to Human Design gates, lines, colors, tones, and bases.
Pure mathematical mapping with zero external dependencies.

Subdivision hierarchy (each level divides the parent equally):
  Gate  = 5.625°   (360° / 64)
  Line  = 0.9375°  (5.625° / 6)
  Color = 0.15625° (0.9375° / 6)
  Tone  = 0.026041…° (0.15625° / 6)
  Base  = 0.005208…° (0.026041° / 5)
"""

from __future__ import annotations

import math

from .data.gates import GATE_ORDER, GATE_START_LONGITUDE, DEGREES_PER_GATE, DEGREES_PER_LINE

# Subdivision constants derived from the gate/line structure.
# Each level divides the parent arc equally.
DEGREES_PER_COLOR: float = DEGREES_PER_LINE / 6    # 0.15625°
DEGREES_PER_TONE: float = DEGREES_PER_COLOR / 6    # ~0.026042°
DEGREES_PER_BASE: float = DEGREES_PER_TONE / 5     # ~0.005208°


# [SOURCE] 参考: humandesign_api (https://github.com/dturkuler/humandesign_api),
#   human_design_engine (https://github.com/MicFell/human_design_engine),
#   PyHD 开发博客 (https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library)
# 参考内容: 黄经度数到门/爻的映射公式 — 302° 起点、5.625° 每门、GATE_ORDER 查表
# 修改说明: 实现为独立函数，添加边界处理和类型标注；扩展至 Color/Tone/Base 细分

def longitude_to_gate_line(longitude: float) -> tuple[int, int]:
    """Map an ecliptic longitude to a Human Design gate and line.

    The ecliptic (360°) is divided into 64 gates of 5.625° each.
    Each gate has 6 lines of 0.9375° each.
    The sequence starts at Gate 41 at longitude 302° (Aquarius 2°).

    Args:
        longitude: Ecliptic longitude in degrees (0-360).

    Returns:
        Tuple of (gate_number, line_number) where gate is 1-64 and line is 1-6.
    """
    # Normalize longitude to 0-360
    longitude = longitude % 360.0

    # Calculate offset from the starting point (302°)
    offset = (longitude - GATE_START_LONGITUDE) % 360.0

    # Determine gate index (0-63)
    gate_index = int(offset / DEGREES_PER_GATE)
    gate_index = min(gate_index, 63)  # Safety clamp

    # Determine line within the gate (1-6)
    remainder = offset - (gate_index * DEGREES_PER_GATE)
    line = int(remainder / DEGREES_PER_LINE) + 1
    line = min(line, 6)  # Safety clamp

    gate = GATE_ORDER[gate_index]
    return gate, line


def longitude_to_gate_line_color_tone_base(
    longitude: float,
) -> tuple[int, int, int, int, int]:
    """Map an ecliptic longitude to Gate, Line, Color, Tone, and Base.

    Subdivision hierarchy (each level divides its parent equally):
      Gate  = 5.625°         (360° / 64 gates)
      Line  = 0.9375°        (5.625° / 6 lines)
      Color = 0.15625°       (0.9375° / 6 colors)
      Tone  = 0.026041…°     (0.15625° / 6 tones)
      Base  = 0.005208…°     (0.026041° / 5 bases)

    Color, Tone, and Base are used in advanced Human Design analysis
    (Variables / Arrows) to determine cognitive orientation.

    Args:
        longitude: Ecliptic longitude in degrees (0-360).

    Returns:
        Tuple of (gate, line, color, tone, base):
          - gate:  1-64
          - line:  1-6
          - color: 1-6
          - tone:  1-6
          - base:  1-5
    """
    longitude = longitude % 360.0
    offset = (longitude - GATE_START_LONGITUDE) % 360.0

    # Gate (1-64)
    gate_index = int(offset / DEGREES_PER_GATE)
    gate_index = min(gate_index, 63)
    remainder = offset - gate_index * DEGREES_PER_GATE

    # Line (1-6)
    line_index = int(remainder / DEGREES_PER_LINE)
    line_index = min(line_index, 5)
    remainder -= line_index * DEGREES_PER_LINE

    # Color (1-6)
    color_index = int(remainder / DEGREES_PER_COLOR)
    color_index = min(color_index, 5)
    remainder -= color_index * DEGREES_PER_COLOR

    # Tone (1-6)
    tone_index = int(remainder / DEGREES_PER_TONE)
    tone_index = min(tone_index, 5)
    remainder -= tone_index * DEGREES_PER_TONE

    # Base (1-5)
    base_index = int(remainder / DEGREES_PER_BASE)
    base_index = min(base_index, 4)

    gate = GATE_ORDER[gate_index]
    return gate, line_index + 1, color_index + 1, tone_index + 1, base_index + 1


def map_all_activations(planet_positions: dict[str, float]) -> list[dict]:
    """Map all planetary positions to gate/line/color/tone/base activations.

    Args:
        planet_positions: Dictionary of {planet_name: ecliptic_longitude}.

    Returns:
        List of activation dicts, each containing:
        {
            "planet": "sun",
            "gate": 41,
            "line": 3,
            "color": 2,
            "tone": 5,
            "base": 1,
            "longitude": 302.5,
        }
    """
    # Define the planet order for Human Design
    planet_order = [
        "sun", "earth", "moon", "north_node", "south_node",
        "mercury", "venus", "mars", "jupiter", "saturn",
        "uranus", "neptune", "pluto",
    ]

    activations: list[dict] = []
    for planet in planet_order:
        if planet not in planet_positions:
            continue
        lon = planet_positions[planet]
        gate, line, color, tone, base = longitude_to_gate_line_color_tone_base(lon)
        activations.append({
            "planet": planet,
            "gate": gate,
            "line": line,
            "color": color,
            "tone": tone,
            "base": base,
            "longitude": round(lon, 6),
        })

    return activations

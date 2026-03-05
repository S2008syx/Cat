"""
Human Design Calculator - Gate Mapping Layer

Maps ecliptic longitudes to Human Design gates and lines.
Pure mathematical mapping with zero external dependencies.
"""

from __future__ import annotations

import math

from .data.gates import GATE_ORDER, GATE_START_LONGITUDE, DEGREES_PER_GATE, DEGREES_PER_LINE


# [SOURCE] 参考: humandesign_api (https://github.com/dturkuler/humandesign_api),
#   human_design_engine (https://github.com/MicFell/human_design_engine),
#   PyHD 开发博客 (https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library)
# 参考内容: 黄经度数到门/爻的映射公式 — 302° 起点、5.625° 每门、GATE_ORDER 查表
# 修改说明: 实现为独立函数，添加边界处理和类型标注

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


def map_all_activations(planet_positions: dict[str, float]) -> list[dict]:
    """Map all planetary positions to gate/line activations.

    Args:
        planet_positions: Dictionary of {planet_name: ecliptic_longitude}.

    Returns:
        List of activation dicts:
        [{"planet": "sun", "gate": 41, "line": 3, "longitude": 302.5}, ...]
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
        gate, line = longitude_to_gate_line(lon)
        activations.append({
            "planet": planet,
            "gate": gate,
            "line": line,
            "longitude": round(lon, 6),
        })

    return activations

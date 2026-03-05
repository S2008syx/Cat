"""
Human Design Calculator - Ephemeris Layer

Swiss Ephemeris wrapper for planetary position calculations.
This module encapsulates all pyswisseph calls. If the astronomical library
needs to be swapped (e.g. to skyfield), only this file needs to change.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import swisseph as swe

# Use Moshier ephemeris (built-in, no external data files needed)
swe.set_ephe_path(None)  # None = use Moshier

# === Planet constants ===
# Swiss Ephemeris planet IDs
PLANET_IDS: dict[str, int] = {
    "sun":        swe.SUN,        # 0
    "moon":       swe.MOON,       # 1
    "mercury":    swe.MERCURY,    # 2
    "venus":      swe.VENUS,      # 3
    "mars":       swe.MARS,       # 4
    "jupiter":    swe.JUPITER,    # 5
    "saturn":     swe.SATURN,     # 6
    "uranus":     swe.URANUS,     # 7
    "neptune":    swe.NEPTUNE,    # 8
    "pluto":      swe.PLUTO,      # 9
    "north_node": swe.MEAN_NODE,  # 10 (True Node could also be used)
}

# Planets computed via Swiss Ephemeris (11 bodies)
# Earth and South Node are derived, not directly queried
COMPUTED_PLANETS: list[str] = list(PLANET_IDS.keys())

# All 13 celestial bodies used in Human Design
ALL_PLANETS: list[str] = [
    "sun", "earth", "moon", "north_node", "south_node",
    "mercury", "venus", "mars", "jupiter", "saturn",
    "uranus", "neptune", "pluto",
]


def utc_to_julian_day(dt: datetime) -> float:
    """Convert a UTC datetime to Julian Day Number.

    Args:
        dt: UTC datetime object.

    Returns:
        Julian Day Number as float.
    """
    # Ensure we're working with UTC
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)

    jd = swe.julday(
        dt.year, dt.month, dt.day,
        dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    )
    return jd


def julian_day_to_utc(jd: float) -> datetime:
    """Convert a Julian Day Number back to UTC datetime.

    Args:
        jd: Julian Day Number.

    Returns:
        UTC datetime object.
    """
    year, month, day, hour_frac = swe.revjul(jd)
    hour = int(hour_frac)
    minute_frac = (hour_frac - hour) * 60
    minute = int(minute_frac)
    second = int((minute_frac - minute) * 60)
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)


def get_planet_longitude(planet_id: int, jd: float) -> float:
    """Get ecliptic longitude for a planet at a given Julian Day.

    Args:
        planet_id: Swiss Ephemeris planet constant.
        jd: Julian Day Number.

    Returns:
        Ecliptic longitude in degrees (0-360).
    """
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    result, _ = swe.calc_ut(jd, planet_id, flags)
    return result[0]  # longitude


def get_sun_position(jd: float) -> tuple[float, float]:
    """Get Sun's ecliptic longitude and speed at a given Julian Day.

    Args:
        jd: Julian Day Number.

    Returns:
        Tuple of (longitude, speed_in_degrees_per_day).
    """
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    result, _ = swe.calc_ut(jd, swe.SUN, flags)
    return result[0], result[3]  # longitude, longitude_speed


def calculate_planet_positions(jd: float) -> dict[str, float]:
    """Calculate ecliptic longitudes for all 13 celestial bodies.

    Args:
        jd: Julian Day Number for the moment to calculate.

    Returns:
        Dictionary mapping planet name to ecliptic longitude (0-360).
        Includes all 13 bodies: sun, earth, moon, north_node, south_node,
        mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto.
    """
    positions: dict[str, float] = {}

    # Calculate positions for the 11 directly-queried bodies
    for name, planet_id in PLANET_IDS.items():
        positions[name] = get_planet_longitude(planet_id, jd)

    # Derive Earth position: Sun + 180° (opposite point on ecliptic)
    positions["earth"] = (positions["sun"] + 180.0) % 360.0

    # Derive South Node: North Node + 180°
    positions["south_node"] = (positions["north_node"] + 180.0) % 360.0

    return positions


def _shortest_arc(a: float, b: float) -> float:
    """Calculate the shortest arc distance from angle a to angle b.

    Handles the 0°/360° boundary crossing correctly.

    Args:
        a: First angle in degrees (0-360).
        b: Second angle in degrees (0-360).

    Returns:
        Signed shortest arc from a to b, in range (-180, 180].
    """
    diff = (b - a) % 360.0
    if diff > 180.0:
        diff -= 360.0
    return diff


# [SOURCE] 参考: PyHD 开发博客 (https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library)
# 参考内容: 88° 太阳回退算法的 Newton-Raphson 迭代法原理
# 修改说明: 根据博客描述的算法思路，使用 Python + pyswisseph 实现

def calculate_design_jd(birth_jd: float) -> float:
    """Calculate the Design moment (88° Sun regression) using Newton-Raphson.

    In Human Design, the "Design" calculation uses the moment when the Sun
    was at a position 88° behind its birth position. This finds that precise
    moment by iterating.

    Args:
        birth_jd: Julian Day of birth.

    Returns:
        Julian Day of the Design moment (when Sun was 88° earlier).

    Algorithm:
        1. Target longitude = (birth_sun_longitude - 88°) mod 360°
        2. Initial estimate: birth_jd - 88 days (roughly 88° at ~1°/day)
        3. Newton-Raphson iteration using Sun's speed to converge
    """
    # Get Sun position at birth
    birth_sun_lon, _ = get_sun_position(birth_jd)

    # Target: Sun position 88° before birth
    target_lon = (birth_sun_lon - 88.0) % 360.0

    # Initial estimate: ~88 days before birth (Sun moves ~1°/day)
    design_jd = birth_jd - 88.0

    # Newton-Raphson iteration
    for _ in range(50):
        sun_lon, sun_speed = get_sun_position(design_jd)
        diff = _shortest_arc(sun_lon, target_lon)

        if abs(diff) < 0.0001:  # Converged (< 0.36 arcseconds)
            break

        # Adjust estimate: diff degrees / speed degrees_per_day = days to adjust
        design_jd += diff / sun_speed

    return design_jd

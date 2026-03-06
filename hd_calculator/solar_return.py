"""
Human Design Calculator - Solar Return Module

Calculates a Solar Return chart — the complete Human Design chart for the
precise moment each year when the Sun returns to its exact natal longitude.

A Solar Return chart acts as an "annual theme chart" in Human Design:
  - The Sun gate is always the same as the natal chart (same longitude)
  - All other planets (Moon, Mercury, Venus, etc.) are at different positions
  - This produces a different set of activated gates, channels, and centers
  - The resulting Type, Authority, Profile, etc. may differ from the natal chart
  - These differences describe the energetic theme for that year

The Solar Return year runs from one return to the next (~365.25 days).

Usage:
    from hd_calculator.solar_return import calculate_solar_return
    from datetime import datetime, timezone

    # Get the 2026 Solar Return chart
    result = calculate_solar_return(
        birth_utc=datetime(1990, 1, 15, 6, 30, tzinfo=timezone.utc),
        year=2026,
        latitude=31.2304,
        longitude=121.4737,
    )
    print(result["return_utc"])      # Exact moment of Solar Return
    print(result["chart"].type)      # Type for this year
    print(result["chart"].profile)   # Profile for this year
"""

from __future__ import annotations

from datetime import datetime, timezone

from .ephemeris import (
    utc_to_julian_day,
    julian_day_to_utc,
    get_sun_position,
    _shortest_arc,
)


def find_solar_return_jd(birth_jd: float, year: int) -> float:
    """Find the Julian Day when the Sun returns to its natal longitude in a given year.

    Uses Newton-Raphson iteration (same approach as the 88° regression
    algorithm in ephemeris.py) to find the precise moment when:
        Sun_longitude(return_jd) == Sun_longitude(birth_jd)

    The Sun completes one full ecliptic revolution in ~365.2422 days
    (tropical year). The initial estimate places us near the birthday
    in the target year, then Newton-Raphson converges to sub-arcsecond
    precision in 3-5 iterations.

    Args:
        birth_jd: Julian Day of birth.
        year: The calendar year for which to find the Solar Return.

    Returns:
        Julian Day of the Solar Return moment.

    Raises:
        RuntimeError: If Newton-Raphson fails to converge within 50 iterations.
    """
    # Target: the natal Sun longitude
    natal_sun_lon, _ = get_sun_position(birth_jd)

    # Initial estimate: same calendar date in target year.
    # The tropical year is ~365.2422 days.
    birth_utc = julian_day_to_utc(birth_jd)
    years_diff = year - birth_utc.year
    estimate_jd = birth_jd + years_diff * 365.2422

    # Newton-Raphson iteration
    for iteration in range(50):
        sun_lon, sun_speed = get_sun_position(estimate_jd)
        diff = _shortest_arc(sun_lon, natal_sun_lon)

        if abs(diff) < 0.0001:  # Converged (< 0.36 arcseconds)
            return estimate_jd

        # Adjust: degrees_remaining / degrees_per_day = days_to_adjust
        estimate_jd += diff / sun_speed

    raise RuntimeError(
        f"Solar Return Newton-Raphson did not converge for year {year} "
        f"after 50 iterations (last diff: {diff:.6f}°)"
    )


def calculate_solar_return(
    birth_utc: datetime,
    year: int,
    latitude: float,
    longitude: float,
) -> dict:
    """Calculate a complete Solar Return chart for a given year.

    This function:
      1. Finds the precise moment the Sun returns to its natal longitude
      2. Computes a full Human Design chart for that moment
      3. Returns both the chart and metadata

    The returned chart is a standard CalculatorOutput — it has Type,
    Authority, Profile, Variables, etc. just like a natal chart. The
    differences between the natal chart and the Solar Return chart
    reveal the energetic themes for that year.

    Args:
        birth_utc: UTC birth datetime.
        year: The calendar year for the Solar Return.
            Must be >= birth year. For the birth year itself,
            returns approximately the natal chart.
        latitude: Birth place latitude (passed through to calculate()).
        longitude: Birth place longitude (passed through to calculate()).

    Returns:
        A dictionary with:
            "return_utc" (datetime): Exact UTC moment of the Solar Return.
            "return_jd" (float): Julian Day of the Solar Return moment.
            "year" (int): The requested year.
            "natal_sun_longitude" (float): The natal Sun longitude (target).
            "chart" (CalculatorOutput): Full HD chart for the return moment.
    """
    # Lazy import to avoid circular dependency
    # (calculate imports solar_return, solar_return uses calculate)
    from . import calculate as _calculate

    birth_jd = utc_to_julian_day(birth_utc)
    natal_sun_lon, _ = get_sun_position(birth_jd)

    # Find the precise Solar Return moment
    return_jd = find_solar_return_jd(birth_jd, year)
    return_utc = julian_day_to_utc(return_jd)

    # Calculate a full chart for the Solar Return moment
    chart = _calculate(
        birth_utc=return_utc,
        latitude=latitude,
        longitude=longitude,
    )

    return {
        "return_utc": return_utc,
        "return_jd": return_jd,
        "year": year,
        "natal_sun_longitude": round(natal_sun_lon, 6),
        "chart": chart,
    }

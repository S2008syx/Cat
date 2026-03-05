"""
Human Design Calculator Module

Pure computation engine that takes UTC birth time + coordinates
and outputs structured Human Design parameters.

This is Part 3 of a 4-part system:
  [Part 2] Input Processing → [Part 3] Calculator (this module) → [Part 4] Interpreter

Usage:
    from hd_calculator import calculate
    from datetime import datetime, timezone

    result = calculate(
        birth_utc=datetime(1990, 1, 15, 6, 30, tzinfo=timezone.utc),
        latitude=31.2304,
        longitude=121.4737,
    )
    print(result.type)       # "Generator"
    print(result.profile)    # "4/6"
    print(result.authority)  # "Emotional"
"""

from __future__ import annotations

from datetime import datetime

from .models import CalculatorOutput
from .ephemeris import (
    utc_to_julian_day,
    julian_day_to_utc,
    calculate_planet_positions,
    calculate_design_jd,
)
from .gate_mapping import map_all_activations
from .chart_properties import (
    find_active_channels,
    find_defined_centers,
    determine_definition_type,
    determine_type,
    determine_strategy,
    determine_authority,
    determine_profile,
    determine_incarnation_cross,
)


def calculate(birth_utc: datetime, latitude: float, longitude: float) -> CalculatorOutput:
    """Calculate a complete Human Design chart.

    This is the ONLY public interface of this module.
    Part 2 calls this function, Part 4 consumes its return value.

    Internally runs a 5-layer pipeline:
      1. Time → Planet positions (Swiss Ephemeris)
      2. Positions → Gates and Lines (longitude mapping)
      3. Gates → Channels + Centers (pattern matching)
      4. Centers → Definition type (BFS connected components)
      5. Combined → Type, Strategy, Authority, Profile, Cross

    Args:
        birth_utc: UTC birth datetime (converted by Part 2).
        latitude: Birth place latitude. Reserved for future use.
        longitude: Birth place longitude. Reserved for future use.

    Returns:
        CalculatorOutput with all computed Human Design parameters.
    """
    # === Layer 1: Time → Planet Positions ===
    birth_jd = utc_to_julian_day(birth_utc)

    # Personality (conscious) planets at birth moment
    personality_positions = calculate_planet_positions(birth_jd)

    # Design (unconscious) planets at 88° Sun regression moment
    design_jd = calculate_design_jd(birth_jd)
    design_positions = calculate_planet_positions(design_jd)
    design_utc = julian_day_to_utc(design_jd)

    # === Layer 2: Positions → Gates and Lines ===
    personality_activations = map_all_activations(personality_positions)
    design_activations = map_all_activations(design_positions)

    # Collect all activated gates (deduplicated)
    all_active_gates: set[int] = set()
    for act in personality_activations:
        all_active_gates.add(act["gate"])
    for act in design_activations:
        all_active_gates.add(act["gate"])

    # === Layer 3: Gates → Channels + Centers ===
    active_channels = find_active_channels(all_active_gates)
    defined_centers, undefined_centers = find_defined_centers(active_channels)

    # === Layer 4: Definition Type ===
    definition_type, split_type = determine_definition_type(
        defined_centers, active_channels
    )

    # === Layer 5: Type, Strategy, Authority, Profile, Cross ===
    hd_type = determine_type(defined_centers, active_channels)
    strategy = determine_strategy(hd_type)
    authority = determine_authority(defined_centers, active_channels, hd_type)

    # Profile: personality Sun line / design Sun line
    p_sun = next(a for a in personality_activations if a["planet"] == "sun")
    d_sun = next(a for a in design_activations if a["planet"] == "sun")
    profile = determine_profile(p_sun["line"], d_sun["line"])

    # Incarnation Cross
    p_earth = next(a for a in personality_activations if a["planet"] == "earth")
    d_earth = next(a for a in design_activations if a["planet"] == "earth")
    cross = determine_incarnation_cross(
        p_sun["gate"], p_earth["gate"],
        d_sun["gate"], d_earth["gate"],
        profile,
    )

    # === Build output ===
    return CalculatorOutput(
        type=hd_type,
        strategy=strategy,
        authority=authority,
        profile=profile,
        definition_type=definition_type,
        split_type=split_type,
        incarnation_cross_type=cross["type"],
        incarnation_cross_gates=cross["gates"],
        defined_centers=defined_centers,
        undefined_centers=undefined_centers,
        active_channels=[
            {
                "gate_a": ch["gate_a"],
                "gate_b": ch["gate_b"],
                "center_a": ch["center_a"],
                "center_b": ch["center_b"],
            }
            for ch in active_channels
        ],
        personality_activations=[
            {
                "planet": a["planet"],
                "gate": a["gate"],
                "line": a["line"],
                "longitude": a["longitude"],
            }
            for a in personality_activations
        ],
        design_activations=[
            {
                "planet": a["planet"],
                "gate": a["gate"],
                "line": a["line"],
                "longitude": a["longitude"],
            }
            for a in design_activations
        ],
        design_utc=design_utc,
        all_active_gates=sorted(all_active_gates),
    )

"""
Human Design Calculator - Transit (Planetary Transit) Module

Calculates the current (or any given moment's) planetary activations
and overlays them onto a natal chart to show which gates, channels,
and centers are temporarily activated by transiting planets.

Transit charts are the "daily weather" of Human Design — they show
collective energy themes that affect everyone, and when overlaid on
a personal chart they reveal which dormant gates/channels "wake up."

Usage:
    from hd_calculator.transit import calculate_transit
    from datetime import datetime, timezone

    # Current planetary activations (no natal chart needed)
    transit = calculate_transit(
        transit_utc=datetime(2026, 3, 6, 12, 0, tzinfo=timezone.utc),
    )
    print(transit["activations"])   # 13 planetary gate/line activations
    print(transit["active_gates"])  # Which gates are lit up right now

    # Overlay on a natal chart to find temporarily completed channels
    from hd_calculator import calculate
    natal = calculate(birth_utc=..., latitude=..., longitude=...)
    transit = calculate_transit(
        transit_utc=datetime.now(timezone.utc),
        natal_gates=set(natal.all_active_gates),
    )
    print(transit["completed_channels"])  # Channels completed by transit
"""

from __future__ import annotations

from datetime import datetime

from .ephemeris import utc_to_julian_day, calculate_planet_positions
from .gate_mapping import map_all_activations
from .chart_properties import find_active_channels, find_defined_centers
from .data.channels import CHANNELS


def calculate_transit(
    transit_utc: datetime,
    natal_gates: set[int] | None = None,
) -> dict:
    """Calculate planetary transit activations for a given moment.

    This function computes which gates are activated by the current
    planetary positions. Optionally, when a set of natal gates is
    provided, it also identifies channels that are *completed* by
    the transit (one gate from natal + one gate from transit).

    Args:
        transit_utc: The UTC datetime for the transit moment.
            Use ``datetime.now(timezone.utc)`` for the current moment.
        natal_gates: Optional set of gate numbers from a natal chart.
            When provided, the function computes overlay analysis:
            which channels and centers become temporarily active.

    Returns:
        A dictionary with the following keys:

        Always present:
            "transit_utc" (datetime): The transit moment used.
            "activations" (list[dict]): 13 planetary activations, each:
                {"planet", "gate", "line", "color", "tone", "base", "longitude"}
            "active_gates" (list[int]): Sorted list of gates activated by transit.
            "transit_channels" (list[dict]): Channels formed by transit planets alone.
            "transit_defined_centers" (list[str]): Centers defined by transit alone.

        Present only when ``natal_gates`` is provided:
            "completed_channels" (list[dict]): Channels where one gate comes
                from the natal chart and the other from transit. Each dict:
                {"gate_a", "gate_b", "center_a", "center_b", "natal_gate", "transit_gate"}
            "overlay_defined_centers" (list[str]): All centers defined when
                natal + transit gates are combined.
            "overlay_undefined_centers" (list[str]): Centers still undefined
                after combining natal + transit.
    """
    # --- Compute transit planetary positions ---
    transit_jd = utc_to_julian_day(transit_utc)
    positions = calculate_planet_positions(transit_jd)
    activations = map_all_activations(positions)

    transit_gates: set[int] = {a["gate"] for a in activations}

    # Channels and centers formed by transit planets alone
    transit_channels = find_active_channels(transit_gates)
    transit_defined, _ = find_defined_centers(transit_channels)

    result: dict = {
        "transit_utc": transit_utc,
        "activations": activations,
        "active_gates": sorted(transit_gates),
        "transit_channels": transit_channels,
        "transit_defined_centers": transit_defined,
    }

    # --- Overlay analysis (natal + transit) ---
    if natal_gates is not None:
        combined_gates = natal_gates | transit_gates

        # Find channels completed by combining natal and transit
        completed_channels: list[dict] = []
        for (gate_a, gate_b), (center_a, center_b) in CHANNELS.items():
            # Channel requires both gates. Find channels where one gate
            # is natal-only and the other is transit (or vice versa).
            a_in_natal = gate_a in natal_gates
            b_in_natal = gate_b in natal_gates
            a_in_transit = gate_a in transit_gates
            b_in_transit = gate_b in transit_gates

            # Both gates present in combined set?
            if not (gate_a in combined_gates and gate_b in combined_gates):
                continue

            # Is this channel ONLY completed because of the transit?
            # (i.e., it was NOT already complete in the natal chart alone)
            natal_complete = a_in_natal and b_in_natal
            if natal_complete:
                continue  # Already defined natally, not a transit effect

            # At least one gate must come from transit
            if a_in_transit and (b_in_natal or b_in_transit):
                completed_channels.append({
                    "gate_a": gate_a,
                    "gate_b": gate_b,
                    "center_a": center_a,
                    "center_b": center_b,
                    "natal_gate": gate_a if a_in_natal else gate_b,
                    "transit_gate": gate_a if (a_in_transit and not a_in_natal) else gate_b,
                })

        # Full overlay: all channels from combined gates
        overlay_channels = find_active_channels(combined_gates)
        overlay_defined, overlay_undefined = find_defined_centers(overlay_channels)

        result["completed_channels"] = completed_channels
        result["overlay_defined_centers"] = overlay_defined
        result["overlay_undefined_centers"] = overlay_undefined

    return result

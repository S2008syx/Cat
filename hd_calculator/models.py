"""
Human Design Calculator - Data Models

Input/output data structures for the calculation pipeline.
These models define the contract between Part 2 (input processing) and Part 4 (interpretation).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CalculatorInput:
    """Input from Part 2 (upstream).

    Attributes:
        birth_utc: UTC birth time, already converted by upstream.
        latitude: Birth place latitude (e.g. 31.2304 for Shanghai).
        longitude: Birth place longitude (e.g. 121.4737 for Shanghai).

    Note:
        latitude/longitude are not used in current HD calculations
        (HD only depends on UTC time), but are reserved for future
        Local Sidereal Time calculations and interface completeness.
    """

    birth_utc: datetime
    latitude: float
    longitude: float


@dataclass
class Activation:
    """A single planetary activation (gate/line/color/tone/base assignment).

    Attributes:
        planet: Planet name (e.g. "sun", "moon", "mercury").
        gate: Gate number (1-64).
        line: Line number (1-6).
        color: Color number (1-6). Subdivides the line arc into 6 equal parts.
        tone: Tone number (1-6). Subdivides the color arc into 6 equal parts.
        base: Base number (1-5). Subdivides the tone arc into 5 equal parts.
        longitude: Ecliptic longitude in degrees (0-360).
    """

    planet: str
    gate: int
    line: int
    color: int
    tone: int
    base: int
    longitude: float


@dataclass
class Channel:
    """An active (defined) channel.

    Attributes:
        gate_a: First gate number.
        gate_b: Second gate number.
        center_a: Center connected by gate_a.
        center_b: Center connected by gate_b.
    """

    gate_a: int
    gate_b: int
    center_a: str
    center_b: str


@dataclass
class CalculatorOutput:
    """Output to Part 4 (downstream).

    Contains all computed Human Design parameters.
    Part 4's interpreter only needs this output to work.
    """

    # === Basic attributes ===
    type: str
    """One of: "Generator", "Manifesting Generator", "Manifestor", "Projector", "Reflector"."""

    strategy: str
    """One of: "To Respond", "To Inform", "To Wait for Invitation", "To Wait a Lunar Cycle"."""

    authority: str
    """One of: "Emotional", "Sacral", "Splenic", "Ego Manifested",
    "Ego Projected", "Self-Projected", "Lunar", "Mental"."""

    profile: str
    """Format "X/Y", e.g. "1/3", "4/6"."""

    definition_type: str
    """One of: "None", "Single", "Split", "Triple Split", "Quadruple Split"."""

    split_type: Optional[str]
    """Only when definition_type == "Split": "Small" or "Large". Otherwise None."""

    # === Incarnation Cross ===
    incarnation_cross_type: str
    """One of: "Right Angle", "Juxtaposition", "Left Angle"."""

    incarnation_cross_gates: list[int]
    """[personality_sun_gate, personality_earth_gate, design_sun_gate, design_earth_gate]."""

    # === Energy Centers ===
    defined_centers: list[str]
    """List of defined center names, e.g. ["sacral", "solar_plexus"]."""

    undefined_centers: list[str]
    """List of undefined center names, e.g. ["head", "ajna"]."""

    # === Channels ===
    active_channels: list[dict]
    """List of active channels: [{"gate_a": 6, "gate_b": 59,
    "center_a": "solar_plexus", "center_b": "sacral"}, ...]."""

    # === Variables / Arrows ===
    variables: dict
    """Four arrows derived from Color values of Sun and North Node activations.
    {
        "digestion":   {"arrow": "Left"|"Right", "color": int, "tone": int},
        "environment": {"arrow": "Left"|"Right", "color": int, "tone": int},
        "motivation":  {"arrow": "Left"|"Right", "color": int, "tone": int},
        "perspective": {"arrow": "Left"|"Right", "color": int, "tone": int},
    }"""

    # === Gates (full 26 activations) ===
    personality_activations: list[dict]
    """Personality (conscious) activations:
    [{"planet": "sun", "gate": 40, "line": 4, "color": 2, "tone": 5,
      "base": 1, "longitude": 123.456}, ...]."""

    design_activations: list[dict]
    """Design (unconscious) activations: same structure as personality."""

    # === Metadata (for debugging and validation) ===
    design_utc: datetime
    """Computed design moment (88° sun regression)."""

    all_active_gates: list[int]
    """Deduplicated list of all activated gate numbers."""

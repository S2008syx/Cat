"""
Bodygraph layout constants for front-end rendering.

Coordinates are normalized (0-1) based on standard HD Bodygraph proportions.
Reference: hdkit (https://github.com/jdempcy/hdkit) SVG structure.

Origin (0,0) = top-left; (1,1) = bottom-right.
"""

# 9 center positions and shapes
# Normalized from hdkit empty-bodygraph.svg (1800x2400 viewBox)
# Shapes match hdkit SVG: triangle (Head up, Ajna down, Heart down,
#   Solar Plexus left, Spleen right), square (Throat, Sacral, Root), diamond (G)
CENTER_LAYOUT: dict[str, dict] = {
    "head": {
        "position": {"x": 0.48, "y": 0.09},
        "shape": "triangle"
    },
    "ajna": {
        "position": {"x": 0.48, "y": 0.22},
        "shape": "triangle"
    },
    "throat": {
        "position": {"x": 0.48, "y": 0.37},
        "shape": "square"
    },
    "g": {
        "position": {"x": 0.48, "y": 0.53},
        "shape": "diamond"
    },
    "heart": {
        "position": {"x": 0.61, "y": 0.61},
        "shape": "triangle"
    },
    "sacral": {
        "position": {"x": 0.48, "y": 0.81},
        "shape": "square"
    },
    "solar_plexus": {
        "position": {"x": 0.75, "y": 0.77},
        "shape": "triangle"
    },
    "spleen": {
        "position": {"x": 0.18, "y": 0.77},
        "shape": "triangle"
    },
    "root": {
        "position": {"x": 0.47, "y": 0.95},
        "shape": "square"
    },
}

# Gate-to-Center mapping (all 64 gates)
# This duplicates hd_calculator.data.centers.GATE_TO_CENTER but is kept here
# so hd_converters can be self-contained for layout purposes.
GATE_TO_CENTER: dict[int, str] = {
    # Head (3 gates)
    61: "head", 63: "head", 64: "head",
    # Ajna (6 gates)
    4: "ajna", 11: "ajna", 17: "ajna", 24: "ajna", 43: "ajna", 47: "ajna",
    # Throat (11 gates)
    8: "throat", 12: "throat", 16: "throat", 20: "throat", 23: "throat",
    31: "throat", 33: "throat", 35: "throat", 45: "throat", 56: "throat", 62: "throat",
    # G Center (8 gates)
    1: "g", 2: "g", 7: "g", 10: "g", 13: "g", 15: "g", 25: "g", 46: "g",
    # Heart / Will / Ego (4 gates)
    21: "heart", 26: "heart", 40: "heart", 51: "heart",
    # Sacral (9 gates)
    3: "sacral", 5: "sacral", 9: "sacral", 14: "sacral", 27: "sacral",
    29: "sacral", 34: "sacral", 42: "sacral", 59: "sacral",
    # Solar Plexus (7 gates)
    6: "solar_plexus", 22: "solar_plexus", 30: "solar_plexus",
    36: "solar_plexus", 37: "solar_plexus", 49: "solar_plexus", 55: "solar_plexus",
    # Spleen (7 gates)
    18: "spleen", 28: "spleen", 32: "spleen", 44: "spleen",
    48: "spleen", 50: "spleen", 57: "spleen",
    # Root (9 gates)
    19: "root", 38: "root", 39: "root", 41: "root", 52: "root",
    53: "root", 54: "root", 58: "root", 60: "root",
}

assert len(GATE_TO_CENTER) == 64, f"Expected 64 gate mappings, got {len(GATE_TO_CENTER)}"
assert len(CENTER_LAYOUT) == 9, f"Expected 9 centers, got {len(CENTER_LAYOUT)}"

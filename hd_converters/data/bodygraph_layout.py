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

# ---------------------------------------------------------------------------
# Rendering-specific layout data (absolute px for 760×880 SVG canvas)
# ---------------------------------------------------------------------------

# Absolute center positions for SVG rendering
CENTER_RENDER_POS: dict[str, tuple[int, int]] = {
    "head":          (380, 90),
    "ajna":          (380, 168),
    "throat":        (380, 260),
    "g":             (380, 362),
    "heart":         (472, 400),
    "sacral":        (380, 498),
    "solar_plexus":  (510, 472),
    "spleen":        (250, 472),
    "root":          (380, 600),
}

# Center shape types with orientation
CENTER_RENDER_SHAPES: dict[str, str] = {
    "head":          "triangle_up",
    "ajna":          "triangle_down",
    "throat":        "square",
    "g":             "diamond",
    "heart":         "triangle_down",
    "sacral":        "square",
    "solar_plexus":  "triangle_right",
    "spleen":        "triangle_left",
    "root":          "square",
}

# Chinese labels for centers
CENTER_RENDER_LABELS: dict[str, str] = {
    "head": "头脑", "ajna": "逻辑", "throat": "喉咙", "g": "G",
    "heart": "意志力", "sacral": "骶骨", "solar_plexus": "情绪",
    "spleen": "直觉", "root": "根",
}

# ---------------------------------------------------------------------------
# 64 Gate positions (absolute px)
# Each gate is positioned near its center, offset toward its channel partner.
# Multi-channel gates (20, 10, 34, 57) have a single position serving all channels.
# Reference: hdkit standard bodygraph proportions.
# ---------------------------------------------------------------------------
GATE_POSITIONS: dict[int, tuple[int, int]] = {
    # === Head (380, 90) — 3 gates, all connect down to Ajna ===
    64: (356, 78),
    61: (380, 74),
    63: (404, 78),

    # === Ajna (380, 168) — 6 gates ===
    # Upper side (connect to Head)
    47: (356, 148),
    24: (380, 144),
    4:  (404, 148),
    # Lower side (connect to Throat)
    17: (356, 188),
    43: (380, 192),
    11: (404, 188),

    # === Throat (380, 260) — 11 gates ===
    # Upper (from Ajna)
    62: (356, 238),
    23: (380, 234),
    56: (404, 238),
    # Left (to Spleen)
    16: (318, 264),
    20: (336, 276),   # Integration gate — connects to 10, 34, 57
    # Center-lower (to G)
    8:  (358, 282),
    31: (380, 286),
    33: (402, 282),
    # Right (to Heart / Solar Plexus)
    45: (422, 260),
    12: (434, 270),
    35: (444, 256),

    # === G Center (380, 362) — 8 gates ===
    # Upper (to Throat)
    1:  (362, 342),
    7:  (380, 338),
    13: (398, 342),
    # Left (Integration)
    10: (346, 366),    # Integration gate — connects to 20, 34, 57
    # Right (to Heart)
    25: (412, 358),
    # Lower (to Sacral)
    15: (362, 384),
    2:  (380, 388),
    46: (398, 384),

    # === Heart (472, 400) — 4 gates ===
    21: (450, 386),    # to 45 (Throat)
    51: (450, 398),    # to 25 (G)
    26: (452, 416),    # to 44 (Spleen)
    40: (496, 406),    # to 37 (Solar Plexus)

    # === Sacral (380, 498) — 9 gates ===
    # Upper (to G)
    5:  (356, 478),
    14: (374, 476),
    29: (400, 478),
    # Left-upper (Integration)
    34: (330, 490),    # Integration gate — connects to 10, 20, 57
    # Sides
    27: (344, 508),    # to 50 (Spleen)
    59: (412, 492),    # to 6 (Solar Plexus)
    # Lower (to Root)
    42: (360, 520),
    3:  (380, 522),
    9:  (400, 520),

    # === Solar Plexus (510, 472) — 7 gates ===
    36: (480, 450),    # to 35 (Throat)
    22: (482, 462),    # to 12 (Throat)
    37: (516, 454),    # to 40 (Heart)
    6:  (488, 478),    # to 59 (Sacral)
    49: (530, 490),    # to 19 (Root)
    55: (522, 496),    # to 39 (Root)
    30: (514, 492),    # to 41 (Root)

    # === Spleen (250, 472) — 7 gates ===
    57: (274, 456),    # Integration gate — connects to 20, 10, 34
    48: (272, 464),    # to 16 (Throat)
    44: (272, 480),    # to 26 (Heart)
    50: (260, 490),    # to 27 (Sacral)
    18: (254, 500),    # to 58 (Root)
    28: (242, 494),    # to 38 (Root)
    32: (236, 484),    # to 54 (Root)

    # === Root (380, 600) — 9 gates ===
    # Upper (to Sacral)
    53: (360, 582),
    60: (380, 578),
    52: (400, 582),
    # Right (to Solar Plexus)
    19: (416, 596),
    39: (428, 602),
    41: (408, 610),
    # Left (to Spleen)
    58: (344, 596),
    38: (332, 602),
    54: (352, 610),
}

assert len(GATE_POSITIONS) == 64, f"Expected 64 gate positions, got {len(GATE_POSITIONS)}"

# ---------------------------------------------------------------------------
# All 36 channels as (gate_a, gate_b) tuples.
# Matches hd_calculator.data.channels.CHANNELS keys.
# ---------------------------------------------------------------------------
ALL_CHANNELS: list[tuple[int, int]] = [
    # Head ↔ Ajna
    (64, 47), (61, 24), (63, 4),
    # Ajna ↔ Throat
    (17, 62), (43, 23), (11, 56),
    # Throat ↔ G
    (8, 1), (31, 7), (33, 13), (20, 10),
    # Throat ↔ Heart
    (45, 21),
    # Throat ↔ Solar Plexus
    (35, 36), (12, 22),
    # Throat ↔ Sacral
    (20, 34),
    # Throat ↔ Spleen
    (20, 57), (16, 48),
    # G ↔ Sacral
    (15, 5), (2, 14), (46, 29), (10, 34),
    # G ↔ Spleen
    (10, 57),
    # G ↔ Heart
    (25, 51),
    # Heart ↔ Spleen
    (26, 44),
    # Heart ↔ Solar Plexus
    (40, 37),
    # Sacral ↔ Solar Plexus
    (59, 6),
    # Sacral ↔ Spleen
    (27, 50), (34, 57),
    # Sacral ↔ Root
    (42, 53), (3, 60), (9, 52),
    # Solar Plexus ↔ Root
    (49, 19), (55, 39), (30, 41),
    # Spleen ↔ Root
    (18, 58), (28, 38), (32, 54),
]

assert len(ALL_CHANNELS) == 36, f"Expected 36 channels, got {len(ALL_CHANNELS)}"

# ---------------------------------------------------------------------------
# Channel curve overrides — channels that need bezier curves to avoid overlap.
# Format: (gate_a, gate_b) → list of quadratic bezier control points [(cx, cy)].
# Channels not listed here are drawn as straight lines.
# ---------------------------------------------------------------------------
CHANNEL_CURVES: dict[tuple[int, int], list[tuple[int, int]]] = {
    # Heart → Spleen (26-44): crosses entire bodygraph, curve below G center
    (26, 44): [(380, 452)],
    # Throat → Sacral (20-34): long integration channel, slight left curve
    (20, 34): [(310, 388)],
    # Throat → Spleen (20-57): integration channel, curve left
    (20, 57): [(280, 360)],
    # G → Spleen (10-57): integration channel
    (10, 57): [(280, 420)],
}

# ---------------------------------------------------------------------------
# Human silhouette SVG path (simple line art, centered at x=380)
# ---------------------------------------------------------------------------
SILHOUETTE_PATH = (
    "M 380,50 "
    "C 396,50 408,62 408,78 C 408,94 396,106 380,106 "
    "C 364,106 352,94 352,78 C 352,62 364,50 380,50 Z "  # head circle
    "M 372,106 L 370,124 L 328,148 C 316,154 310,166 310,180 "
    "L 308,310 C 306,340 310,370 316,400 "
    "L 322,460 L 320,520 L 318,590 C 316,610 322,630 336,640 "
    "L 360,650 "  # left side
    "M 388,106 L 390,124 L 432,148 C 444,154 450,166 450,180 "
    "L 452,310 C 454,340 450,370 444,400 "
    "L 438,460 L 440,520 L 442,590 C 444,610 438,630 424,640 "
    "L 400,650"  # right side
)

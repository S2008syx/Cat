"""
Human Design Center Definitions

The 9 energy centers and their associated gates.
"""

# [SOURCE] 参考: SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign),
#   hdkit (https://github.com/jdempcy/hdkit)
# 参考内容: 中心定义 (Center definitions) — 9 centers with their gate assignments
# 修改说明: 整理为 Python 字典格式

# All 9 centers and the gates they contain
CENTERS: dict[str, set[int]] = {
    "head":          {64, 61, 63},
    "ajna":          {47, 24, 4, 17, 43, 11},
    "throat":        {62, 23, 56, 8, 31, 35, 45, 33, 20, 16, 12},
    "g":             {1, 7, 13, 25, 46, 2, 15, 10},
    "heart":         {21, 51, 26, 40},
    "sacral":        {5, 14, 29, 34, 27, 42, 3, 9, 59},
    "solar_plexus":  {36, 6, 37, 49, 55, 30, 22},
    "spleen":        {57, 44, 50, 48, 18, 28, 32},
    "root":          {53, 60, 52, 19, 39, 41, 58, 38, 54},
}

ALL_CENTER_NAMES: list[str] = list(CENTERS.keys())

# Motor centers (centers that generate energy)
MOTOR_CENTERS: set[str] = {"root", "sacral", "solar_plexus", "heart"}

# Verify all 64 gates are accounted for
_all_gates = set()
for gates in CENTERS.values():
    _all_gates |= gates
assert len(_all_gates) == 64, f"Expected 64 gates across all centers, got {len(_all_gates)}"
assert _all_gates == set(range(1, 65)), "Gates must be numbered 1-64"

# Build reverse lookup: gate → center
GATE_TO_CENTER: dict[int, str] = {}
for center_name, gates in CENTERS.items():
    for gate in gates:
        GATE_TO_CENTER[gate] = center_name

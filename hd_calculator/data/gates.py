"""
Human Design Gate Order Table

The 64 gates arranged in their sequence around the Human Design mandala (Rave wheel).
Starting from Gate 41 at ecliptic longitude 302° (Aquarius 2°), going clockwise.

Each gate occupies 5.625° of the ecliptic (360° / 64 = 5.625°).
Each line within a gate occupies 0.9375° (5.625° / 6 = 0.9375°).
"""

# [SOURCE] 参考: hdkit (https://github.com/jdempcy/hdkit),
#   SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign),
#   humandesign_api (https://github.com/dturkuler/humandesign_api),
#   human_design_engine (https://github.com/MicFell/human_design_engine)
# 参考内容: 门序表 (Gate Order) — 64 gates in mandala sequence
# 修改说明: 从多个项目交叉验证后整理为 Python 列表，起点为 Gate 41 at 302°

GATE_ORDER: list[int] = [
    41, 19, 13, 49, 30, 55, 37, 63,   # 302.000° - 347.000°
    22, 36, 25, 17, 21, 51, 42, 3,    # 347.000° - 32.000° (wraps around 0°)
    27, 24, 2, 23, 8, 20, 16, 35,     # ...
    45, 12, 15, 52, 39, 53, 62, 56,
    31, 33, 7, 4, 29, 59, 40, 64,
    47, 6, 46, 18, 48, 57, 32, 50,
    28, 44, 1, 43, 14, 34, 9, 5,
    26, 11, 10, 58, 38, 54, 61, 60,
]

# Starting longitude for the gate sequence (Gate 41 starts at 302°)
GATE_START_LONGITUDE: float = 302.0

# Degrees per gate
DEGREES_PER_GATE: float = 5.625

# Degrees per line (6 lines per gate)
DEGREES_PER_LINE: float = 0.9375

assert len(GATE_ORDER) == 64, f"Expected 64 gates, got {len(GATE_ORDER)}"
assert len(set(GATE_ORDER)) == 64, "Duplicate gate numbers found"
assert all(1 <= g <= 64 for g in GATE_ORDER), "Gate numbers must be 1-64"

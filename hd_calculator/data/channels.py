"""
Human Design Channel Definitions

All 36 channels connecting the 9 energy centers.
Each channel is defined by a pair of gates and the two centers they connect.

The 9 centers: head, ajna, throat, g, heart, sacral, solar_plexus, spleen, root
"""

# [SOURCE] 参考: SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign),
#   hdkit (https://github.com/jdempcy/hdkit),
#   MCP_Human_design (https://github.com/dvvolkovv/MCP_Human_design)
# 参考内容: 通道表 (Channel definitions) — 36 channels with gate pairs and center connections
# 修改说明: 从多个项目交叉验证后整理为 Python 字典格式

# Format: (gate_a, gate_b): ("center_of_gate_a", "center_of_gate_b")
CHANNELS: dict[tuple[int, int], tuple[str, str]] = {
    # === Head ↔ Ajna (3 channels) ===
    (64, 47): ("head", "ajna"),
    (61, 24): ("head", "ajna"),
    (63, 4):  ("head", "ajna"),

    # === Ajna ↔ Throat (3 channels) ===
    (17, 62): ("ajna", "throat"),
    (43, 23): ("ajna", "throat"),
    (11, 56): ("ajna", "throat"),

    # === Throat ↔ G Center (4 channels) ===
    (8, 1):   ("throat", "g"),
    (31, 7):  ("throat", "g"),
    (33, 13): ("throat", "g"),
    (20, 10): ("throat", "g"),

    # === Throat ↔ Heart/Ego (1 channel) ===
    (45, 21): ("throat", "heart"),

    # === Throat ↔ Solar Plexus (2 channels) ===
    (35, 36): ("throat", "solar_plexus"),
    (12, 22): ("throat", "solar_plexus"),

    # === Throat ↔ Sacral (1 channel) ===
    (20, 34): ("throat", "sacral"),

    # === Throat ↔ Spleen (2 channels) ===
    (20, 57): ("throat", "spleen"),
    (16, 48): ("throat", "spleen"),

    # === G Center ↔ Sacral (4 channels) ===
    (15, 5):  ("g", "sacral"),
    (2, 14):  ("g", "sacral"),
    (46, 29): ("g", "sacral"),
    (10, 34): ("g", "sacral"),

    # === G Center ↔ Spleen (1 channel) ===
    (10, 57): ("g", "spleen"),

    # === G Center ↔ Heart/Ego (1 channel) ===
    (25, 51): ("g", "heart"),

    # === Heart/Ego ↔ Spleen (1 channel) ===
    (26, 44): ("heart", "spleen"),

    # === Heart/Ego ↔ Solar Plexus (1 channel) ===
    (40, 37): ("heart", "solar_plexus"),

    # === Sacral ↔ Solar Plexus (1 channel) ===
    (59, 6):  ("sacral", "solar_plexus"),

    # === Sacral ↔ Spleen (2 channels) ===
    (27, 50): ("sacral", "spleen"),
    (34, 57): ("sacral", "spleen"),

    # === Sacral ↔ Root (3 channels) ===
    (42, 53): ("sacral", "root"),
    (3, 60):  ("sacral", "root"),
    (9, 52):  ("sacral", "root"),

    # === Solar Plexus ↔ Root (3 channels) ===
    (49, 19): ("solar_plexus", "root"),
    (55, 39): ("solar_plexus", "root"),
    (30, 41): ("solar_plexus", "root"),

    # === Spleen ↔ Root (3 channels) ===
    (18, 58): ("spleen", "root"),
    (28, 38): ("spleen", "root"),
    (32, 54): ("spleen", "root"),
}

assert len(CHANNELS) == 36, f"Expected 36 channels, got {len(CHANNELS)}"

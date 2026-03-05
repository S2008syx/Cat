"""
36 Human Design Channels — names, centers, and themes.

Key is (gate_a, gate_b) matching hd_calculator.data.channels order.
"""

CHANNEL_DATA: dict[tuple[int, int], dict] = {
    # === Head ↔ Ajna ===
    (64, 47): {
        "gates": [64, 47], "name_zh": "抽象之通道", "name_en": "Channel of Abstraction",
        "centers": ["head", "ajna"], "theme": "心智活动与过程——从困惑到领悟"
    },
    (61, 24): {
        "gates": [61, 24], "name_zh": "觉知之通道", "name_en": "Channel of Awareness",
        "centers": ["head", "ajna"], "theme": "思考者——从神秘到合理化"
    },
    (63, 4): {
        "gates": [63, 4], "name_zh": "逻辑之通道", "name_en": "Channel of Logic",
        "centers": ["head", "ajna"], "theme": "心智的安逸——从怀疑到公式"
    },

    # === Ajna ↔ Throat ===
    (17, 62): {
        "gates": [17, 62], "name_zh": "接受之通道", "name_en": "Channel of Acceptance",
        "centers": ["ajna", "throat"], "theme": "组织型人才——意见与细节"
    },
    (43, 23): {
        "gates": [43, 23], "name_zh": "构建之通道", "name_en": "Channel of Structuring",
        "centers": ["ajna", "throat"], "theme": "个体性——从洞见到同化"
    },
    (11, 56): {
        "gates": [11, 56], "name_zh": "好奇之通道", "name_en": "Channel of Curiosity",
        "centers": ["ajna", "throat"], "theme": "探索者——想法与刺激"
    },

    # === Throat ↔ G Center ===
    (8, 1): {
        "gates": [8, 1], "name_zh": "启发之通道", "name_en": "Channel of Inspiration",
        "centers": ["throat", "g"], "theme": "创意的榜样——贡献与自我表达"
    },
    (31, 7): {
        "gates": [31, 7], "name_zh": "领袖之通道", "name_en": "Channel of the Alpha",
        "centers": ["throat", "g"], "theme": "领导力——影响与自我角色"
    },
    (33, 13): {
        "gates": [33, 13], "name_zh": "浪子之通道", "name_en": "Channel of the Prodigal",
        "centers": ["throat", "g"], "theme": "见证者——隐退与聆听"
    },
    (20, 10): {
        "gates": [20, 10], "name_zh": "觉醒之通道", "name_en": "Channel of Awakening",
        "centers": ["throat", "g"], "theme": "承诺于更高原则——当下与行为"
    },

    # === Throat ↔ Heart ===
    (45, 21): {
        "gates": [45, 21], "name_zh": "金钱之通道", "name_en": "Channel of Money",
        "centers": ["throat", "heart"], "theme": "物质主义者——聚集与掌控"
    },

    # === Throat ↔ Solar Plexus ===
    (35, 36): {
        "gates": [35, 36], "name_zh": "多才多艺之通道", "name_en": "Channel of Transitoriness",
        "centers": ["throat", "solar_plexus"], "theme": "万事通——变化与危机"
    },
    (12, 22): {
        "gates": [12, 22], "name_zh": "开放之通道", "name_en": "Channel of Openness",
        "centers": ["throat", "solar_plexus"], "theme": "社交人——谨慎与优雅"
    },

    # === Throat ↔ Sacral ===
    (20, 34): {
        "gates": [20, 34], "name_zh": "魅力之通道", "name_en": "Channel of Charisma",
        "centers": ["throat", "sacral"], "theme": "忙碌的人——当下与力量"
    },

    # === Throat ↔ Spleen ===
    (20, 57): {
        "gates": [20, 57], "name_zh": "脑波之通道", "name_en": "Channel of the Brainwave",
        "centers": ["throat", "spleen"], "theme": "穿透性的觉知——当下与直觉"
    },
    (16, 48): {
        "gates": [16, 48], "name_zh": "才华之通道", "name_en": "Channel of the Wavelength",
        "centers": ["throat", "spleen"], "theme": "才华——技艺与深度"
    },

    # === G Center ↔ Sacral ===
    (15, 5): {
        "gates": [15, 5], "name_zh": "韵律之通道", "name_en": "Channel of Rhythm",
        "centers": ["g", "sacral"], "theme": "顺流——极端与固定模式"
    },
    (2, 14): {
        "gates": [2, 14], "name_zh": "脉动之通道", "name_en": "Channel of the Beat",
        "centers": ["g", "sacral"], "theme": "掌管钥匙的人——方向与权力"
    },
    (46, 29): {
        "gates": [46, 29], "name_zh": "发现之通道", "name_en": "Channel of Discovery",
        "centers": ["g", "sacral"], "theme": "成功在于跟随——身体与坚持"
    },
    (10, 34): {
        "gates": [10, 34], "name_zh": "探索之通道", "name_en": "Channel of Exploration",
        "centers": ["g", "sacral"], "theme": "遵循信念——行为与力量"
    },

    # === G Center ↔ Spleen ===
    (10, 57): {
        "gates": [10, 57], "name_zh": "完美形式之通道", "name_en": "Channel of Perfected Form",
        "centers": ["g", "spleen"], "theme": "存活——行为与直觉"
    },

    # === G Center ↔ Heart ===
    (25, 51): {
        "gates": [25, 51], "name_zh": "发起之通道", "name_en": "Channel of Initiation",
        "centers": ["g", "heart"], "theme": "需要成为第一——天真与震撼"
    },

    # === Heart ↔ Spleen ===
    (26, 44): {
        "gates": [26, 44], "name_zh": "投降之通道", "name_en": "Channel of Surrender",
        "centers": ["heart", "spleen"], "theme": "传递者——利己与警觉"
    },

    # === Heart ↔ Solar Plexus ===
    (40, 37): {
        "gates": [40, 37], "name_zh": "社区之通道", "name_en": "Channel of Community",
        "centers": ["heart", "solar_plexus"], "theme": "寻求部落的人——独处与家庭"
    },

    # === Sacral ↔ Solar Plexus ===
    (59, 6): {
        "gates": [59, 6], "name_zh": "亲密之通道", "name_en": "Channel of Mating",
        "centers": ["sacral", "solar_plexus"], "theme": "专注于繁衍——分散与摩擦"
    },

    # === Sacral ↔ Spleen ===
    (27, 50): {
        "gates": [27, 50], "name_zh": "保存之通道", "name_en": "Channel of Preservation",
        "centers": ["sacral", "spleen"], "theme": "监护人——滋养与价值"
    },
    (34, 57): {
        "gates": [34, 57], "name_zh": "力量之通道", "name_en": "Channel of Power",
        "centers": ["sacral", "spleen"], "theme": "人类原型——力量与直觉"
    },

    # === Sacral ↔ Root ===
    (42, 53): {
        "gates": [42, 53], "name_zh": "成熟之通道", "name_en": "Channel of Maturation",
        "centers": ["sacral", "root"], "theme": "平衡发展——增长与开始"
    },
    (3, 60): {
        "gates": [3, 60], "name_zh": "变异之通道", "name_en": "Channel of Mutation",
        "centers": ["sacral", "root"], "theme": "脉搏的能量——秩序与限制"
    },
    (9, 52): {
        "gates": [9, 52], "name_zh": "专注之通道", "name_en": "Channel of Concentration",
        "centers": ["sacral", "root"], "theme": "决心——专注与静止"
    },

    # === Solar Plexus ↔ Root ===
    (49, 19): {
        "gates": [49, 19], "name_zh": "综合之通道", "name_en": "Channel of Synthesis",
        "centers": ["solar_plexus", "root"], "theme": "敏感——原则与靠近"
    },
    (55, 39): {
        "gates": [55, 39], "name_zh": "情绪之通道", "name_en": "Channel of Emoting",
        "centers": ["solar_plexus", "root"], "theme": "多愁善感——丰盛与挑衅"
    },
    (30, 41): {
        "gates": [30, 41], "name_zh": "识别之通道", "name_en": "Channel of Recognition",
        "centers": ["solar_plexus", "root"], "theme": "聚焦的能量——感受与收缩"
    },

    # === Spleen ↔ Root ===
    (18, 58): {
        "gates": [18, 58], "name_zh": "批判之通道", "name_en": "Channel of Judgment",
        "centers": ["spleen", "root"], "theme": "不知足——纠正与喜悦"
    },
    (28, 38): {
        "gates": [28, 38], "name_zh": "挣扎之通道", "name_en": "Channel of Struggle",
        "centers": ["spleen", "root"], "theme": "顽固——玩家与战士"
    },
    (32, 54): {
        "gates": [32, 54], "name_zh": "蜕变之通道", "name_en": "Channel of Transformation",
        "centers": ["spleen", "root"], "theme": "驱动力——持久与野心"
    },
}

assert len(CHANNEL_DATA) == 36, f"Expected 36 channels, got {len(CHANNEL_DATA)}"

"""
64 Human Design Gates — names, center, and keynotes.

Each gate maps to: name_zh, name_en, center, keynote
"""

GATE_DATA: dict[int, dict] = {
    1: {
        "gate": 1, "name_zh": "自我表达之门", "name_en": "Gate of Self-Expression",
        "center": "g", "keynote": "创造性的自我表达"
    },
    2: {
        "gate": 2, "name_zh": "接收之门", "name_en": "Gate of the Receptive",
        "center": "g", "keynote": "更高知识的方向"
    },
    3: {
        "gate": 3, "name_zh": "秩序之门", "name_en": "Gate of Ordering",
        "center": "sacral", "keynote": "变异与创新的能量"
    },
    4: {
        "gate": 4, "name_zh": "公式化之门", "name_en": "Gate of Formulization",
        "center": "ajna", "keynote": "理解的公式化"
    },
    5: {
        "gate": 5, "name_zh": "等待之门", "name_en": "Gate of Fixed Patterns",
        "center": "sacral", "keynote": "固定的节律与习惯"
    },
    6: {
        "gate": 6, "name_zh": "摩擦之门", "name_en": "Gate of Friction",
        "center": "solar_plexus", "keynote": "情绪的亲密与摩擦"
    },
    7: {
        "gate": 7, "name_zh": "军队之门", "name_en": "Gate of the Role of the Self",
        "center": "g", "keynote": "在互动中的自我角色"
    },
    8: {
        "gate": 8, "name_zh": "凝聚之门", "name_en": "Gate of Contribution",
        "center": "throat", "keynote": "做出独特贡献"
    },
    9: {
        "gate": 9, "name_zh": "专注之门", "name_en": "Gate of Focus",
        "center": "sacral", "keynote": "处理细节的能量"
    },
    10: {
        "gate": 10, "name_zh": "自我行为之门", "name_en": "Gate of the Behavior of the Self",
        "center": "g", "keynote": "爱自己的行为"
    },
    11: {
        "gate": 11, "name_zh": "和平之门", "name_en": "Gate of Ideas",
        "center": "ajna", "keynote": "新想法与概念"
    },
    12: {
        "gate": 12, "name_zh": "谨慎之门", "name_en": "Gate of Caution",
        "center": "throat", "keynote": "社交谨慎与表达"
    },
    13: {
        "gate": 13, "name_zh": "聆听者之门", "name_en": "Gate of the Listener",
        "center": "g", "keynote": "倾听与收集秘密"
    },
    14: {
        "gate": 14, "name_zh": "权力技巧之门", "name_en": "Gate of Power Skills",
        "center": "sacral", "keynote": "掌握资源的能量"
    },
    15: {
        "gate": 15, "name_zh": "极端之门", "name_en": "Gate of Extremes",
        "center": "g", "keynote": "人类行为的极端"
    },
    16: {
        "gate": 16, "name_zh": "技艺之门", "name_en": "Gate of Skills",
        "center": "throat", "keynote": "通过重复掌握技能"
    },
    17: {
        "gate": 17, "name_zh": "追随之门", "name_en": "Gate of Opinions",
        "center": "ajna", "keynote": "逻辑性的意见与跟随"
    },
    18: {
        "gate": 18, "name_zh": "纠正之门", "name_en": "Gate of Correction",
        "center": "spleen", "keynote": "发现并纠正模式"
    },
    19: {
        "gate": 19, "name_zh": "靠近之门", "name_en": "Gate of Wanting",
        "center": "root", "keynote": "对资源和归属的需求"
    },
    20: {
        "gate": 20, "name_zh": "当下之门", "name_en": "Gate of the Now",
        "center": "throat", "keynote": "活在当下的觉知"
    },
    21: {
        "gate": 21, "name_zh": "猎人之门", "name_en": "Gate of the Hunter/Huntress",
        "center": "heart", "keynote": "掌控与管理资源"
    },
    22: {
        "gate": 22, "name_zh": "优雅之门", "name_en": "Gate of Openness",
        "center": "solar_plexus", "keynote": "情绪的开放与优雅"
    },
    23: {
        "gate": 23, "name_zh": "同化之门", "name_en": "Gate of Assimilation",
        "center": "throat", "keynote": "将复杂化为简单"
    },
    24: {
        "gate": 24, "name_zh": "回归之门", "name_en": "Gate of Rationalization",
        "center": "ajna", "keynote": "反复思考与合理化"
    },
    25: {
        "gate": 25, "name_zh": "天真之门", "name_en": "Gate of Innocence",
        "center": "g", "keynote": "无条件之爱的精神"
    },
    26: {
        "gate": 26, "name_zh": "利己主义之门", "name_en": "Gate of the Egoist",
        "center": "heart", "keynote": "伟大的驯服者之力"
    },
    27: {
        "gate": 27, "name_zh": "滋养之门", "name_en": "Gate of Caring",
        "center": "sacral", "keynote": "照顾与滋养他人"
    },
    28: {
        "gate": 28, "name_zh": "玩家之门", "name_en": "Gate of the Game Player",
        "center": "spleen", "keynote": "为意义而挣扎"
    },
    29: {
        "gate": 29, "name_zh": "深渊之门", "name_en": "Gate of Perseverance",
        "center": "sacral", "keynote": "对体验说是的承诺"
    },
    30: {
        "gate": 30, "name_zh": "燃烧之火之门", "name_en": "Gate of Feelings",
        "center": "solar_plexus", "keynote": "对新体验的渴望"
    },
    31: {
        "gate": 31, "name_zh": "影响之门", "name_en": "Gate of Influence",
        "center": "throat", "keynote": "民主的领导力"
    },
    32: {
        "gate": 32, "name_zh": "持久之门", "name_en": "Gate of Continuity",
        "center": "spleen", "keynote": "本能地识别转变"
    },
    33: {
        "gate": 33, "name_zh": "隐退之门", "name_en": "Gate of Privacy",
        "center": "throat", "keynote": "记忆与隐退"
    },
    34: {
        "gate": 34, "name_zh": "强大之门", "name_en": "Gate of Power",
        "center": "sacral", "keynote": "纯粹的骶骨力量"
    },
    35: {
        "gate": 35, "name_zh": "变化之门", "name_en": "Gate of Change",
        "center": "throat", "keynote": "进步与体验"
    },
    36: {
        "gate": 36, "name_zh": "幽暗之光之门", "name_en": "Gate of Crisis",
        "center": "solar_plexus", "keynote": "情绪危机带来成长"
    },
    37: {
        "gate": 37, "name_zh": "家庭之门", "name_en": "Gate of Friendship",
        "center": "solar_plexus", "keynote": "友谊和社区的情感纽带"
    },
    38: {
        "gate": 38, "name_zh": "战士之门", "name_en": "Gate of the Fighter",
        "center": "root", "keynote": "为目标斗争的压力"
    },
    39: {
        "gate": 39, "name_zh": "挑衅之门", "name_en": "Gate of Provocation",
        "center": "root", "keynote": "通过挑衅激发精神"
    },
    40: {
        "gate": 40, "name_zh": "递送之门", "name_en": "Gate of Aloneness",
        "center": "heart", "keynote": "独处与意志力"
    },
    41: {
        "gate": 41, "name_zh": "收缩之门", "name_en": "Gate of Contraction",
        "center": "root", "keynote": "幻想与新开始的压力"
    },
    42: {
        "gate": 42, "name_zh": "增长之门", "name_en": "Gate of Growth",
        "center": "sacral", "keynote": "完成周期的能量"
    },
    43: {
        "gate": 43, "name_zh": "突破之门", "name_en": "Gate of Insight",
        "center": "ajna", "keynote": "独特的内在洞见"
    },
    44: {
        "gate": 44, "name_zh": "警觉之门", "name_en": "Gate of Alertness",
        "center": "spleen", "keynote": "本能识别模式"
    },
    45: {
        "gate": 45, "name_zh": "聚集之门", "name_en": "Gate of the Gatherer",
        "center": "throat", "keynote": "物质的聚集与分配"
    },
    46: {
        "gate": 46, "name_zh": "身体之门", "name_en": "Gate of the Determination of the Self",
        "center": "g", "keynote": "对身体的爱与决心"
    },
    47: {
        "gate": 47, "name_zh": "领悟之门", "name_en": "Gate of Realization",
        "center": "ajna", "keynote": "从困惑到领悟"
    },
    48: {
        "gate": 48, "name_zh": "深度之门", "name_en": "Gate of Depth",
        "center": "spleen", "keynote": "深度与才华的恐惧"
    },
    49: {
        "gate": 49, "name_zh": "革命之门", "name_en": "Gate of Principles",
        "center": "solar_plexus", "keynote": "接受与拒绝的原则"
    },
    50: {
        "gate": 50, "name_zh": "价值之门", "name_en": "Gate of Values",
        "center": "spleen", "keynote": "守护部落价值观"
    },
    51: {
        "gate": 51, "name_zh": "激震之门", "name_en": "Gate of Shock",
        "center": "heart", "keynote": "竞争与突然的震撼"
    },
    52: {
        "gate": 52, "name_zh": "静止之门", "name_en": "Gate of Stillness",
        "center": "root", "keynote": "专注与静止的压力"
    },
    53: {
        "gate": 53, "name_zh": "发展之门", "name_en": "Gate of Beginnings",
        "center": "root", "keynote": "开启新循环的压力"
    },
    54: {
        "gate": 54, "name_zh": "少女出嫁之门", "name_en": "Gate of Drive",
        "center": "root", "keynote": "向上攀升的野心"
    },
    55: {
        "gate": 55, "name_zh": "丰盛之门", "name_en": "Gate of Spirit",
        "center": "solar_plexus", "keynote": "情绪丰盛的精神"
    },
    56: {
        "gate": 56, "name_zh": "旅人之门", "name_en": "Gate of Stimulation",
        "center": "throat", "keynote": "通过故事刺激"
    },
    57: {
        "gate": 57, "name_zh": "温柔之门", "name_en": "Gate of Intuitive Clarity",
        "center": "spleen", "keynote": "当下直觉的清晰"
    },
    58: {
        "gate": 58, "name_zh": "喜悦之门", "name_en": "Gate of Vitality",
        "center": "root", "keynote": "追求完美的活力"
    },
    59: {
        "gate": 59, "name_zh": "分散之门", "name_en": "Gate of Sexuality",
        "center": "sacral", "keynote": "打破障碍的亲密"
    },
    60: {
        "gate": 60, "name_zh": "限制之门", "name_en": "Gate of Acceptance",
        "center": "root", "keynote": "接受限制带来变异"
    },
    61: {
        "gate": 61, "name_zh": "内在真理之门", "name_en": "Gate of Mystery",
        "center": "head", "keynote": "探索未知的灵感"
    },
    62: {
        "gate": 62, "name_zh": "细节之门", "name_en": "Gate of Detail",
        "center": "throat", "keynote": "表达细节与事实"
    },
    63: {
        "gate": 63, "name_zh": "完成之后之门", "name_en": "Gate of Doubt",
        "center": "head", "keynote": "逻辑的质疑与怀疑"
    },
    64: {
        "gate": 64, "name_zh": "完成之前之门", "name_en": "Gate of Confusion",
        "center": "head", "keynote": "从困惑中寻找意义"
    },
}

assert len(GATE_DATA) == 64, f"Expected 64 gates, got {len(GATE_DATA)}"

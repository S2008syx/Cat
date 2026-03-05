"""
9 Human Design Centers — names, themes, and not-self themes.
"""

CENTER_DATA: dict[str, dict] = {
    "head": {
        "id": "head", "name_zh": "头脑中心",
        "theme": "灵感与疑问",
        "not_self_theme": "试图回答所有不属于自己的问题"
    },
    "ajna": {
        "id": "ajna", "name_zh": "逻辑中心",
        "theme": "概念化与思维处理",
        "not_self_theme": "假装确定自己并不确定的事"
    },
    "throat": {
        "id": "throat", "name_zh": "喉咙中心",
        "theme": "沟通与行动的显化",
        "not_self_theme": "试图引起注意或急于表达"
    },
    "g": {
        "id": "g", "name_zh": "G中心",
        "theme": "身份认同、方向与爱",
        "not_self_theme": "迷失方向，寻找爱和身份认同"
    },
    "heart": {
        "id": "heart", "name_zh": "意志力中心",
        "theme": "意志力、自我价值与物质世界",
        "not_self_theme": "不断试图证明自己的价值"
    },
    "sacral": {
        "id": "sacral", "name_zh": "骶骨中心",
        "theme": "生命力、性欲与工作能量",
        "not_self_theme": "不知道什么时候够了"
    },
    "solar_plexus": {
        "id": "solar_plexus", "name_zh": "情绪中心",
        "theme": "情绪、感受与欲望",
        "not_self_theme": "回避真相和冲突"
    },
    "spleen": {
        "id": "spleen", "name_zh": "直觉中心",
        "theme": "直觉、健康与存活本能",
        "not_self_theme": "紧抓不健康的东西不放"
    },
    "root": {
        "id": "root", "name_zh": "根中心",
        "theme": "肾上腺素压力与驱动",
        "not_self_theme": "急于想把事情做完以摆脱压力"
    },
}

assert len(CENTER_DATA) == 9, f"Expected 9 centers, got {len(CENTER_DATA)}"

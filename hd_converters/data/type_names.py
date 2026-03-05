"""
5 Human Design Types — names, themes, strategy, and not-self.
"""

TYPE_DATA: dict[str, dict] = {
    "Generator": {
        "key": "Generator", "name_zh": "生产者", "name_en": "Generator",
        "theme": "满足 vs 挫败", "strategy_zh": "等待回应", "not_self": "挫败"
    },
    "Manifesting Generator": {
        "key": "Manifesting Generator", "name_zh": "显示生产者",
        "name_en": "Manifesting Generator",
        "theme": "满足 vs 挫败与愤怒", "strategy_zh": "等待回应，然后告知",
        "not_self": "挫败与愤怒"
    },
    "Manifestor": {
        "key": "Manifestor", "name_zh": "显示者", "name_en": "Manifestor",
        "theme": "平和 vs 愤怒", "strategy_zh": "告知", "not_self": "愤怒"
    },
    "Projector": {
        "key": "Projector", "name_zh": "投射者", "name_en": "Projector",
        "theme": "成功 vs 苦涩", "strategy_zh": "等待邀请", "not_self": "苦涩"
    },
    "Reflector": {
        "key": "Reflector", "name_zh": "反映者", "name_en": "Reflector",
        "theme": "惊喜 vs 失望", "strategy_zh": "等待一个月球周期",
        "not_self": "失望"
    },
}

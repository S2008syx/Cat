"""
12 Human Design Profiles and 6 Lines — names.
"""

LINE_NAMES: dict[int, dict] = {
    1: {"number": 1, "name_zh": "调查者", "name_en": "Investigator"},
    2: {"number": 2, "name_zh": "隐士", "name_en": "Hermit"},
    3: {"number": 3, "name_zh": "烈士", "name_en": "Martyr"},
    4: {"number": 4, "name_zh": "机会者", "name_en": "Opportunist"},
    5: {"number": 5, "name_zh": "异端者", "name_en": "Heretic"},
    6: {"number": 6, "name_zh": "榜样", "name_en": "Role Model"},
}

PROFILE_DATA: dict[str, dict] = {
    "1/3": {"key": "1/3", "name_zh": "调查者/烈士"},
    "1/4": {"key": "1/4", "name_zh": "调查者/机会者"},
    "2/4": {"key": "2/4", "name_zh": "隐士/机会者"},
    "2/5": {"key": "2/5", "name_zh": "隐士/异端者"},
    "3/5": {"key": "3/5", "name_zh": "烈士/异端者"},
    "3/6": {"key": "3/6", "name_zh": "烈士/榜样"},
    "4/6": {"key": "4/6", "name_zh": "机会者/榜样"},
    "4/1": {"key": "4/1", "name_zh": "机会者/调查者"},
    "5/1": {"key": "5/1", "name_zh": "异端者/调查者"},
    "5/2": {"key": "5/2", "name_zh": "异端者/隐士"},
    "6/2": {"key": "6/2", "name_zh": "榜样/隐士"},
    "6/3": {"key": "6/3", "name_zh": "榜样/烈士"},
}

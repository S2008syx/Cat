"""
Words Converter — transforms CalculatorOutput into WordsData
with structured keyword/name data for front-end display.

Pure data lookup and mapping, no report generation.
"""

from __future__ import annotations

from hd_calculator.models import CalculatorOutput
from .models import WordsData
from .data.type_names import TYPE_DATA
from .data.authority_names import AUTHORITY_DATA
from .data.profile_names import PROFILE_DATA, LINE_NAMES
from .data.center_names import CENTER_DATA
from .data.channel_names import CHANNEL_DATA
from .data.gate_names import GATE_DATA
from .data.cross_names import CROSS_DATA
from .data.bodygraph_layout import GATE_TO_CENTER


# Definition type descriptions
_DEFINITION_DESCRIPTIONS: dict[str, dict] = {
    "None": {
        "key": "None", "name_zh": "无定义",
        "description": "没有任何中心被定义。你是一面反射周围环境的镜子。"
    },
    "Single": {
        "key": "Single", "name_zh": "单一定义",
        "description": "所有定义的中心通过通道彼此相连，能量流动一致而稳定。"
    },
    "Split": {
        "key": "Split", "name_zh": "二分定义",
        "description": "定义的中心分成两个独立的组，需要桥梁来连接两部分能量。"
    },
    "Triple Split": {
        "key": "Triple Split", "name_zh": "三分定义",
        "description": "定义的中心分成三个独立的组，需要多个连接点来整合能量。"
    },
    "Quadruple Split": {
        "key": "Quadruple Split", "name_zh": "四分定义",
        "description": "定义的中心分成四个独立的组，是最稀有的定义类型。"
    },
}


def convert_words(output: CalculatorOutput) -> WordsData:
    """Convert CalculatorOutput to WordsData for front-end display.

    Args:
        output: A CalculatorOutput instance from hd_calculator.

    Returns:
        WordsData with all keyword/name mappings.
    """
    # === Type info ===
    type_info = dict(TYPE_DATA.get(output.type, {"key": output.type, "name_zh": output.type}))

    # === Authority info ===
    authority_info = dict(AUTHORITY_DATA.get(output.authority, {
        "key": output.authority, "name_zh": output.authority
    }))

    # === Profile info ===
    profile_key = output.profile
    line1_num = int(profile_key.split("/")[0])
    line2_num = int(profile_key.split("/")[1])
    profile_base = dict(PROFILE_DATA.get(profile_key, {"key": profile_key, "name_zh": profile_key}))
    profile_info = {
        **profile_base,
        "line1": LINE_NAMES.get(line1_num, {"number": line1_num, "name_zh": str(line1_num)}),
        "line2": LINE_NAMES.get(line2_num, {"number": line2_num, "name_zh": str(line2_num)}),
    }

    # === Definition info ===
    def_info = dict(_DEFINITION_DESCRIPTIONS.get(output.definition_type, {
        "key": output.definition_type, "name_zh": output.definition_type
    }))
    if output.split_type:
        def_info["split_type"] = output.split_type

    # === Cross info ===
    p_sun_gate = output.incarnation_cross_gates[0] if output.incarnation_cross_gates else 0
    cross_base = CROSS_DATA.get(p_sun_gate, {"name_en": "Unknown", "name_zh": "未知"})
    cross_type = output.incarnation_cross_type
    if cross_type == "Right Angle":
        prefix_en = "Right Angle"
        prefix_zh = "右角度"
    elif cross_type == "Juxtaposition":
        prefix_en = "Juxtaposition"
        prefix_zh = "并列"
    else:
        prefix_en = "Left Angle"
        prefix_zh = "左角度"

    cross_info = {
        "type": cross_type,
        "name_en": f"{prefix_en} {cross_base['name_en']}",
        "name_zh": f"{prefix_zh}{cross_base['name_zh']}",
        "gates": output.incarnation_cross_gates,
    }

    # === Center infos (all 9) ===
    defined_set = set(output.defined_centers)
    center_infos = []
    for center_id, cdata in CENTER_DATA.items():
        center_infos.append({
            "id": center_id,
            "name_zh": cdata["name_zh"],
            "defined": center_id in defined_set,
            "theme": cdata["theme"],
            "not_self_theme": cdata["not_self_theme"],
        })

    # === Channel infos (only active) ===
    channel_infos = []
    for ch in output.active_channels:
        key = (ch["gate_a"], ch["gate_b"])
        cdata = CHANNEL_DATA.get(key)
        if cdata:
            channel_infos.append({
                "gates": cdata["gates"],
                "name_zh": cdata["name_zh"],
                "name_en": cdata["name_en"],
                "centers": cdata["centers"],
                "theme": cdata["theme"],
            })
        else:
            # [FALLBACK] 反转 key 顺序查找 — 防御性代码，处理 gate 顺序不一致的情况
            rev_key = (ch["gate_b"], ch["gate_a"])
            cdata = CHANNEL_DATA.get(rev_key)
            if cdata:
                channel_infos.append({
                    "gates": cdata["gates"],
                    "name_zh": cdata["name_zh"],
                    "name_en": cdata["name_en"],
                    "centers": cdata["centers"],
                    "theme": cdata["theme"],
                })
            else:
                # [FALLBACK] 兜底 — CHANNEL_DATA 覆盖全部 36 条通道，
                # 正常情况下不会到达这里。保留以防数据不完整时不崩溃。
                channel_infos.append({
                    "gates": [ch["gate_a"], ch["gate_b"]],
                    "name_zh": "未知通道",
                    "name_en": "Unknown Channel",
                    "centers": [ch["center_a"], ch["center_b"]],
                    "theme": "",
                })

    # === Gate infos (all active, deduplicated) ===
    personality_gates = {a["gate"] for a in output.personality_activations}
    design_gates = {a["gate"] for a in output.design_activations}

    # Build activation lookup
    activation_details: dict[int, list[dict]] = {}
    for act in output.personality_activations:
        g = act["gate"]
        activation_details.setdefault(g, []).append({
            "side": "personality", "planet": act["planet"], "line": act["line"],
            "color": act["color"], "tone": act["tone"], "base": act["base"],
        })
    for act in output.design_activations:
        g = act["gate"]
        activation_details.setdefault(g, []).append({
            "side": "design", "planet": act["planet"], "line": act["line"],
            "color": act["color"], "tone": act["tone"], "base": act["base"],
        })

    gate_infos = []
    for gate in sorted(output.all_active_gates):
        gdata = GATE_DATA.get(gate)
        if gdata:
            gate_infos.append({
                "gate": gate,
                "name_zh": gdata["name_zh"],
                "name_en": gdata["name_en"],
                "center": gdata["center"],
                "keynote": gdata["keynote"],
                "activated_by": activation_details.get(gate, []),
            })
        else:
            # [FALLBACK] GATE_DATA 覆盖全部 64 门，正常不会到达这里。
            # 保留以防数据不完整时不崩溃。
            gate_infos.append({
                "gate": gate,
                "name_zh": f"门 {gate}",
                "name_en": f"Gate {gate}",
                "center": GATE_TO_CENTER.get(gate, "unknown"),
                "keynote": "",
                "activated_by": activation_details.get(gate, []),
            })

    # === Activations table (13 personality + 13 design rows) ===
    planet_order = [
        "sun", "earth", "north_node", "south_node", "moon",
        "mercury", "venus", "mars", "jupiter", "saturn",
        "uranus", "neptune", "pluto",
    ]
    planet_zh = {
        "sun": "太阳", "earth": "地球", "north_node": "北交点",
        "south_node": "南交点", "moon": "月亮", "mercury": "水星",
        "venus": "金星", "mars": "火星", "jupiter": "木星",
        "saturn": "土星", "uranus": "天王星", "neptune": "海王星",
        "pluto": "冥王星",
    }

    def _build_rows(acts: list[dict]) -> list[dict]:
        lookup = {a["planet"]: a for a in acts}
        rows = []
        for p in planet_order:
            a = lookup.get(p)
            if a:
                gdata = GATE_DATA.get(a["gate"], {})
                rows.append({
                    "planet": p,
                    "planet_zh": planet_zh.get(p, p),
                    "gate": a["gate"],
                    "line": a["line"],
                    "color": a["color"],
                    "tone": a["tone"],
                    "base": a["base"],
                    "gate_name_zh": gdata.get("name_zh", ""),
                    "gate_name_en": gdata.get("name_en", ""),
                })
            else:
                # [FALLBACK] map_all_activations() 总是返回全部 13 颗星体，
                # 正常不会缺失。保留以防上游数据不完整时不崩溃。
                rows.append({
                    "planet": p,
                    "planet_zh": planet_zh.get(p, p),
                    "gate": None,
                    "line": None,
                    "color": None,
                    "tone": None,
                    "base": None,
                    "gate_name_zh": "",
                    "gate_name_en": "",
                })
        return rows

    activations = {
        "personality": _build_rows(output.personality_activations),
        "design": _build_rows(output.design_activations),
    }

    return WordsData(
        type_info=type_info,
        authority_info=authority_info,
        profile_info=profile_info,
        definition_info=def_info,
        cross_info=cross_info,
        center_infos=center_infos,
        channel_infos=channel_infos,
        gate_infos=gate_infos,
        activations=activations,
    )

"""
Bodygraph SVG image generator.

Generates a self-contained SVG string from GraphData + WordsData,
suitable for rendering as an <img> or downloading.
"""

from __future__ import annotations


# SVG canvas
W, H = 480, 680
PAD = 20

# Colors
C_DEFINED = "#f5c542"
C_UNDEFINED = "#e8e8e8"
C_STROKE_DEF = "#b8860b"
C_STROKE_UNDEF = "#aaa"
C_PERSONALITY = "#333"
C_DESIGN = "#c0392b"
C_MIXED = "#8e44ad"
C_BG = "#ffffff"
C_TEXT = "#333"
C_ACCENT = "#6c5ce7"

# Center positions (absolute px)
_CENTER_POS = {
    "head":          (240, 60),
    "ajna":          (240, 150),
    "throat":        (240, 250),
    "g":             (240, 355),
    "heart":         (320, 400),
    "sacral":        (240, 520),
    "solar_plexus":  (370, 490),
    "spleen":        (110, 490),
    "root":          (240, 620),
}

_CENTER_SHAPES = {
    "head": "triangle",
    "ajna": "triangle",
    "throat": "square",
    "g": "diamond",
    "heart": "triangle",
    "sacral": "square",
    "solar_plexus": "triangle",
    "spleen": "triangle",
    "root": "square",
}

_CENTER_LABELS = {
    "head": "头脑",
    "ajna": "逻辑",
    "throat": "喉咙",
    "g": "G",
    "heart": "意志力",
    "sacral": "骶骨",
    "solar_plexus": "情绪",
    "spleen": "直觉",
    "root": "根",
}


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _center_shape_svg(cid: str, defined: bool, size: int = 26) -> str:
    x, y = _CENTER_POS[cid]
    fill = C_DEFINED if defined else C_UNDEFINED
    stroke = C_STROKE_DEF if defined else C_STROKE_UNDEF
    shape = _CENTER_SHAPES[cid]
    label = _CENTER_LABELS.get(cid, cid)

    parts = []
    if shape == "triangle":
        pts = f"{x},{y - size} {x - size},{y + int(size * 0.7)} {x + size},{y + int(size * 0.7)}"
        parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    elif shape == "diamond":
        pts = f"{x},{y - size} {x + size},{y} {x},{y + size} {x - size},{y}"
        parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    else:  # square
        s2 = int(size * 0.8)
        parts.append(
            f'<rect x="{x - s2}" y="{y - s2}" width="{s2 * 2}" height="{s2 * 2}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2" rx="3"/>'
        )
    # label
    parts.append(
        f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="10" '
        f'font-weight="bold" fill="{C_TEXT}">{_escape(label)}</text>'
    )
    return "\n".join(parts)


def _channel_line_svg(center_a: str, center_b: str, color: str) -> str:
    if center_a not in _CENTER_POS or center_b not in _CENTER_POS:
        return ""
    x1, y1 = _CENTER_POS[center_a]
    x2, y2 = _CENTER_POS[center_b]
    c = {"personality": C_PERSONALITY, "design": C_DESIGN, "mixed": C_MIXED}.get(color, "#999")
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{c}" stroke-width="3" stroke-linecap="round" opacity="0.7"/>'
    )


def generate_chart_svg(graph_data: dict, words_data: dict, name: str = "", birth_info: str = "") -> str:
    """Generate a self-contained SVG bodygraph image.

    Args:
        graph_data: GraphData.to_dict() output.
        words_data: WordsData.to_dict() output.
        name: Person's name.
        birth_info: Birth date/time string.

    Returns:
        SVG string.
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" style="font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
        f'<rect width="{W}" height="{H}" fill="{C_BG}" rx="12"/>',
    ]

    # Title
    title = _escape(f"{name} 的人类图" if name else "人类图")
    parts.append(
        f'<text x="{W // 2}" y="28" text-anchor="middle" font-size="16" '
        f'font-weight="bold" fill="{C_TEXT}">{title}</text>'
    )
    if birth_info:
        parts.append(
            f'<text x="{W // 2}" y="44" text-anchor="middle" font-size="11" '
            f'fill="#888">{_escape(birth_info)}</text>'
        )

    # Meta info (type / profile / authority)
    meta = graph_data.get("meta", {})
    type_zh = words_data.get("type_info", {}).get("name_zh", meta.get("type", ""))
    profile = meta.get("profile", "")
    authority_zh = words_data.get("authority_info", {}).get("name_zh", meta.get("authority", ""))
    # Not-self theme
    not_self = words_data.get("type_info", {}).get("not_self", "")

    # Channels (draw behind centers)
    for ch in graph_data.get("channels", []):
        parts.append(_channel_line_svg(ch["center_a"], ch["center_b"], ch["color"]))

    # Centers
    centers_defined = {}
    for c in graph_data.get("centers", []):
        centers_defined[c["id"]] = c["defined"]
    for cid in _CENTER_POS:
        defined = centers_defined.get(cid, False)
        parts.append(_center_shape_svg(cid, defined))

    # Info box at bottom-left
    info_lines = []
    if type_zh:
        info_lines.append(f"类型: {type_zh}")
    if profile:
        info_lines.append(f"人生角色: {profile}")
    if authority_zh:
        info_lines.append(f"权威: {authority_zh}")
    definition_zh = words_data.get("definition_info", {}).get("name_zh", "")
    if definition_zh:
        info_lines.append(f"定义: {definition_zh}")
    if not_self:
        info_lines.append(f"非自我主题: {not_self}")

    # Draw info text
    # Strategy
    strategy = words_data.get("type_info", {}).get("strategy", "")
    if strategy:
        info_lines.append(f"策略: {strategy}")

    cross_zh = words_data.get("cross_info", {}).get("name_zh", "")
    if cross_zh:
        info_lines.append(f"轮回交叉: {cross_zh}")

    # Render info lines in a box area top-right corner
    # Actually let's keep them simple above the graph
    # We'll put them below the title area

    # Legend
    ly = H - 20
    parts.append(
        f'<rect x="8" y="{ly - 10}" width="12" height="12" fill="{C_DEFINED}" '
        f'stroke="{C_STROKE_DEF}" stroke-width="1"/>'
    )
    parts.append(f'<text x="24" y="{ly}" font-size="9" fill="#888">已定义</text>')
    parts.append(
        f'<rect x="60" y="{ly - 10}" width="12" height="12" fill="{C_UNDEFINED}" '
        f'stroke="{C_STROKE_UNDEF}" stroke-width="1"/>'
    )
    parts.append(f'<text x="76" y="{ly}" font-size="9" fill="#888">未定义</text>')
    parts.append(
        f'<line x1="120" y1="{ly - 4}" x2="135" y2="{ly - 4}" '
        f'stroke="{C_PERSONALITY}" stroke-width="2"/>'
    )
    parts.append(f'<text x="139" y="{ly}" font-size="9" fill="#888">个性</text>')
    parts.append(
        f'<line x1="165" y1="{ly - 4}" x2="180" y2="{ly - 4}" '
        f'stroke="{C_DESIGN}" stroke-width="2"/>'
    )
    parts.append(f'<text x="184" y="{ly}" font-size="9" fill="#888">设计</text>')

    parts.append("</svg>")
    return "\n".join(parts)

"""
Bodygraph SVG image generator.

Generates a self-contained SVG string from GraphData + WordsData,
suitable for rendering as an <img> or downloading.

Rendering layers (back to front):
  1. Human body silhouette (light gray outline)
  2. Inactive channels (all 36, light gray)
  3. Active channels (colored: black/red/purple, split for mixed)
  4. Center shapes (9 centers, defined=gold, undefined=gray)
  5. Gate activation dots (colored circles for active gates)
  6. Gate numbers (all 64 labels)
  7. Variables arrows + Tone numbers (top area)
  8. Activation tables (left=Design/red, right=Personality/black)
  9. Info bar (Type / Profile / Authority / Cross)
"""

from __future__ import annotations

from .data.bodygraph_layout import (
    CENTER_RENDER_POS, CENTER_RENDER_SHAPES, CENTER_RENDER_LABELS,
    GATE_POSITIONS, GATE_TO_CENTER,
    ALL_CHANNELS, CHANNEL_CURVES, SILHOUETTE_PATH,
)

# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
W, H = 760, 880

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
C_DEFINED = "#f5c542"
C_UNDEFINED = "#e8e8e8"
C_STROKE_DEF = "#b8860b"
C_STROKE_UNDEF = "#aaa"
C_PERSONALITY = "#333"
C_DESIGN = "#c0392b"
C_BOTH = "#8e44ad"
C_CHANNEL_INACTIVE = "#e0e0e0"
C_BG = "#ffffff"
C_TEXT = "#333"
C_SILHOUETTE = "#f0f0f0"

# Planet display order and symbols
_PLANET_ORDER = [
    "sun", "earth", "north_node", "south_node", "moon",
    "mercury", "venus", "mars", "jupiter", "saturn",
    "uranus", "neptune", "pluto",
]
_PLANET_SYMBOLS: dict[str, str] = {
    "sun": "\u2609", "earth": "\u2295",
    "north_node": "\u260a", "south_node": "\u260b",
    "moon": "\u263d", "mercury": "\u263f",
    "venus": "\u2640", "mars": "\u2642",
    "jupiter": "\u2643", "saturn": "\u2644",
    "uranus": "\u2645", "neptune": "\u2646",
    "pluto": "\u2647",
}


def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _gate_color_value(color: str) -> str:
    """Map gate/channel color key to CSS color."""
    return {
        "personality": C_PERSONALITY,
        "design": C_DESIGN,
        "both": C_BOTH,
        "mixed": C_BOTH,
    }.get(color, "#999")


# ---------------------------------------------------------------------------
# Layer 1 — Human silhouette
# ---------------------------------------------------------------------------
def _render_silhouette() -> str:
    return (
        f'<path d="{SILHOUETTE_PATH}" fill="none" '
        f'stroke="{C_SILHOUETTE}" stroke-width="1.8" stroke-linecap="round"/>'
    )


# ---------------------------------------------------------------------------
# Layer 2 — Inactive channels (all 36, light gray)
# ---------------------------------------------------------------------------
def _channel_path_d(ga: int, gb: int) -> str:
    """Build SVG path 'd' attribute for a channel between two gates."""
    x1, y1 = GATE_POSITIONS[ga]
    x2, y2 = GATE_POSITIONS[gb]
    key = (ga, gb)
    rev = (gb, ga)
    ctrl = CHANNEL_CURVES.get(key) or CHANNEL_CURVES.get(rev)
    if ctrl and len(ctrl) == 1:
        cx, cy = ctrl[0]
        return f"M {x1},{y1} Q {cx},{cy} {x2},{y2}"
    if ctrl and len(ctrl) == 2:
        c1x, c1y = ctrl[0]
        c2x, c2y = ctrl[1]
        return f"M {x1},{y1} C {c1x},{c1y} {c2x},{c2y} {x2},{y2}"
    return f"M {x1},{y1} L {x2},{y2}"


def _render_inactive_channels(active_keys: set[tuple[int, int]]) -> str:
    parts: list[str] = []
    for ga, gb in ALL_CHANNELS:
        if (ga, gb) in active_keys or (gb, ga) in active_keys:
            continue
        d = _channel_path_d(ga, gb)
        parts.append(
            f'<path d="{d}" fill="none" stroke="{C_CHANNEL_INACTIVE}" '
            f'stroke-width="3" stroke-linecap="round"/>'
        )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 3 — Active channels (colored)
# ---------------------------------------------------------------------------
def _render_active_channels(
    channels: list[dict], gate_color_map: dict[int, str]
) -> str:
    """Render active channels with split coloring for mixed channels."""
    parts: list[str] = []
    for ch in channels:
        ga, gb = ch["gate_a"], ch["gate_b"]
        ch_color = ch.get("color", "personality")

        if ch_color != "mixed":
            css = _gate_color_value(ch_color)
            d = _channel_path_d(ga, gb)
            parts.append(
                f'<path d="{d}" fill="none" stroke="{css}" '
                f'stroke-width="4" stroke-linecap="round" opacity="0.85"/>'
            )
        else:
            # Split coloring: each half takes its gate's color
            x1, y1 = GATE_POSITIONS.get(ga, (0, 0))
            x2, y2 = GATE_POSITIONS.get(gb, (0, 0))
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2

            # Check for bezier curve
            key = (ga, gb)
            rev = (gb, ga)
            ctrl = CHANNEL_CURVES.get(key) or CHANNEL_CURVES.get(rev)

            color_a = _gate_color_value(gate_color_map.get(ga, "personality"))
            color_b = _gate_color_value(gate_color_map.get(gb, "design"))

            if ctrl:
                # For curves, draw the full path but use a gradient
                grad_id = f"grad_{ga}_{gb}"
                parts.append(
                    f'<defs><linearGradient id="{grad_id}" '
                    f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'gradientUnits="userSpaceOnUse">'
                    f'<stop offset="0%" stop-color="{color_a}"/>'
                    f'<stop offset="50%" stop-color="{color_a}"/>'
                    f'<stop offset="50%" stop-color="{color_b}"/>'
                    f'<stop offset="100%" stop-color="{color_b}"/>'
                    f'</linearGradient></defs>'
                )
                d = _channel_path_d(ga, gb)
                parts.append(
                    f'<path d="{d}" fill="none" stroke="url(#{grad_id})" '
                    f'stroke-width="4" stroke-linecap="round" opacity="0.85"/>'
                )
            else:
                # Straight line: two half-segments
                parts.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{mx}" y2="{my}" '
                    f'stroke="{color_a}" stroke-width="4" '
                    f'stroke-linecap="round" opacity="0.85"/>'
                )
                parts.append(
                    f'<line x1="{mx}" y1="{my}" x2="{x2}" y2="{y2}" '
                    f'stroke="{color_b}" stroke-width="4" '
                    f'stroke-linecap="round" opacity="0.85"/>'
                )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 4 — Center shapes
# ---------------------------------------------------------------------------
_CENTER_SIZE = 26


def _center_shape_svg(cid: str, defined: bool) -> str:
    x, y = CENTER_RENDER_POS[cid]
    fill = C_DEFINED if defined else C_UNDEFINED
    stroke = C_STROKE_DEF if defined else C_STROKE_UNDEF
    shape = CENTER_RENDER_SHAPES[cid]
    label = CENTER_RENDER_LABELS.get(cid, cid)
    s = _CENTER_SIZE

    parts: list[str] = []
    if shape == "triangle_up":
        pts = f"{x},{y - s} {x - s},{y + int(s * 0.7)} {x + s},{y + int(s * 0.7)}"
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
    elif shape == "triangle_down":
        pts = f"{x - s},{y - int(s * 0.7)} {x + s},{y - int(s * 0.7)} {x},{y + s}"
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
    elif shape == "triangle_left":
        pts = f"{x + int(s * 0.7)},{y - s} {x + int(s * 0.7)},{y + s} {x - s},{y}"
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
    elif shape == "triangle_right":
        pts = f"{x - int(s * 0.7)},{y - s} {x + s},{y} {x - int(s * 0.7)},{y + s}"
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
    elif shape == "diamond":
        pts = f"{x},{y - s} {x + s},{y} {x},{y + s} {x - s},{y}"
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
    else:  # square
        hs = int(s * 0.8)
        parts.append(
            f'<rect x="{x - hs}" y="{y - hs}" width="{hs * 2}" height="{hs * 2}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2" rx="3"/>'
        )
    # Center label
    parts.append(
        f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="9" '
        f'font-weight="bold" fill="{C_TEXT}" pointer-events="none">'
        f'{_escape(label)}</text>'
    )
    return "\n".join(parts)


def _render_centers(centers: list[dict]) -> str:
    defined_set: set[str] = set()
    for c in centers:
        if c.get("defined"):
            defined_set.add(c["id"])
    parts = [_center_shape_svg(cid, cid in defined_set) for cid in CENTER_RENDER_POS]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 5 — Gate activation dots
# ---------------------------------------------------------------------------
_GATE_DOT_R = 8


def _render_gate_dots(gate_color_map: dict[int, str]) -> str:
    """Draw colored dots behind gate numbers for active gates."""
    parts: list[str] = []
    for gate_num, color_key in gate_color_map.items():
        if gate_num not in GATE_POSITIONS:
            continue
        gx, gy = GATE_POSITIONS[gate_num]
        css = _gate_color_value(color_key)
        parts.append(
            f'<circle cx="{gx}" cy="{gy}" r="{_GATE_DOT_R}" '
            f'fill="{css}" opacity="0.25"/>'
        )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 6 — Gate numbers
# ---------------------------------------------------------------------------
_GATE_FONT = 8


def _render_gate_numbers(active_gates: set[int], gate_color_map: dict[int, str]) -> str:
    """Render all 64 gate numbers. Active gates are bold + colored."""
    parts: list[str] = []
    for gate_num, (gx, gy) in GATE_POSITIONS.items():
        is_active = gate_num in active_gates
        color = _gate_color_value(gate_color_map[gate_num]) if gate_num in gate_color_map else "#bbb"
        weight = "bold" if is_active else "normal"
        font_size = _GATE_FONT + 1 if is_active else _GATE_FONT
        parts.append(
            f'<text x="{gx}" y="{gy + 3}" text-anchor="middle" '
            f'font-size="{font_size}" font-weight="{weight}" fill="{color}" '
            f'pointer-events="none">{gate_num}</text>'
        )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 7 — Variables arrows + Tone
# ---------------------------------------------------------------------------
_ARROW_LABELS = {
    "digestion": "消化",
    "environment": "环境",
    "motivation": "动机",
    "perspective": "观点",
}


def _render_variables(variables: dict | None) -> str:
    if not variables:
        return ""
    parts: list[str] = []
    # Four arrows positioned across the top of the bodygraph
    # Layout: ←2  ←3  |  4→  5→  (left pair = body, right pair = mind)
    base_y = 48
    positions = [
        ("digestion",   280, base_y),    # top-left
        ("environment", 340, base_y),    # left-center
        ("motivation",  420, base_y),    # right-center
        ("perspective", 480, base_y),    # top-right
    ]
    for var_key, vx, vy in positions:
        var = variables.get(var_key)
        if not var:
            continue
        arrow_dir = var.get("arrow", "Left")
        tone = var.get("tone", "")
        arrow_sym = "\u2190" if arrow_dir == "Left" else "\u2192"  # ← or →
        label = _ARROW_LABELS.get(var_key, var_key)
        display = f"{arrow_sym} {tone}" if tone else arrow_sym
        parts.append(
            f'<text x="{vx}" y="{vy}" text-anchor="middle" font-size="11" '
            f'fill="{C_TEXT}">{_escape(display)}</text>'
        )
        parts.append(
            f'<text x="{vx}" y="{vy + 12}" text-anchor="middle" font-size="7" '
            f'fill="#999">{_escape(label)}</text>'
        )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 8 — Activation tables (side panels)
# ---------------------------------------------------------------------------
def _render_activation_tables(activations: dict | None) -> str:
    """Left panel = Design (red), Right panel = Personality (black)."""
    if not activations:
        return ""
    parts: list[str] = []

    def _draw_table(
        rows: list[dict], start_x: int, start_y: int,
        text_color: str, side_label: str
    ) -> None:
        # Header
        parts.append(
            f'<text x="{start_x + 55}" y="{start_y}" text-anchor="middle" '
            f'font-size="10" font-weight="bold" fill="{text_color}">'
            f'{_escape(side_label)}</text>'
        )
        row_h = 18
        for i, row in enumerate(rows):
            ry = start_y + 16 + i * row_h
            planet = row.get("planet", "")
            symbol = _PLANET_SYMBOLS.get(planet, "?")
            gate = row.get("gate")
            line = row.get("line")
            if gate is not None:
                gate_line = f"{gate}.{line}"
            else:
                gate_line = "-"
            # Planet symbol
            parts.append(
                f'<text x="{start_x + 6}" y="{ry}" font-size="12" '
                f'fill="{text_color}">{symbol}</text>'
            )
            # Gate.Line
            parts.append(
                f'<text x="{start_x + 26}" y="{ry}" font-size="10" '
                f'fill="{text_color}">{_escape(gate_line)}</text>'
            )
            # Gate name (truncated)
            gname = row.get("gate_name_zh", "")
            if len(gname) > 5:
                gname = gname[:5] + ".."
            parts.append(
                f'<text x="{start_x + 64}" y="{ry}" font-size="8" '
                f'fill="{text_color}" opacity="0.7">{_escape(gname)}</text>'
            )

    # Design (left, red)
    design_rows = activations.get("design", [])
    _draw_table(design_rows, 8, 110, C_DESIGN, "Design \u8bbe\u8ba1")

    # Personality (right, black)
    personality_rows = activations.get("personality", [])
    _draw_table(personality_rows, 640, 110, C_PERSONALITY, "Personality \u4e2a\u6027")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Layer 9 — Info bar
# ---------------------------------------------------------------------------
def _render_info_bar(words_data: dict) -> str:
    parts: list[str] = []
    meta_y = 710
    line_h = 18

    info_items: list[str] = []
    type_zh = words_data.get("type_info", {}).get("name_zh", "")
    strategy = words_data.get("type_info", {}).get("strategy", "")
    authority_zh = words_data.get("authority_info", {}).get("name_zh", "")
    profile_key = words_data.get("profile_info", {}).get("key", "")
    definition_zh = words_data.get("definition_info", {}).get("name_zh", "")
    not_self = words_data.get("type_info", {}).get("not_self", "")
    cross_zh = words_data.get("cross_info", {}).get("name_zh", "")

    if type_zh:
        info_items.append(f"\u7c7b\u578b: {type_zh}")
    if strategy:
        info_items.append(f"\u7b56\u7565: {strategy}")
    if profile_key:
        info_items.append(f"\u4eba\u751f\u89d2\u8272: {profile_key}")
    if authority_zh:
        info_items.append(f"\u6743\u5a01: {authority_zh}")
    if definition_zh:
        info_items.append(f"\u5b9a\u4e49: {definition_zh}")
    if not_self:
        info_items.append(f"\u975e\u81ea\u6211\u4e3b\u9898: {not_self}")
    if cross_zh:
        info_items.append(f"\u8f6e\u56de\u4ea4\u53c9: {cross_zh}")

    # Two-column layout
    col1_x, col2_x = 30, 400
    for i, item in enumerate(info_items):
        col_x = col1_x if i % 2 == 0 else col2_x
        row = i // 2
        parts.append(
            f'<text x="{col_x}" y="{meta_y + row * line_h}" '
            f'font-size="10" fill="{C_TEXT}">{_escape(item)}</text>'
        )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
def _render_legend() -> str:
    ly = H - 22
    parts: list[str] = []
    items = [
        (C_DEFINED, C_STROKE_DEF, "\u5df2\u5b9a\u4e49"),
        (C_UNDEFINED, C_STROKE_UNDEF, "\u672a\u5b9a\u4e49"),
    ]
    lx = 200
    for fill, stroke, label in items:
        parts.append(
            f'<rect x="{lx}" y="{ly - 10}" width="12" height="12" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )
        parts.append(f'<text x="{lx + 16}" y="{ly}" font-size="9" fill="#888">{label}</text>')
        lx += 64

    line_items = [
        (C_PERSONALITY, "\u4e2a\u6027(Personality)"),
        (C_DESIGN, "\u8bbe\u8ba1(Design)"),
        (C_BOTH, "\u4e24\u8005(Both)"),
    ]
    for color, label in line_items:
        parts.append(
            f'<line x1="{lx}" y1="{ly - 4}" x2="{lx + 15}" y2="{ly - 4}" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        parts.append(f'<text x="{lx + 19}" y="{ly}" font-size="9" fill="#888">{label}</text>')
        lx += 90
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generate_chart_svg(
    graph_data: dict, words_data: dict,
    name: str = "", birth_info: str = "",
) -> str:
    """Generate a self-contained SVG bodygraph image.

    Args:
        graph_data: GraphData.to_dict() output.
        words_data: WordsData.to_dict() output.
        name: Person's name.
        birth_info: Birth date/time string.

    Returns:
        SVG string.
    """
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" '
        f'style="font-family: -apple-system, BlinkMacSystemFont, \'Noto Sans SC\', sans-serif;">',
        f'<rect width="{W}" height="{H}" fill="{C_BG}" rx="12"/>',
    ]

    # --- Title ---
    title = _escape(f"{name} \u7684\u4eba\u7c7b\u56fe" if name else "\u4eba\u7c7b\u56fe")
    parts.append(
        f'<text x="{W // 2}" y="22" text-anchor="middle" font-size="15" '
        f'font-weight="bold" fill="{C_TEXT}">{title}</text>'
    )
    if birth_info:
        parts.append(
            f'<text x="{W // 2}" y="36" text-anchor="middle" font-size="10" '
            f'fill="#888">{_escape(birth_info)}</text>'
        )

    # --- Build lookup structures ---
    # Gate color map: gate_num → "personality" | "design" | "both"
    gate_color_map: dict[int, str] = {}
    for g in graph_data.get("gates", []):
        gate_color_map[g["gate"]] = g.get("color", "personality")

    active_gates = set(gate_color_map.keys())

    # Active channel keys
    active_channel_keys: set[tuple[int, int]] = set()
    for ch in graph_data.get("channels", []):
        active_channel_keys.add((ch["gate_a"], ch["gate_b"]))

    # --- Layer 1: Human silhouette ---
    parts.append(_render_silhouette())

    # --- Layer 2: Inactive channels ---
    parts.append(_render_inactive_channels(active_channel_keys))

    # --- Layer 3: Active channels ---
    parts.append(_render_active_channels(graph_data.get("channels", []), gate_color_map))

    # --- Layer 4: Centers ---
    parts.append(_render_centers(graph_data.get("centers", [])))

    # --- Layer 5: Gate activation dots ---
    parts.append(_render_gate_dots(gate_color_map))

    # --- Layer 6: Gate numbers ---
    parts.append(_render_gate_numbers(active_gates, gate_color_map))

    # --- Layer 7: Variables arrows + Tone ---
    variables = graph_data.get("meta", {}).get("variables")
    parts.append(_render_variables(variables))

    # --- Layer 8: Activation tables ---
    parts.append(_render_activation_tables(words_data.get("activations")))

    # --- Layer 9: Info bar ---
    parts.append(_render_info_bar(words_data))

    # --- Legend ---
    parts.append(_render_legend())

    parts.append("</svg>")
    return "\n".join(parts)

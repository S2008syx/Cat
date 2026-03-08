"""
Graph Converter — transforms CalculatorOutput into GraphData
for front-end Bodygraph rendering.

Pure data transformation, no SVG generation.
"""

from __future__ import annotations

from hd_calculator.models import CalculatorOutput
from .models import GraphData
from .data.bodygraph_layout import CENTER_LAYOUT, GATE_TO_CENTER
from .data.center_names import CENTER_DATA


def convert_graph(output: CalculatorOutput) -> GraphData:
    """Convert CalculatorOutput to GraphData for front-end rendering.

    Args:
        output: A CalculatorOutput instance from hd_calculator.

    Returns:
        GraphData with centers, channels, gates, and meta.
    """
    defined_set = set(output.defined_centers)
    personality_gates = {a["gate"] for a in output.personality_activations}
    design_gates = {a["gate"] for a in output.design_activations}

    # === Centers (all 9) ===
    centers = []
    for center_id in CENTER_LAYOUT:
        layout = CENTER_LAYOUT[center_id]
        name_zh = CENTER_DATA[center_id]["name_zh"]
        centers.append({
            "id": center_id,
            "name_zh": name_zh,
            "defined": center_id in defined_set,
            "position": layout["position"],
            "shape": layout["shape"],
        })

    # === Gates (deduplicated, with color and activation details) ===
    # Build activation lookup: gate -> list of {side, planet, line}
    activation_details: dict[int, list[dict]] = {}
    for act in output.personality_activations:
        g = act["gate"]
        activation_details.setdefault(g, []).append({
            "side": "personality", "planet": act["planet"], "line": act["line"]
        })
    for act in output.design_activations:
        g = act["gate"]
        activation_details.setdefault(g, []).append({
            "side": "design", "planet": act["planet"], "line": act["line"]
        })

    gates = []
    for gate in sorted(output.all_active_gates):
        in_p = gate in personality_gates
        in_d = gate in design_gates
        if in_p and in_d:
            color = "both"
        elif in_p:
            color = "personality"
        else:
            color = "design"

        gates.append({
            "gate": gate,
            "center": GATE_TO_CENTER.get(gate, "unknown"),
            "color": color,
            "activated_by": activation_details.get(gate, []),
        })

    # === Channels (only active, with color) ===
    channels = []
    for ch in output.active_channels:
        ga, gb = ch["gate_a"], ch["gate_b"]
        a_in_p = ga in personality_gates
        b_in_p = gb in personality_gates
        a_in_d = ga in design_gates
        b_in_d = gb in design_gates
        has_p = a_in_p or b_in_p
        has_d = a_in_d or b_in_d

        if has_p and has_d:
            ch_color = "mixed"
        elif has_p:
            ch_color = "personality"
        else:
            ch_color = "design"

        channels.append({
            "gate_a": ga,
            "gate_b": gb,
            "center_a": ch["center_a"],
            "center_b": ch["center_b"],
            "color": ch_color,
        })

    # === Meta ===
    meta = {
        "type": output.type,
        "profile": output.profile,
        "authority": output.authority,
        "variables": output.variables,
    }

    return GraphData(
        centers=centers,
        channels=channels,
        gates=gates,
        meta=meta,
    )

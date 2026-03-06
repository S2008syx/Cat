"""
Human Design Calculator - Chart Properties

Derives channels, centers, type, authority, profile, definition type,
and incarnation cross from gate activations.

Layers 3-5 of the calculation pipeline.
"""

from __future__ import annotations

from collections import defaultdict

from .data.channels import CHANNELS
from .data.centers import ALL_CENTER_NAMES, MOTOR_CENTERS, GATE_TO_CENTER


def find_active_channels(active_gates: set[int]) -> list[dict]:
    """Find all defined (active) channels based on activated gates.

    A channel is defined when BOTH of its gates are activated.

    Args:
        active_gates: Set of all activated gate numbers.

    Returns:
        List of channel dicts:
        [{"gate_a": 6, "gate_b": 59, "center_a": "solar_plexus", "center_b": "sacral"}, ...]
    """
    # [SOURCE] 参考: SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign)
    # 参考内容: 通道激活逻辑 — 两端门都激活则通道定义
    # 修改说明: 简化为 Python set intersection 检查

    active_channels: list[dict] = []
    for (gate_a, gate_b), (center_a, center_b) in CHANNELS.items():
        if gate_a in active_gates and gate_b in active_gates:
            active_channels.append({
                "gate_a": gate_a,
                "gate_b": gate_b,
                "center_a": center_a,
                "center_b": center_b,
            })
    return active_channels


def find_defined_centers(active_channels: list[dict]) -> tuple[list[str], list[str]]:
    """Determine which centers are defined based on active channels.

    A center is defined if at least one channel passes through it.

    Args:
        active_channels: List of active channel dicts.

    Returns:
        Tuple of (defined_centers, undefined_centers) as lists of center names.
    """
    defined: set[str] = set()
    for ch in active_channels:
        defined.add(ch["center_a"])
        defined.add(ch["center_b"])

    defined_list = [c for c in ALL_CENTER_NAMES if c in defined]
    undefined_list = [c for c in ALL_CENTER_NAMES if c not in defined]
    return defined_list, undefined_list


def _build_center_adjacency(active_channels: list[dict]) -> dict[str, set[str]]:
    """Build adjacency graph of defined centers connected by active channels.

    Args:
        active_channels: List of active channel dicts.

    Returns:
        Adjacency dict: {center_name: set of connected center names}.
    """
    adj: dict[str, set[str]] = defaultdict(set)
    for ch in active_channels:
        a, b = ch["center_a"], ch["center_b"]
        adj[a].add(b)
        adj[b].add(a)
    return dict(adj)


# [SOURCE] 参考: PyHD 开发博客 (https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library)
# 参考内容: 定义类型 (Definition Type) — BFS 连通分量算法
# 修改说明: 使用 Python BFS 实现，增加 Small/Large Split 判断

def determine_definition_type(
    defined_centers: list[str],
    active_channels: list[dict],
) -> tuple[str, str | None]:
    """Determine the definition type using connected components (BFS).

    Args:
        defined_centers: List of defined center names.
        active_channels: List of active channel dicts.

    Returns:
        Tuple of (definition_type, split_type).
        definition_type: "None" | "Single" | "Split" | "Triple Split" | "Quadruple Split"
        split_type: Only for "Split": "Small" or "Large". Otherwise None.
    """
    if not defined_centers:
        return "None", None

    adj = _build_center_adjacency(active_channels)
    visited: set[str] = set()
    components: list[set[str]] = []

    for center in defined_centers:
        if center in visited:
            continue
        # BFS from this center
        component: set[str] = set()
        queue = [center]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            component.add(current)
            for neighbor in adj.get(current, set()):
                if neighbor not in visited and neighbor in set(defined_centers):
                    queue.append(neighbor)
        components.append(component)

    num_components = len(components)

    if num_components == 0:
        return "None", None
    elif num_components == 1:
        return "Single", None
    elif num_components == 2:
        # Determine Small vs Large split
        # Small Split: the two components can be bridged by a single gate
        # (there exists an undefined channel where one gate is in component A
        #  and the other is in component B, and each gate's center matches)
        split_type = _determine_split_size(components, active_channels)
        return "Split", split_type
    elif num_components == 3:
        return "Triple Split", None
    else:
        return "Quadruple Split", None


def _determine_split_size(
    components: list[set[str]],
    active_channels: list[dict],
) -> str:
    """Determine if a split definition is Small or Large.

    Small Split: a single undefined gate activation could bridge the two components.
    Large Split: requires more than one gate to bridge.

    In practice: check if any single channel in the CHANNELS table connects
    a center in component A to a center in component B. If yes → Small Split.
    """
    comp_a, comp_b = components[0], components[1]

    for (gate_a, gate_b), (center_a, center_b) in CHANNELS.items():
        # Check if this channel bridges the two components
        if (center_a in comp_a and center_b in comp_b) or \
           (center_a in comp_b and center_b in comp_a):
            return "Small"

    return "Large"


def _has_path_to_throat(
    start_center: str,
    defined_centers: set[str],
    active_channels: list[dict],
) -> bool:
    """Check if there's a path from start_center to throat through defined channels.

    Uses BFS to search through defined centers connected by active channels.

    Args:
        start_center: Starting center name.
        defined_centers: Set of all defined center names.
        active_channels: List of active channel dicts.

    Returns:
        True if a path exists from start_center to "throat".
    """
    if start_center == "throat":
        return True
    if start_center not in defined_centers:
        return False

    adj = _build_center_adjacency(active_channels)
    visited: set[str] = set()
    queue = [start_center]

    while queue:
        current = queue.pop(0)
        if current == "throat":
            return True
        if current in visited:
            continue
        visited.add(current)
        for neighbor in adj.get(current, set()):
            if neighbor not in visited and neighbor in defined_centers:
                queue.append(neighbor)

    return False


# [SOURCE] 参考: SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign),
#   MCP_Human_design (https://github.com/dvvolkovv/MCP_Human_design)
# 参考内容: 类型判定 (Type determination) — 动力中心到喉咙路径搜索算法
# 修改说明: 从 C# 和 JS 翻译为 Python，使用 BFS 路径搜索

def determine_type(
    defined_centers: list[str],
    active_channels: list[dict],
) -> str:
    """Determine the Human Design Type.

    Rules (evaluated in order):
    1. No defined centers → Reflector
    2. Sacral defined + motor-to-throat path → Manifesting Generator
    3. Sacral defined → Generator
    4. Motor (root/solar_plexus/heart, NOT sacral) has path to throat → Manifestor
    5. Everything else → Projector

    "Has path" means: through defined channels, can traverse from the motor
    center to the throat center, possibly through intermediate defined centers.

    Args:
        defined_centers: List of defined center names.
        active_channels: List of active channel dicts.

    Returns:
        One of: "Generator", "Manifesting Generator", "Manifestor",
        "Projector", "Reflector".
    """
    defined_set = set(defined_centers)

    # Rule 1: No defined centers → Reflector
    if not defined_centers:
        return "Reflector"

    sacral_defined = "sacral" in defined_set

    # Check if any motor center has a path to throat
    # For MG check: include sacral as motor
    # For Manifestor check: exclude sacral
    non_sacral_motors = {"root", "solar_plexus", "heart"}

    if sacral_defined:
        # Check if there's a motor-to-throat connection (for MG vs Generator)
        # Motor centers for MG: any motor including sacral
        any_motor_to_throat = False
        for motor in MOTOR_CENTERS:
            if motor in defined_set and _has_path_to_throat(motor, defined_set, active_channels):
                any_motor_to_throat = True
                break

        if any_motor_to_throat:
            return "Manifesting Generator"
        else:
            return "Generator"

    # Sacral NOT defined
    # Rule 4: Non-sacral motor to throat → Manifestor
    for motor in non_sacral_motors:
        if motor in defined_set and _has_path_to_throat(motor, defined_set, active_channels):
            return "Manifestor"

    # Rule 5: Everything else
    return "Projector"


# [SOURCE] 参考: SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign)
# 参考内容: 权威判定 (Authority determination) — 优先级链
# 修改说明: 从 C# 翻译为 Python if-elif 链

def determine_authority(
    defined_centers: list[str],
    active_channels: list[dict],
    hd_type: str,
) -> str:
    """Determine the Inner Authority.

    Priority chain (first match wins):
    1. Solar Plexus defined → Emotional
    2. Sacral defined → Sacral
    3. Spleen defined → Splenic
    4. Heart defined AND directly connected to Throat → Ego Manifested
    5. Heart defined → Ego Projected
    6. G center defined AND directly connected to Throat → Self-Projected
    7. Reflector type → Lunar
    8. Everything else → Mental (also called "None" or "Environment")

    "Directly connected" means there's an active channel between the two centers.

    Args:
        defined_centers: List of defined center names.
        active_channels: List of active channel dicts.
        hd_type: The determined HD type string.

    Returns:
        One of: "Emotional", "Sacral", "Splenic", "Ego Manifested",
        "Ego Projected", "Self-Projected", "Lunar", "Mental".
    """
    defined_set = set(defined_centers)

    # Build direct connections for quick lookup
    direct_connections: set[tuple[str, str]] = set()
    for ch in active_channels:
        a, b = ch["center_a"], ch["center_b"]
        direct_connections.add((a, b))
        direct_connections.add((b, a))

    if "solar_plexus" in defined_set:
        return "Emotional"

    if "sacral" in defined_set:
        return "Sacral"

    if "spleen" in defined_set:
        return "Splenic"

    if "heart" in defined_set:
        if ("heart", "throat") in direct_connections:
            return "Ego Manifested"
        else:
            return "Ego Projected"

    if "g" in defined_set:
        if ("g", "throat") in direct_connections:
            return "Self-Projected"

    if hd_type == "Reflector":
        return "Lunar"

    return "Mental"


def determine_strategy(hd_type: str) -> str:
    """Determine the Strategy based on Type.

    Args:
        hd_type: The determined HD type.

    Returns:
        The strategy string.
    """
    strategies = {
        "Generator": "To Respond",
        "Manifesting Generator": "To Respond",
        "Manifestor": "To Inform",
        "Projector": "To Wait for Invitation",
        "Reflector": "To Wait a Lunar Cycle",
    }
    return strategies[hd_type]


def determine_profile(personality_sun_line: int, design_sun_line: int) -> str:
    """Determine the Profile from personality and design Sun lines.

    Args:
        personality_sun_line: Line number (1-6) of the personality Sun.
        design_sun_line: Line number (1-6) of the design Sun.

    Returns:
        Profile string in "X/Y" format (e.g., "4/6").
    """
    return f"{personality_sun_line}/{design_sun_line}"


# [SOURCE] 参考: SharpAstrology.HumanDesign (https://github.com/CReizner/SharpAstrology.HumanDesign),
#   humandesign_api (https://github.com/dturkuler/humandesign_api)
# 参考内容: 化身十字 (Incarnation Cross) — 轮廓首位决定十字类型
# 修改说明: 实现为简单映射函数

def determine_variables(
    personality_activations: list[dict],
    design_activations: list[dict],
) -> dict:
    """Determine the four Variables (Arrows) from activation Color and Tone.

    Variables are the four directional arrows shown at the corners of a
    Human Design bodygraph. Each arrow points Left (strategic/focused) or
    Right (receptive/peripheral), representing a person's cognitive and
    biological orientation.

    The four Variables are derived from Color values (1-3 = Left, 4-6 = Right)
    of specific activations:

      Arrow Position   │ Source                 │ Domain
      ─────────────────┼────────────────────────┼──────────────────────
      Top-Right        │ Personality Sun Color   │ Motivation (mind)
      Top-Left         │ Design Sun Color        │ Digestion (body)
      Bottom-Right     │ Personality North Node Color │ Perspective (mind)
      Bottom-Left      │ Design North Node Color │ Environment (body)

    Direction rule:
      Color 1-3 → "Left"  (strategic, focused, active)
      Color 4-6 → "Right" (receptive, peripheral, passive)

    Tone further specifies the quality within each Variable (1-6).

    Args:
        personality_activations: 13 conscious activations (must include
            color/tone fields from the extended gate mapping).
        design_activations: 13 unconscious activations.

    Returns:
        Dict with four Variable entries:
        {
            "digestion":   {"arrow": "Left"|"Right", "color": int, "tone": int},
            "environment": {"arrow": "Left"|"Right", "color": int, "tone": int},
            "motivation":  {"arrow": "Left"|"Right", "color": int, "tone": int},
            "perspective": {"arrow": "Left"|"Right", "color": int, "tone": int},
        }
    """
    def _find(activations: list[dict], planet: str) -> dict:
        return next(a for a in activations if a["planet"] == planet)

    def _arrow(color: int) -> str:
        return "Left" if color <= 3 else "Right"

    p_sun = _find(personality_activations, "sun")
    d_sun = _find(design_activations, "sun")
    p_node = _find(personality_activations, "north_node")
    d_node = _find(design_activations, "north_node")

    return {
        "digestion": {
            "arrow": _arrow(d_sun["color"]),
            "color": d_sun["color"],
            "tone": d_sun["tone"],
        },
        "environment": {
            "arrow": _arrow(d_node["color"]),
            "color": d_node["color"],
            "tone": d_node["tone"],
        },
        "motivation": {
            "arrow": _arrow(p_sun["color"]),
            "color": p_sun["color"],
            "tone": p_sun["tone"],
        },
        "perspective": {
            "arrow": _arrow(p_node["color"]),
            "color": p_node["color"],
            "tone": p_node["tone"],
        },
    }


def determine_incarnation_cross(
    personality_sun_gate: int,
    personality_earth_gate: int,
    design_sun_gate: int,
    design_earth_gate: int,
    profile: str,
) -> dict:
    """Determine the Incarnation Cross type and gates.

    The cross type depends on the first number of the profile:
    - Profile lines 1, 2, 3 → Right Angle Cross
    - Profile line 4 → Juxtaposition Cross
    - Profile lines 5, 6 → Left Angle Cross

    Args:
        personality_sun_gate: Gate of the personality Sun.
        personality_earth_gate: Gate of the personality Earth.
        design_sun_gate: Gate of the design Sun.
        design_earth_gate: Gate of the design Earth.
        profile: Profile string (e.g., "4/6").

    Returns:
        Dict with "type" and "gates" keys.
    """
    first_line = int(profile.split("/")[0])

    if first_line <= 3:
        cross_type = "Right Angle"
    elif first_line == 4:
        cross_type = "Juxtaposition"
    else:
        cross_type = "Left Angle"

    return {
        "type": cross_type,
        "gates": [personality_sun_gate, personality_earth_gate,
                  design_sun_gate, design_earth_gate],
    }

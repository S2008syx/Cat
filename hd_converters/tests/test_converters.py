"""
Tests for Graph Converter and Words Converter.

Uses a mock CalculatorOutput to verify both converters independently.
"""

import json
from datetime import datetime, timezone

from hd_calculator.models import CalculatorOutput
from hd_converters import convert_graph, convert_words, GraphData, WordsData


def _make_sample_output() -> CalculatorOutput:
    """Create a sample CalculatorOutput resembling a Generator 4/6 chart."""
    return CalculatorOutput(
        type="Generator",
        strategy="To Respond",
        authority="Sacral",
        profile="4/6",
        definition_type="Single",
        split_type=None,
        incarnation_cross_type="Right Angle",
        incarnation_cross_gates=[13, 7, 43, 23],
        defined_centers=["throat", "g", "sacral", "spleen"],
        undefined_centers=["head", "ajna", "heart", "solar_plexus", "root"],
        active_channels=[
            {"gate_a": 20, "gate_b": 10, "center_a": "throat", "center_b": "g"},
            {"gate_a": 34, "gate_b": 57, "center_a": "sacral", "center_b": "spleen"},
            {"gate_a": 10, "gate_b": 34, "center_a": "g", "center_b": "sacral"},
        ],
        personality_activations=[
            {"planet": "sun", "gate": 13, "line": 4, "longitude": 100.0},
            {"planet": "earth", "gate": 7, "line": 4, "longitude": 280.0},
            {"planet": "north_node", "gate": 10, "line": 3, "longitude": 200.0},
            {"planet": "south_node", "gate": 15, "line": 3, "longitude": 20.0},
            {"planet": "moon", "gate": 20, "line": 5, "longitude": 50.0},
            {"planet": "mercury", "gate": 34, "line": 2, "longitude": 150.0},
            {"planet": "venus", "gate": 1, "line": 1, "longitude": 250.0},
            {"planet": "mars", "gate": 43, "line": 6, "longitude": 300.0},
            {"planet": "jupiter", "gate": 8, "line": 3, "longitude": 45.0},
            {"planet": "saturn", "gate": 23, "line": 2, "longitude": 60.0},
            {"planet": "uranus", "gate": 2, "line": 4, "longitude": 190.0},
            {"planet": "neptune", "gate": 57, "line": 1, "longitude": 270.0},
            {"planet": "pluto", "gate": 46, "line": 5, "longitude": 170.0},
        ],
        design_activations=[
            {"planet": "sun", "gate": 43, "line": 6, "longitude": 12.0},
            {"planet": "earth", "gate": 23, "line": 6, "longitude": 192.0},
            {"planet": "north_node", "gate": 34, "line": 1, "longitude": 155.0},
            {"planet": "south_node", "gate": 20, "line": 1, "longitude": 335.0},
            {"planet": "moon", "gate": 57, "line": 3, "longitude": 265.0},
            {"planet": "mercury", "gate": 10, "line": 5, "longitude": 205.0},
            {"planet": "venus", "gate": 25, "line": 2, "longitude": 10.0},
            {"planet": "mars", "gate": 51, "line": 4, "longitude": 5.0},
            {"planet": "jupiter", "gate": 42, "line": 3, "longitude": 340.0},
            {"planet": "saturn", "gate": 3, "line": 1, "longitude": 350.0},
            {"planet": "uranus", "gate": 27, "line": 6, "longitude": 35.0},
            {"planet": "neptune", "gate": 22, "line": 2, "longitude": 320.0},
            {"planet": "pluto", "gate": 36, "line": 4, "longitude": 315.0},
        ],
        design_utc=datetime(1990, 7, 10, 12, 0, tzinfo=timezone.utc),
        all_active_gates=[1, 2, 3, 7, 8, 10, 13, 15, 20, 22, 23, 25, 27,
                          34, 36, 42, 43, 46, 51, 57],
    )


def _make_reflector_output() -> CalculatorOutput:
    """Create a minimal Reflector output (no defined centers)."""
    return CalculatorOutput(
        type="Reflector",
        strategy="To Wait a Lunar Cycle",
        authority="Lunar",
        profile="5/1",
        definition_type="None",
        split_type=None,
        incarnation_cross_type="Left Angle",
        incarnation_cross_gates=[1, 2, 7, 13],
        defined_centers=[],
        undefined_centers=["head", "ajna", "throat", "g", "heart",
                           "sacral", "solar_plexus", "spleen", "root"],
        active_channels=[],
        personality_activations=[
            {"planet": "sun", "gate": 1, "line": 5, "longitude": 250.0},
            {"planet": "earth", "gate": 2, "line": 5, "longitude": 70.0},
        ],
        design_activations=[
            {"planet": "sun", "gate": 7, "line": 1, "longitude": 110.0},
            {"planet": "earth", "gate": 13, "line": 1, "longitude": 290.0},
        ],
        design_utc=datetime(1990, 7, 10, 12, 0, tzinfo=timezone.utc),
        all_active_gates=[1, 2, 7, 13],
    )


# ==================== Graph Converter Tests ====================

class TestGraphConverter:

    def test_returns_graph_data(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        assert isinstance(graph, GraphData)

    def test_nine_centers(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        assert len(graph.centers) == 9

    def test_center_defined_status(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        center_map = {c["id"]: c for c in graph.centers}
        assert center_map["sacral"]["defined"] is True
        assert center_map["g"]["defined"] is True
        assert center_map["head"]["defined"] is False
        assert center_map["root"]["defined"] is False

    def test_center_has_position_and_shape(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        for center in graph.centers:
            assert "position" in center
            assert "x" in center["position"]
            assert "y" in center["position"]
            assert 0 <= center["position"]["x"] <= 1
            assert 0 <= center["position"]["y"] <= 1
            assert center["shape"] in ("square", "triangle", "diamond")

    def test_channels_only_active(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        assert len(graph.channels) == len(output.active_channels)

    def test_channel_color_logic(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        ch_map = {(c["gate_a"], c["gate_b"]): c for c in graph.channels}
        # Channel 20-10: gate 20 in both personality and design, gate 10 in both
        # → has_p=True, has_d=True → mixed
        ch_20_10 = ch_map.get((20, 10))
        assert ch_20_10 is not None
        assert ch_20_10["color"] == "mixed"

    def test_gate_color_both(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        gate_map = {g["gate"]: g for g in graph.gates}
        # Gate 10: in personality (north_node) AND design (mercury) → both
        assert gate_map[10]["color"] == "both"

    def test_gate_color_personality_only(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        gate_map = {g["gate"]: g for g in graph.gates}
        # Gate 13: only in personality (sun) → personality
        assert gate_map[13]["color"] == "personality"

    def test_gate_color_design_only(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        gate_map = {g["gate"]: g for g in graph.gates}
        # Gate 3: only in design (saturn) → design
        assert gate_map[3]["color"] == "design"

    def test_gate_activated_by(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        gate_map = {g["gate"]: g for g in graph.gates}
        # Gate 34: personality mercury line 2, design north_node line 1
        g34 = gate_map[34]
        assert len(g34["activated_by"]) == 2
        sides = {a["side"] for a in g34["activated_by"]}
        assert sides == {"personality", "design"}

    def test_gate_count_matches_all_active(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        assert len(graph.gates) == len(output.all_active_gates)

    def test_meta_fields(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        assert graph.meta["type"] == "Generator"
        assert graph.meta["profile"] == "4/6"
        assert graph.meta["authority"] == "Sacral"

    def test_to_dict_json_serializable(self):
        output = _make_sample_output()
        graph = convert_graph(output)
        d = graph.to_dict()
        # Must not raise
        json_str = json.dumps(d, ensure_ascii=False)
        assert isinstance(json_str, str)
        assert "Generator" in json_str

    def test_reflector_no_channels(self):
        output = _make_reflector_output()
        graph = convert_graph(output)
        assert len(graph.channels) == 0
        assert all(c["defined"] is False for c in graph.centers)


# ==================== Words Converter Tests ====================

class TestWordsConverter:

    def test_returns_words_data(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert isinstance(words, WordsData)

    def test_type_info(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert words.type_info["key"] == "Generator"
        assert words.type_info["name_zh"] == "生产者"
        assert "strategy_zh" in words.type_info

    def test_authority_info(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert words.authority_info["key"] == "Sacral"
        assert words.authority_info["name_zh"] == "骶骨权威"
        assert "description" in words.authority_info

    def test_profile_info(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert words.profile_info["key"] == "4/6"
        assert words.profile_info["name_zh"] == "机会者/榜样"
        assert words.profile_info["line1"]["name_zh"] == "机会者"
        assert words.profile_info["line2"]["name_zh"] == "榜样"

    def test_definition_info(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert words.definition_info["key"] == "Single"
        assert words.definition_info["name_zh"] == "单一定义"

    def test_cross_info(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert words.cross_info["type"] == "Right Angle"
        assert "斯芬克斯" in words.cross_info["name_zh"]
        assert words.cross_info["gates"] == [13, 7, 43, 23]

    def test_nine_center_infos(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert len(words.center_infos) == 9
        sacral = next(c for c in words.center_infos if c["id"] == "sacral")
        assert sacral["defined"] is True
        assert sacral["theme"] != ""
        assert sacral["not_self_theme"] != ""

    def test_channel_infos_match_active(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert len(words.channel_infos) == len(output.active_channels)
        for ch_info in words.channel_infos:
            assert "name_zh" in ch_info
            assert "name_en" in ch_info
            assert "theme" in ch_info

    def test_gate_infos_count(self):
        output = _make_sample_output()
        words = convert_words(output)
        assert len(words.gate_infos) == len(output.all_active_gates)

    def test_gate_infos_fields(self):
        output = _make_sample_output()
        words = convert_words(output)
        for gi in words.gate_infos:
            assert "gate" in gi
            assert "name_zh" in gi
            assert "name_en" in gi
            assert "center" in gi
            assert "keynote" in gi
            assert "activated_by" in gi

    def test_to_dict_json_serializable(self):
        output = _make_sample_output()
        words = convert_words(output)
        d = words.to_dict()
        json_str = json.dumps(d, ensure_ascii=False)
        assert isinstance(json_str, str)
        assert "生产者" in json_str

    def test_reflector_words(self):
        output = _make_reflector_output()
        words = convert_words(output)
        assert words.type_info["key"] == "Reflector"
        assert words.type_info["name_zh"] == "反映者"
        assert words.authority_info["key"] == "Lunar"
        assert words.definition_info["key"] == "None"
        assert len(words.channel_infos) == 0

    def test_left_angle_cross(self):
        output = _make_reflector_output()
        words = convert_words(output)
        assert words.cross_info["type"] == "Left Angle"
        assert "左角度" in words.cross_info["name_zh"]


# ==================== Data Completeness Tests ====================

class TestDataCompleteness:

    def test_64_gates_in_data(self):
        from hd_converters.data.gate_names import GATE_DATA
        assert len(GATE_DATA) == 64
        for g in range(1, 65):
            assert g in GATE_DATA, f"Gate {g} missing from GATE_DATA"

    def test_36_channels_in_data(self):
        from hd_converters.data.channel_names import CHANNEL_DATA
        assert len(CHANNEL_DATA) == 36

    def test_9_centers_in_data(self):
        from hd_converters.data.center_names import CENTER_DATA
        assert len(CENTER_DATA) == 9

    def test_5_types_in_data(self):
        from hd_converters.data.type_names import TYPE_DATA
        assert len(TYPE_DATA) == 5

    def test_8_authorities_in_data(self):
        from hd_converters.data.authority_names import AUTHORITY_DATA
        assert len(AUTHORITY_DATA) == 8

    def test_12_profiles_in_data(self):
        from hd_converters.data.profile_names import PROFILE_DATA
        assert len(PROFILE_DATA) == 12

    def test_6_lines_in_data(self):
        from hd_converters.data.profile_names import LINE_NAMES
        assert len(LINE_NAMES) == 6

    def test_64_crosses_in_data(self):
        from hd_converters.data.cross_names import CROSS_DATA
        assert len(CROSS_DATA) == 64

    def test_64_gate_layout_mappings(self):
        from hd_converters.data.bodygraph_layout import GATE_TO_CENTER
        assert len(GATE_TO_CENTER) == 64

    def test_gate_names_have_required_fields(self):
        from hd_converters.data.gate_names import GATE_DATA
        for g, data in GATE_DATA.items():
            assert "gate" in data
            assert "name_zh" in data
            assert "name_en" in data
            assert "center" in data
            assert "keynote" in data

    def test_channel_names_have_required_fields(self):
        from hd_converters.data.channel_names import CHANNEL_DATA
        for key, data in CHANNEL_DATA.items():
            assert "gates" in data
            assert "name_zh" in data
            assert "name_en" in data
            assert "centers" in data
            assert "theme" in data

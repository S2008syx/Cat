"""
Data models for Graph and Words converters.

Both GraphData and WordsData provide to_dict() for JSON serialization.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GraphData:
    """Structured data for front-end Bodygraph rendering."""

    centers: list[dict] = field(default_factory=list)
    channels: list[dict] = field(default_factory=list)
    gates: list[dict] = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "centers": self.centers,
            "channels": self.channels,
            "gates": self.gates,
            "meta": self.meta,
        }


@dataclass
class WordsData:
    """Structured keyword/name data for front-end display."""

    type_info: dict = field(default_factory=dict)
    authority_info: dict = field(default_factory=dict)
    profile_info: dict = field(default_factory=dict)
    definition_info: dict = field(default_factory=dict)
    cross_info: dict = field(default_factory=dict)
    center_infos: list[dict] = field(default_factory=list)
    channel_infos: list[dict] = field(default_factory=list)
    gate_infos: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "type_info": self.type_info,
            "authority_info": self.authority_info,
            "profile_info": self.profile_info,
            "definition_info": self.definition_info,
            "cross_info": self.cross_info,
            "center_infos": self.center_infos,
            "channel_infos": self.channel_infos,
            "gate_infos": self.gate_infos,
        }

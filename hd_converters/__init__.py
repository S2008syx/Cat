"""
Human Design Data Converters

Two parallel converters that transform CalculatorOutput into front-end ready data:
  - convert_graph(): GraphData for Bodygraph rendering
  - convert_words(): WordsData for keyword/name display

Usage:
    from hd_calculator import calculate
    from hd_converters import convert_graph, convert_words

    output = calculate(birth_utc=..., latitude=..., longitude=...)
    graph = convert_graph(output)
    words = convert_words(output)

    # JSON serializable
    graph_dict = graph.to_dict()
    words_dict = words.to_dict()
"""

from .graph_converter import convert_graph
from .words_converter import convert_words
from .models import GraphData, WordsData

__all__ = ["convert_graph", "convert_words", "GraphData", "WordsData"]

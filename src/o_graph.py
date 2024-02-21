import json

from graph import EdgeAttributes, Graph, NodeAttributes
from typing_extensions import override


class OutsideGraph(Graph):
    def __init__(self, path=None):
        super(OutsideGraph, self).__init__()

        self.COLORS = {
            "road": "#84DCC6",
            "exit": "#FF686B"
        }
        self.PREFIXES = {
            "c": "road",
            "e": "exit"
        }
        self.load_graph(path) if path else None
    
    @override   
    def load_graph(self, path: str) -> None:
        self.name = self.get_graph_name(path)
        print(self.name)
        campus = json.load(open(path))
        nodes = list(campus.values())
        print(nodes)


    
graph = OutsideGraph(f"data/exits_positions/solbosch_map_updated.json")
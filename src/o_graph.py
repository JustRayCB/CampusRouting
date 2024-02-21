import json

from graph import EdgeAttributes, Graph, NodeAttributes
from typing_extensions import override
from typing import Any, Dict, List


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
    
    def get_name_from_id(self, id: str) -> str:
        if id[0] == "c":
            return f"Road {id[1:]}"
        elif id[0] == "e":
            entry_number, building = id.split("_")[1], id[1:id.index('_')]
            return f"Entry {entry_number} of building {building}"
        else:
            raise ValueError(f"Invalid id: {id}")
    
    @override   
    def load_graph(self, path: str) -> None:
        self.name = self.get_graph_name(path)
        print(self.name)
        campus_data = json.load(open(path))
        campus_name = list(campus_data.keys())[0]
        nodes = list(campus_data[campus_name])
        for node in nodes:
            self.add_node_(node)

    @override
    def add_node_(self, node_data: Dict[str, Any]) -> None:
        nodes_attrs: Dict[str, Any] = {}
        node_name: str = ""
        a_type, a_color = NodeAttributes.TYPE, NodeAttributes.COLOR
        for key, value in node_data.items():
            if key == "id":
                node_name = self.get_name_from_id(value)
                nodes_attrs[a_type] = self.PREFIXES[value[0]]
                nodes_attrs[a_color] = self.COLORS[self.PREFIXES[value[0]]]
            elif key == "neighbors":
                self.add_neighbors(value, node_name)
            else:
                nodes_attrs[key] = value
        self.add_node(node_name, **nodes_attrs)

    @override
    def add_neighbors(self, neighbors: Dict, source: str) -> None:
        edges = []
        for neighbor in neighbors:
            edge_data = {}
            target_name = self.get_name_from_id(neighbor["id"])
            edge_data[EdgeAttributes.WEIGHT] = neighbor[EdgeAttributes.WEIGHT]
            edge = (source, target_name, edge_data)
            edges.append(edge)
        self.add_edges_from(edges)
    
graph = OutsideGraph(f"data/exits_positions/solbosch_map_updated.json")
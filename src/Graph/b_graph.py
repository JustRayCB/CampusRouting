"""Graph representation of the building.

:Author: Rayan Contuliano Bravo 
:Date: 12/02/2024
:Description: This class is used to represent a building as a graph using the networkx library.
"""

import json
from typing import Any, Dict, List

from typing_extensions import override

from .graph import EdgeAttributes, Graph, GraphTypes, NodeAttributes


class BNodeAttributes(NodeAttributes):
    """Attributes of a node in a Building."""

    FLOOR = "floor"


class BEdgeAttributes(EdgeAttributes):
    """Attributes of an edge in a Building."""

    DIRECTION = "direction"


class BuildingGraph(Graph):

    def __init__(self, path=None):
        super(BuildingGraph, self).__init__()
        self.COLORS = {
            "hallway": "#21243D",
            "class": "#88E1F2",
            "toilet": "#FFD082",
            "unknown": "#FF7C7C",
            "stair": "#CCCCFF",
            "lift": "#AF7AC5",
            "entrance": "#FFD700",
        }
        self.PREFIXES = {
            "H": "hallway",
            "E": "class",
            "T": "toilet",
            "U": "unknown",
            "S": "stair",
            "L": "lift",
            "e": "entrance",
        }
        self.n_floors = -1
        self.current_floor = -1
        self.graph_type = GraphTypes.BUILDING
        self.load_graph(path) if path else None

    def is_elevator_or_stair(self, id: str) -> bool:
        """
        Check if the room is an elevator or a stair.

        :param id: The id of the room.
        :returns: True if the room is an elevator or a stair, False otherwise.
        """
        node_type: str = self.get_type_from_id(id)
        return node_type == self.PREFIXES["S"] or node_type == self.PREFIXES["L"]

    def is_entrance(self, id: str) -> bool:
        node_type: str = self.get_type_from_id(id)
        return node_type == self.PREFIXES["e"]

    def get_entrances(self):
        """Get all the entrances of the building."""
        return [node for node in self.nodes if self.is_entrance(node)]

    @override
    def get_name_from_id(self, id: str) -> str:
        """Get the name of a node from its id.

        :param id: The id of the node.
        :param floor: The floor of the node.
        :returns: The name of the node.
        """
        if self.is_elevator_or_stair(id) or self.is_entrance(id):
            # Elevators and Stairs do not have a floor cause they are the same on all floors
            return id
        return f"{id}_{self.current_floor}"

    @override
    def load_graph(self, path: str) -> None:
        self.name = self.get_graph_name(path)
        print(f"Building graph {self.name} created.")
        building_data = json.load(open(path))
        floors: List[str] = list(building_data.keys())
        self.n_floors = len(floors)
        for current_floor in floors:
            self.current_floor = int(current_floor)
            rooms: List[Dict] = building_data[current_floor]
            for room in rooms:
                self.add_node_(room)

    @override
    def add_node_(self, node_data: Dict[str, Any]) -> None:
        node_attrs: Dict[str, Any] = {}
        node_name: str = ""
        a_type, a_color, a_floor = (
            BNodeAttributes.TYPE,
            BNodeAttributes.COLOR,
            BNodeAttributes.FLOOR,
        )
        for key, value in node_data.items():
            if key == "id":
                node_name = self.get_name_from_id(value)
                node_attrs[a_type] = self.get_type_from_id(value)
                node_attrs[a_color] = self.get_color_from_type(node_attrs[a_type])
                node_attrs[a_floor] = self.current_floor
            elif key == "neighbors":
                # Add the attribute of the edges
                self.add_neighbors(value, node_name)
            else:
                node_attrs[key] = value
        self.add_node(node_name, **node_attrs)

    @override
    def add_neighbors(self, neighbors: Dict, source: str) -> None:
        edges = []  # List of all the edges that start from the source node
        weight, direction = BEdgeAttributes.WEIGHT, BEdgeAttributes.DIRECTION
        for neighbor in neighbors:
            edge_attributes: Dict[str, Any] = {}
            target_name = self.get_name_from_id(neighbor[BNodeAttributes.ID])
            edge_attributes[weight] = neighbor[weight]
            directions = {}
            data_direction = neighbor[direction]
            if type(data_direction) is str:
                directions = data_direction  # If there is only one direction (not the boys band 😆)
            else:
                for predecessor in data_direction:
                    if predecessor == "null" or predecessor is None:
                        # There can be no predecessor e.g First node of a building, or we come from a cul-de-sac
                        directions[predecessor] = data_direction[predecessor]
                    else:
                        # keep in mind that the predecessor is the predecessor of the source before reaching target
                        # The direction we need to take depends of the predecessor
                        directions[self.get_name_from_id(predecessor)] = neighbor[direction][
                            predecessor
                        ]
            if self.is_elevator_or_stair(source) and self.is_elevator_or_stair(target_name):
                raise ValueError("Elevators and Stairs cannot be connected to each other.")
            edge_attributes[direction] = directions
            edge = (source, target_name, edge_attributes)
            edges.append(edge)
        self.add_edges_from(edges)

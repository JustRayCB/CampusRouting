"""Graph representation of the building.

:Author: Rayan Contuliano Bravo 
:Date: 02/08/2024
:Description: This class is used to represent a building as a graph using the networkx library.
"""

import json
from enum import Enum
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import networkx as nx


class NodeAttributes(Enum):
    """Attributes of a node."""

    NAME = "name"
    COLOR = "color"
    TYPE = "type"
    FLOOR = "floor"


class EdgeAttributes(Enum):
    """Attributes of an edge."""

    WEIGHT = "weight"
    DIRECTION = "direction"


class BuildingGraph(nx.DiGraph):
    """Represents a building as a graph."""

    def __init__(self, path=None):
        super(BuildingGraph, self).__init__()
        self.COLORS = {
            "hallway": "#21243D",
            "class": "#88E1F2",
            "toilet": "#FFD082",
            "unknown": "#FF7C7C",
            "stair": "#CCCCFF",
            "lift": "#AF7AC5",
        }
        self.PREFIXES = {
            "H": "hallway",
            "E": "class",
            "T": "toilet",
            "U": "unknown",
            "S": "stair",
            "L": "lift",
        }
        self.n_floors = -1
        self.load_building(path) if path else None

    def get_type_from_id(self, id: str) -> str:
        """Get the type of a node from its id.

        :param id: The id of the node.
        :returns: The type of the node.
        """
        for prefix, room_type in self.PREFIXES.items():
            if id.startswith(prefix):
                return room_type
        raise ValueError(f"Invalid id: {id} for a room.")

    def get_name_from_id(self, id: str, floor: str) -> str:
        """Get the name of a node from its id.

        :param id: The id of the node.
        :param floor: The floor of the node.
        :returns: The name of the node.
        """
        if self.is_elevator_or_stair(id):
            # Elevators and Stairs do not have a floor cause they are the same on all floors
            return id
        return f"{id}_{floor}"

    def is_elevator_or_stair(self, id: str) -> bool:
        """
        Check if the room is an elevator or a stair.

        :param id: The id of the room.
        :returns: True if the room is an elevator or a stair, False otherwise.
        """
        node_type: str = self.get_type_from_id(id)
        return node_type == self.PREFIXES["S"] or node_type == self.PREFIXES["L"]

    def get_color_from_type(self, node_type: str) -> str:
        """Get the color of a node from its type.

        :param node_type: The type of the node.
        :returns: The color of the node.
        """
        return self.COLORS[node_type]

    def add_room(self, data: Dict, floor: str) -> None:
        """
        Setup a node with its attributes and edges (attributes included) in the graph.

        :param graph: The graph in which the node will be added.
        :param data: The data of the node taken from the json file.
        :param floor: The floor of the node.
        :returns: The name of the node.
        """
        node_attributes: Dict[str, str] = {}
        node_name = ""
        a_type, a_color, a_floor = (
            NodeAttributes.TYPE.value,
            NodeAttributes.COLOR.value,
            NodeAttributes.FLOOR.value,
        )
        for key, value in data.items():
            if key == "id":
                node_name = self.get_name_from_id(value, floor)
                node_attributes[a_type] = self.get_type_from_id(value)
                node_attributes[a_color] = self.get_color_from_type(node_attributes[a_type])
                node_attributes[a_floor] = floor
            elif key == "neighbors":
                # Add the attribute to the edges
                self.add_neighbors(value, node_name, floor)
            else:
                # Add the others attributes to the node
                node_attributes[key] = value
        self.add_node(node_name, **node_attributes)

    def add_neighbors(self, neighbors: Dict, source: str, floor: str) -> None:
        """
        Setup edges with its attributes in the graph according to the neighbors of the source node.

        :param graph: The graph in which the edges will be added.
        :param neighbors: The neighbors of the source node.
        :param source: The source node.
        :param floor: The floor of the source node and its neighbors.
        """
        edges = []  # List of all the edges that start from the source node
        weight, direction = EdgeAttributes.WEIGHT.value, EdgeAttributes.DIRECTION.value
        for neighbor in neighbors:
            edge_attributes: Dict[str, Any] = {}
            target_name = self.get_name_from_id(neighbor["id"], floor)
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
                        directions[self.get_name_from_id(predecessor, floor)] = neighbor[direction][
                            predecessor
                        ]
            if self.is_elevator_or_stair(source) and self.is_elevator_or_stair(target_name):
                raise ValueError("Elevators and Stairs cannot be connected to each other.")
            edge_attributes[direction] = directions
            edge = (source, target_name, edge_attributes)
            edges.append(edge)
        self.add_edges_from(edges)

    def load_building(self, path: str):
        self.name = path.split("/")[-1].split(".")[0]
        print(self.name)
        building_data = json.load(open(path))
        floors: List[str] = list(building_data.keys())
        for current_floor in floors:
            rooms: List[Dict] = building_data[current_floor]
            for room in rooms:
                self.add_room(room, current_floor)

    def show_graph(self, show: bool = True):
        """
        Show the graph with its nodes and edges. If a source and a target are given, the shortest path will be highlighted.
        """
        colors = [self.nodes[node]["color"] for node in self.nodes]
        pos = nx.spring_layout(self)
        nx.draw(
            self,
            pos,
            with_labels=True,
            node_color=colors,
            font_size=8,
            font_color="white",
            node_size=800,
        )
        if show:
            plt.show()
        else:
            return pos

    def show_path(self, path: List[str]):
        pos = self.show_graph(False)
        nx.draw_networkx_edges(
            self,
            pos,
            edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
            edge_color="red",
            width=2,
        )
        plt.show()

    def default_dijkstra(self, source: str, target: str):
        return nx.shortest_path(self, source, target, weight="weight")

import json
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import networkx as nx

"""
NOTE: Nodes Attributes:
    We can add a node and its attributes to the graph using the add_nodes_from method. 
    For example: G.add_nodes_from([(1, {"color": "blue"}), (2, {"color": "green"})])
    Then all the nodes will have the attribute color with the corresponding value.
    All the nodes do not need to have the same attributes.
NOTE: Edges Attributes:
    Using the add_edges_from method, we can add edges and their attributes to the graph. 
    For example: G.add_edges_from([(1, 2, {"weight": 3.1415}), (3, 4, {"weight": 2.718})])
WARNING: 
    If you add a node that is already in the graph, the attributes will be updated but not deleted or duplicated
    I assume it is the same for edges.
"""

DATA_DIR = "data/plans/Solbosch/"
BUILDINGS = ["P1"]

COLORS = {
    "hallway": "#21243D",
    "class": "#88E1F2",
    "toilet": "#FFD082",
    "unknown": "#FF7C7C",
    "stair": "#CCCCFF",
    "lift": "#AF7AC5",
}

PREFIXES = {
    "H": "hallway",
    "E": "class",
    "T": "toilet",
    "U": "unknown",
    "S": "stair",
    "L": "lift",
}


def load_json(file_path) -> Dict:
    """Load a json file and return its content as a dictionary."""
    with open(file_path, "r") as file:
        return json.load(file)


def get_type_from_id(id: str) -> str:
    """Return the type of the room from its id."""
    for prefix, room_type in PREFIXES.items():
        if id.startswith(prefix):
            return room_type
    raise ValueError(f"Invalid id: {id} for a room.")


def is_elevator_or_stair(id: str) -> bool:
    """Return True if the room is an elevator or a stair."""
    node_type: str = get_type_from_id(id)
    return node_type == PREFIXES["S"] or node_type == PREFIXES["L"]
    # return id.startswith(PREFIXES["S"]) or id.startswith(PREFIXES["L"])


def get_name_from_id(id: str, floor: str) -> str:
    """Return the name of the room from its id and floor."""
    # node_type: str = get_type_from_id(id)
    # if node_type == PREFIXES["S"] or node_type == PREFIXES["L"]:
    if is_elevator_or_stair(id):
        # Elevators and Stairs do not have a floor
        return id
    return f"{id}_{floor}"


def setup_edges(graph: nx.Graph, neighbors: List[Dict], source: str, floor: str) -> None:
    """Setup an edge with its attributes in the graph."""
    edges = []
    # (source, target, attributes: dict)
    for neighbor in neighbors:
        edge_attributes: Dict[str, Any] = {}
        target_name = get_name_from_id(neighbor["id"], floor)
        edge_attributes["weight"] = neighbor["weight"]
        direction = {}
        data_direction = neighbor["direction"]
        if type(data_direction) is str:
            direction = data_direction  # If there is only one direction (not the boys band 😆)
        else:
            for predecessor in data_direction:
                if predecessor == "null" or predecessor is None:
                    # There can be no predecessor e.g First node of a building, or we come from a cul-de-sac
                    direction[predecessor] = data_direction[predecessor]
                else:
                    # keep in mind that the predecessor is the predecessor of the source before reaching target
                    # The direction we need to take depends of the predecessor
                    direction[get_name_from_id(predecessor, floor)] = neighbor["direction"][
                        predecessor
                    ]
        edge = (source, target_name, edge_attributes)
        edges.append(edge)
    graph.add_edges_from(edges)


def setup_node(graph: nx.Graph, data: Dict, floor: str) -> None:
    """Setup a node with its attributes and edges (attributes included) in the graph."""
    node_attributes: Dict[str, str] = {}
    node_name = ""
    for key, value in data.items():
        if key == "id":
            node_name = get_name_from_id(value, floor)
            node_attributes["type"] = get_type_from_id(value)
            node_attributes["color"] = COLORS[node_attributes["type"]]
        elif key == "neighbors":
            # Add the attribute to the edges
            setup_edges(graph, value, node_name, floor)
        else:
            # Add the attribute to the node
            node_attributes[key] = value
    graph.add_node(node_name, **node_attributes)


def build_graph(data: Dict) -> nx.DiGraph:
    """Build a graph from the data of a building struture previously retrieved from json file."""
    graph = nx.DiGraph()
    floors: List[str] = list(data.keys())
    for current_floor in floors:
        rooms: List[Dict] = data[current_floor]
        print("For floor: ", current_floor)
        for room in rooms:
            setup_node(graph, room, current_floor)
    return graph


if __name__ == "__main__":
    buildings_data: Dict[str, Dict] = {}
    buildings_graph: Dict[str, nx.Graph] = {}
    for building in BUILDINGS:
        file_path = DATA_DIR + building + "/" + building + ".json"
        data = load_json(file_path)
        buildings_data[building] = data
        buildings_graph[building] = build_graph(data)
        colors = [
            buildings_graph[building].nodes[node]["color"]
            for node in buildings_graph[building].nodes
        ]
        pos = nx.spring_layout(buildings_graph[building])
        nx.draw(
            buildings_graph[building],
            pos,
            with_labels=True,
            node_color=colors,
            font_size=8,
            font_color="white",
            node_size=800,
        )
        # nx.draw(buildings_graph[building], with_labels=True, node_color=colors)
        plt.show()

""" 
@Author: Rayan Contuliano Bravo
@Date: 07/02/2024
@Description: This script is used to convert the json file of a building structure to a networkx graph.
"""

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


def load_json(file_path: str) -> Dict:
    """
    Load a json file and return its content as a dictionary.

    :param file_path: The path of the json file to load.
    :returns: The content of the json file as a dictionary according to the json format.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def get_type_from_id(id: str) -> str:
    """
    According to the id of a room, return its type.

    NOTE: The id of a room is always composed of a prefix and a number.
    :param id: The id of the room.
                the type of the room and a number.
    :returns: The type of the room.
    """
    for prefix, room_type in PREFIXES.items():
        if id.startswith(prefix):
            return room_type
    raise ValueError(f"Invalid id: {id} for a room.")


def is_elevator_or_stair(id: str) -> bool:
    """
    Check if the room is an elevator or a stair.

    :param id: The id of the room.
    :returns: True if the room is an elevator or a stair, False otherwise.
    """
    node_type: str = get_type_from_id(id)
    return node_type == PREFIXES["S"] or node_type == PREFIXES["L"]


def get_name_from_id(id: str, floor: str) -> str:
    """
    Fix the name of a room by adding the floor to its id according to it's type.
    The floor is needed to differentiate the rooms with the same id
    (according to the plans) but in different floors.

    :param id: The id of the room.
    :param floor: The floor of the room.
    :returns: The name of the room.
    """
    if is_elevator_or_stair(id):
        # Elevators and Stairs do not have a floor cause they are the same on all floors
        return id
    return f"{id}_{floor}"


def setup_edges(graph: nx.Graph, neighbors: List[Dict], source: str, floor: str) -> None:
    """
    Setup edges with its attributes in the graph according to the neighbors of the source node.

    :param graph: The graph in which the edges will be added.
    :param neighbors: The neighbors of the source node.
    :param source: The source node.
    :param floor: The floor of the source node and its neighbors.
    """
    edges = []  # List of all the edges that start from the source node
    for neighbor in neighbors:
        edge_attributes: Dict[str, Any] = {}
        target_name = get_name_from_id(neighbor["id"], floor)
        edge_attributes["weight"] = neighbor["weight"]
        directions = {}
        data_direction = neighbor["direction"]
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
                    directions[get_name_from_id(predecessor, floor)] = neighbor["direction"][
                        predecessor
                    ]
        if is_elevator_or_stair(source) and is_elevator_or_stair(target_name):
            raise ValueError("Elevators and Stairs cannot be connected to each other.")
        edge_attributes["direction"] = directions
        edge = (source, target_name, edge_attributes)
        edges.append(edge)
    graph.add_edges_from(edges)


def setup_node(graph: nx.Graph, data: Dict, floor: str) -> None:
    """
    Setup a node with its attributes and edges (attributes included) in the graph.

    :param graph: The graph in which the node will be added.
    :param data: The data of the node taken from the json file.
    :param floor: The floor of the node.
    :returns: The name of the node.
    """
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
            # Add the others attributes to the node
            node_attributes[key] = value
    graph.add_node(node_name, **node_attributes)


def build_graph(data: Dict) -> nx.DiGraph:
    """
    Build a graph from the data of a building struture previously retrieved from json file.

    :param data: The data of the building structure.
    :returns: The directed graph of the building structure.
    """
    graph = nx.DiGraph()
    floors: List[str] = list(data.keys())
    for current_floor in floors:
        rooms: List[Dict] = data[current_floor]
        for room in rooms:
            setup_node(graph, room, current_floor)
    return graph


def check_edges(graph: nx.Graph):
    """Check the edges of the graph."""
    edges = graph.edges.data()
    while True:
        found = False
        i = input("Enter the name of the source and destination: ")
        if i == "exit":
            break
        for edge in edges:
            source, target = i.split()
            if source in edge and target in edge:
                found = True
                print(edge)
        if not found:
            print("No edge found.")


def show_graph(graph: nx.DiGraph, sota: tuple = ()):
    """
    Show the graph with its nodes and edges. If a source and a target are given, the shortest path will be highlighted.

    :param graph: The graph to show.
    :param sota: The source and the target of which the shortest path will be highlighted if it exists.
    """
    colors = [graph.nodes[node]["color"] for node in graph.nodes]
    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=colors,
        font_size=8,
        font_color="white",
        node_size=800,
    )

    plt.show()


def shortest_path(graph: nx.Graph, source: str, target: str):
    """Find the shortest path between two nodes in the graph using NetworkX algorithm."""
    return nx.shortest_path(graph, source, target, weight="weight")


def main():
    buildings_data: Dict[str, Dict] = {}
    buildings_graph: Dict[str, nx.DiGraph] = {}
    for building in BUILDINGS:
        file_path = DATA_DIR + building + "/" + building + ".json"
        data = load_json(file_path)
        buildings_data[building] = data
        buildings_graph[building] = build_graph(data)
        # check_edges(buildings_graph[building])
        # show_graph(buildings_graph[building])
        # find_path(buildings_graph[building])
    return buildings_graph


if __name__ == "__main__":
    main()

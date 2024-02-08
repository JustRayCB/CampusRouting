"""
:Author: Rayan Contuliano Bravo
:Date: 07/02/2024
:Decription: This module contains the implementation of the Dijkstra algorithm to find the 
            shortest path between two nodes in a building graph.
"""

from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx
from pqdict import pqdict


def take_stairs(graph: nx.DiGraph, predecessor: str, from_node: str, to_node: str) -> bool:
    return graph.nodes[predecessor]["floor"] != graph.nodes[to_node]["floor"]


def analyse_path(graph: nx.DiGraph, path: List[str]):
    """Transform a path into a sequence of instructions.

    :param graph: Building graph.
    :param path: The path to analyse. A path is a list of nodes.
    """
    """
    Intructions Possibles:
        - Montez les escaliers jurqu'à l'étage <floor>
        - Descendez les escaliers jusqu'à l'étage <floor>
        - Prenez l'ascenseur jusqu'à l'étage <floor>
        - Allez tout droit jusqu'au bout du couloir
        - Tournez à droite 
        - Tournez à gauche
        - La salle <room> est à votre droite
        - La salle <room> est à votre gauche
        - Vous êtes arrivé à la salle <room>
        - TODO: Ajouter d'autres instuctions
    """
    pair_rooms = [[path[i], path[i + 1]] for i in range(len(path) - 1)]
    predecessor = "null"
    for pair in pair_rooms:
        # print(f"From {pair[0]} to {pair[1]}")
        direction = graph.edges[pair[0], pair[1]]["direction"]
        d = direction if type(direction) == str else direction[predecessor]
        if predecessor == "null":
            pass
        elif take_stairs(graph, predecessor, pair[0], pair[1]) and predecessor != "null":
            print(f"From {predecessor} to {pair[1]}: go to the stairs :{pair[0]}")
        print(f"From {pair[0]} to {pair[1]}: go  {d}")
        predecessor = pair[0]


def recover_path(predecessors, source, target):
    """
    Recover the path from the source to the target node.

    :param predecessors: The list of the choosen predecessor of each node.
    :param source: The source node.
    :param target: The target node.
    :return: The path between the source and the target node.
    """
    path = [target]
    while target != source:
        target = predecessors[target]
        path.append(target)
    path.reverse()
    return path


def dijkstra(graph: nx.DiGraph, source: str, target: str):
    """
    Implement the Dijkstra algorithm for finding the shortest path.

    between two nodes in a graph using the library NetworkX.
    :param graph: The graph in which the shortest path will be found.
    :param source: The source node's id.
    :param target: The target node's id.
    :return: The shortest path between the source and the target node.
    """

    dist_to: Dict = {node: float("inf") for node in graph.nodes}
    predecessor: Dict = {}
    dist_to[source] = 0
    pq = pqdict()  # It use a min heap to store the nodes and their distances to the source node.
    pq.additem(source, 0)

    for node, distance in pq.popitems():
        if node == target:
            break  # We stop the algorithm when we reach the target node.
        for neighbor in graph.neighbors(node):
            new_distance_neighbor = dist_to[node] + graph.edges[node, neighbor]["weight"]
            if dist_to[neighbor] > new_distance_neighbor:
                dist_to[neighbor] = new_distance_neighbor
                predecessor[neighbor] = node
                (
                    pq.updateitem(neighbor, new_distance_neighbor)
                    if neighbor in pq
                    else pq.additem(neighbor, new_distance_neighbor)
                )
    return dist_to[target], recover_path(predecessor, source, target)


def show_path(graph: nx.DiGraph, path):
    """
    Show the graph with its nodes and edges. The path will be highlighted.

    :param graph: The graph to show.
    :param path: The path to highlight.
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
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
        edge_color="red",
        width=2,
    )
    plt.show()

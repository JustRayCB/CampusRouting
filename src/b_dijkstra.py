"""
:Author: Rayan Contuliano Bravo
:Date: 07/02/2024
:Decription: This module contains the implementation of the Dijkstra algorithm to find the 
            shortest path between two nodes in a building graph.
"""

import networkx as nx
from pqdict import pqdict


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

    dist_to = {node: float("inf") for node in graph.nodes}
    predecessor = {}
    dist_to[source] = 0
    pq = pqdict()  # It use a min heap to store the nodes and their distances to the source node.
    pq.additem(source, 0)
    # We insert all the nodes in the priority queue.
    # for node in graph.nodes:
    #     priority = 0 if node == source else float("inf")
    #     pq.additem(node, priority)

    for node, distance in pq.popitem():
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

"""
:Author: Rayan Contuliano Bravo
:Date: 08/02/2024
:Decription: This module contains the implementation of the Dijkstra algorithm to find the 
shortest path between two nodes in a building graph.
"""

from typing import Dict, List

from pqdict import pqdict

from Graph import Graph
from Graph.graph import GraphTypes


class Dijkstra:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def nodesNotNull(self, source: str, target: str):
        """Check if the nodes are not null

        :param source: source node
        :param target: target node
        :raises ValueError: If the source or the target node is null.
        """
        if "" in [source, target]:
            raise ValueError(
                f"The source and the target nodes must be specified. src: {source}, trg: {target}"
            )

    def existingNodes(self, source: str, target: str) -> List:
        """Check if the nodes are in the graph.

        :param source: The source node.
        :param target: The target node.
        :raises ValueError: If the node is not in the graph.
        :return: The source and the target node.
        """
        my_nodes: List = [source, target]
        for idx in range(len(my_nodes)):
            if not self.graph.is_in_graph(my_nodes[idx]):
                if self.graph.type == GraphTypes.OUTSIDE:
                    raise ValueError(
                        f"The node {my_nodes[idx]} is not in the outside graph {self.graph.name}"
                    )
                # If the node is not in the graph, we find it by the name.
                my_nodes[idx] = self.graph.find_node(my_nodes[idx])
        return my_nodes

    def dijkstra(self, source: str, target: str):
        """Implement the Dijkstra algorithm for finding the shortest path.
        between two nodes in a graph using the library NetworkX.

        :param source: The source node's id.
        :param target: The target node's id.
        :return: The shortest path between the source and the target node.
        """
        self.nodesNotNull(source, target)
        source, target = self.existingNodes(source, target)
        dist_to: Dict = {node: float("inf") for node in self.graph.nodes}
        predecessor: Dict = {}
        dist_to[source] = 0
        pq = pqdict()  # It use a min heap to store the nodes and their distances to the source node.
        pq.additem(source, 0)

        for idx, _ in pq.popitems():
            if idx == target:
                break  # We stop the algorithm when we reach the target node.
            for neighbor in self.graph.neighbors(idx):
                new_distance_neighbor = dist_to[idx] + self.graph.edges[idx, neighbor]["weight"]
                if dist_to[neighbor] > new_distance_neighbor:
                    dist_to[neighbor] = new_distance_neighbor
                    predecessor[neighbor] = idx
                    (
                        pq.updateitem(neighbor, new_distance_neighbor)
                        if neighbor in pq
                        else pq.additem(neighbor, new_distance_neighbor)
                    )
        if dist_to[target] == float("inf"):
            return (float("inf"), [])
        return (dist_to[target], self.recover_path(predecessor, source, target))

    def recover_path(self, predecessors, source, target):
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
        return path[::-1]

    def show_shortest_path(self, source, target):
        _, path = self.dijkstra(source, target)
        self.graph.show_path(path)

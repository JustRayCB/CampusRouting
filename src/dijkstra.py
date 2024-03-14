"""
:Author: Rayan Contuliano Bravo
:Date: 08/02/2024
:Decription: This module contains the implementation of the Dijkstra algorithm to find the 
shortest path between two nodes in a building graph.
"""

from typing import Dict

from pqdict import pqdict

from Graph import Graph


class Dijkstra:
    def __init__(self, graph: Graph, source: str = "", target: str = "") -> None:
        self.graph = graph
        self.path = [] if "" in [source, target] else self.dijkstra(source, target)[1]

    def dijkstra(self, source: str, target: str):
        """Implement the Dijkstra algorithm for finding the shortest path.
        between two nodes in a graph using the library NetworkX.

        :param source: The source node's id.
        :param target: The target node's id.
        :return: The shortest path between the source and the target node.
        """
        if "" in [source, target]:
            raise ValueError(
                f"The source and the target nodes must be specified. src: {source}, trg: {target}"
            )
        if not self.graph.is_in_graph(source):
            # If the source node is not in the graph, we find it by the name.
            if self.graph.name == "solbosch_map_updated":
                raise ValueError(f"The node {source} is not in the graph {self.graph.name}")
            tmp = source
            source = self.graph.find_node(source)
            assert source != tmp, f"The node {target} is not in the graph {self.graph.name}"
        if not self.graph.is_in_graph(target):
            # If the target node is not in the graph, we find it by the name.
            if self.graph.name == "solbosch_map_updated":
                raise ValueError(f"The node {target} is not in the graph {self.graph.name}")
            tmp = target
            target = self.graph.find_node(target)
            assert target != tmp, f"The node {target} is not in the graph {self.graph.name}"
        dist_to: Dict = {node: float("inf") for node in self.graph.nodes}
        predecessor: Dict = {}
        dist_to[source] = 0
        pq = pqdict()  # It use a min heap to store the nodes and their distances to the source node.
        pq.additem(source, 0)
        found = False

        for node, _ in pq.popitems():
            if node == target:
                found = True
                break  # We stop the algorithm when we reach the target node.
            for neighbor in self.graph.neighbors(node):
                new_distance_neighbor = dist_to[node] + self.graph.edges[node, neighbor]["weight"]
                if dist_to[neighbor] > new_distance_neighbor:
                    dist_to[neighbor] = new_distance_neighbor
                    predecessor[neighbor] = node
                    (
                        pq.updateitem(neighbor, new_distance_neighbor)
                        if neighbor in pq
                        else pq.additem(neighbor, new_distance_neighbor)
                    )
        return (
            (dist_to[target], self.recover_path(predecessor, source, target))
            if found
            else (float("inf"), [])
        )

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
        path.reverse()
        self.path = path
        return path

    def show_shortest_path(self):
        assert self.path != [], "The path has not been calculated yet."
        self.graph.show_path(self.path)

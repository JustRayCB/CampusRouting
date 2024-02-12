"""Graph class 

:Autor: Rayan Contuliano Bravo
:Date: 02/12/2024
:Description: This class is used to easily represent a graph.
"""

# import json
from abc import abstractmethod
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx


class NodeAttributes:
    """Attributes of a node."""

    NAME = "name"
    COLOR = "color"
    TYPE = "type"


class EdgeAttributes:
    """Attributes of an edge."""

    WEIGHT = "weight"


class Graph(nx.DiGraph):
    def init(self, path=None):
        super(Graph, self).__init__()
        self.COLORS: Dict[str, str] = {}
        self.PREFIXES: Dict[str, str] = {}
        # self.n_floors = -1
        self.load_graph(path) if path else None

    def get_type_from_id(self, id: str) -> str:
        """Get the type of a node from its id.

        :param id: The id of the node.
        :returns: The type of the node.
        """
        for prefix, room_type in self.PREFIXES.items():
            if id.startswith(prefix):
                return room_type
        raise ValueError(f"Invalid id: {id} for node in", self.__class__.__name__)

    def get_color_from_type(self, node_type: str) -> str:
        """Get the color of a node from its type.

        :param node_type: The type of the node.
        :returns: The color of the node.
        """
        return self.COLORS[node_type]

    @abstractmethod
    def get_graph_name(self, path: str) -> str:
        raise NotImplementedError("This method should be implemented in ", self.__class__.__name__)

    @abstractmethod
    def load_graph(self, path: str) -> None:
        """Load a graph data from a json file or similar.

        :param path: Path of the file containing the graph data.
        :raises NotImplementedError: This method should be implemented in the subclass.
        """
        raise NotImplementedError("This method should be implemented in ", self.__class__.__name__)

    @abstractmethod
    def add_node_(self, node_data: dict) -> None:
        """Setup a node with its attributes and edges (attributes included) in the graph.

        :param node_data: The data of the node taken from the json file.
        :raises NotImplementedError: This method should be implemented in the subclass.
        """
        raise NotImplementedError("This method should be implemented in ", self.__class__.__name__)

    @abstractmethod
    def add_neighbors(self, neighbors: Dict, source: str) -> None:
        """Setup edges with its attributes in the graph according to the neighbors of the source node.

        :param neighbors: The neighbors of the source node.
        :param source: The source node.
        :raises NotImplementedError: This method should be implemented in the subclass.
        """
        raise NotImplementedError("This method should be implemented in", self.__class__.__name__)

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

    def show_path(self, path: List[str]) -> None:
        """Show the path on the graph.

        :param path: Sequence of nodes id that represent the path.
        """
        pos = self.show_graph(False)
        nx.draw_networkx_edges(
            self,
            pos,
            edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
            edge_color="red",
            width=2,
        )
        plt.show()

    def default_dijkstra(self, source: str, target: str) -> List:
        return nx.shortest_path(self, source, target, weight=EdgeAttributes.WEIGHT)

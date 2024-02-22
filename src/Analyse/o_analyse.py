"""Class to analyse the path of in the graph.

:Author: Rayan Contuliano Bravo.
:Date: 02/13/2024
:Description: This class is used to analyse the path of the graph by traducting it into coordinates.
"""

from Graph import OutsideGraph


class OAnalysePath:
    """Class to analyse the path of in the outside graph."""

    def __init__(self, graph: OutsideGraph, path: list = []):
        """Constructor of the class."""
        self.graph: OutsideGraph = graph
        self.path = path
        self.instructions = []

    def set_path(self, path):
        """Set the path to analyse."""
        self.path = path

    def get_instructions(self):
        """Get the instructions."""
        return self.instructions

    def analyse(self):
        long = [self.graph.nodes[i]["longitude"] for i in self.path]
        lat = [self.graph.nodes[i]["latitude"] for i in self.path]
        return list(zip(lat, long))

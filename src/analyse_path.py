"""Class to analyse the path of in the graph.

:Author: Rayan Contuliano Bravo.
:Date: 08/02/2024
:Description: This class is used to analyse the path of the graph by traducting it into instructions.
Instructions can be traducted into images.
"""

from graph import BuildingGraph


class AnalysePath:
    """Class to analyse the path of in the graph."""

    def __init__(self, graph: BuildingGraph, path: list = []):
        """Constructor of the class."""
        self.graph: BuildingGraph = graph
        self.path = path
        self.instructions = []

    def set_path(self, path):
        """Set the path to analyse."""
        self.path = path

    def analyse(self):
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
        pair_rooms = [[self.path[i], self.path[i + 1]] for i in range(len(self.path) - 1)]
        predecessor = "null"
        for pair in pair_rooms:
            direction = self.graph.edges[pair[0], pair[1]]["direction"]
            d = direction if type(direction) == str else direction[predecessor]
            if predecessor == "null":
                pass
            elif self.take_stairs(predecessor, pair[0], pair[1]) and predecessor != "null":
                print(f"From {predecessor} to {pair[1]}: go to the stairs :{pair[0]}")
            print(f"From {pair[0]} to {pair[1]}: by {d}")
            predecessor = pair[0]

    def take_stairs(self, predecessor: str, from_node: str, to_node: str) -> bool:
        ret = self.graph.nodes[predecessor]["floor"] != self.graph.nodes[to_node]["floor"]
        assert self.graph.is_elevator_or_stair(from_node) if ret else True
        return ret

    def get_instructions(self):
        """Get the instructions."""
        return self.instructions

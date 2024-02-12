"""Class to analyse the path of in the graph.

:Author: Rayan Contuliano Bravo.
:Date: 08/02/2024
:Description: This class is used to analyse the path of the graph by traducting it into instructions.
Instructions can be traducted into images.
"""

from typing import Tuple

from b_graph import BuildingGraph


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
        for from_node, to_node in pair_rooms:
            direction = self.graph.edges[from_node, to_node]["direction"]
            d = direction if type(direction) == str else direction[predecessor]
            take_stairs, up = (
                self.take_stairs(predecessor, from_node, to_node)
                if predecessor != "null"
                else (False, False)
            )
            if take_stairs:
                assert predecessor != "null"
                type_ = self.graph.get_type_from_id(from_node)
                go_up = "Montez les escaliers" if type_ == "stair" else "Prenez l'ascenseur"
                go_down = "Descendez les escaliers" if type_ == "stair" else "Prenez l'ascenseur"
                if up:
                    self.instructions.append(
                        f"{go_up} jusqu'à l'étage {self.graph.nodes[to_node]['floor']}"
                    )
                else:
                    self.instructions.append(
                        f"{go_down} jusqu'à l'étage {self.graph.nodes[to_node]['floor']}"
                    )
            elif d == "straight":
                self.instructions.append("Allez tout droit")
            else:
                # d is left or right
                assert d in ["left", "right"]
                direction = "droite" if d == "right" else "gauche"
                if [from_node, to_node] == pair_rooms[-1]:
                    self.instructions.append(f"La salle {to_node} est sur votre {direction}")
                    self.instructions.append(f"Vous êtes arrivé à la salle {to_node}")
                else:
                    self.instructions.append(f"Tournez à {direction}")

            predecessor = from_node
        print(self.instructions)

    def take_stairs(self, predecessor: str, from_node: str, to_node: str) -> Tuple[bool, bool]:
        ret = self.graph.nodes[predecessor]["floor"] != self.graph.nodes[to_node]["floor"]
        assert self.graph.is_elevator_or_stair(from_node) if ret else True
        if ret:
            return ret, int(self.graph.nodes[predecessor]["floor"]) < int(
                self.graph.nodes[to_node]["floor"]
            )
        return ret, False

    def get_instructions(self):
        """Get the instructions."""
        return self.instructions

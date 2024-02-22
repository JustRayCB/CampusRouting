"""Class to analyse the path of in the graph.

:Author: Rayan Contuliano Bravo.
:Date: 08/02/2024
:Description: This class is used to analyse the path of the graph by traducting it into instructions.
Instructions can be traducted into images.
"""

from typing import Tuple

from Graph import BuildingGraph


class Instruction:
    """Class to represent an instruction."""

    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2
    STAIRS = 3
    ELEVATOR = 4
    ARRIVED = 5


class BAnalysePath:
    """Class to analyse the path of in the graph."""

    def __init__(self, graph: BuildingGraph, path: list = []):
        """Constructor of the class."""
        self.graph: BuildingGraph = graph
        self.path = path
        self.images_dir = "data/images/instructions3D/"
        self.images_extension = ".png"
        self.text_instructions = [
            "Allez tout droit",
            "Tournez à gauche",
            "Tournez à droite",
            ["Montez les escaliers jusqu'à l'étage", "Descendez les escaliers jusqu'à l'étage"],
            ["Prenez l'ascenseur jusqu'à l'étage", "Prenez l'ascenseur jusqu'à l'étage"],
            "Vous êtes arrivé à la salle",
        ]
        self.images_instructions = [
            "go_straight",
            "go_left",
            "go_right",
            "take_stairs",
            "take_lift",
            "arrived",
        ]
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
            instruction: Tuple[str, str]  # (Instruction, image)
            take_stairs, up = (
                self.take_stairs(predecessor, from_node, to_node)
                if predecessor
                != "null"  # if there is no predecessor, we cant take stairs or elevator cause  we dont know where we are
                else (False, False)
            )
            if take_stairs:
                assert predecessor != "null"
                type_ = self.graph.get_type_from_id(from_node)
                tmp = (
                    self.text_instructions[Instruction.STAIRS]
                    if type_ == "stair"
                    else self.text_instructions[Instruction.ELEVATOR]
                )  # Base of take stairs or elevator
                if up:
                    tmp = f"{tmp[0]} {self.graph.nodes[to_node]['floor']}"
                else:
                    tmp = f"{tmp[1]} {self.graph.nodes[to_node]['floor']}"
                instruction = (tmp, self.images_instructions[Instruction.STAIRS])
            elif d == "straight":
                instruction = (
                    self.text_instructions[Instruction.STRAIGHT],
                    self.images_instructions[Instruction.STRAIGHT],
                )
            else:
                # d is left or right
                assert d in ["left", "right"]
                direction = "droite" if d == "right" else "gauche"
                if [from_node, to_node] == pair_rooms[-1]:
                    instruction = (
                        f"La salle {to_node} est sur votre {direction}",
                        self.images_instructions[Instruction.ARRIVED],
                    )
                else:
                    direction, image = (
                        (
                            self.text_instructions[Instruction.RIGHT],
                            self.images_instructions[Instruction.RIGHT],
                        )
                        if d == "right"
                        else (
                            self.text_instructions[Instruction.LEFT],
                            self.images_instructions[Instruction.LEFT],
                        )
                    )
                    instruction = (direction, image)
            instruction = (
                instruction[0],
                f"{self.images_dir}{instruction[1]}{self.images_extension}",
            )
            self.instructions.append(instruction)
            predecessor = from_node
        return self.instructions

    def take_stairs(self, predecessor: str, from_node: str, to_node: str) -> Tuple[bool, bool]:
        """Check if the path goes through stairs or elevator.

        :param predecessor: Node before from_node.
        :param from_node: Actual node we are in.
        :param to_node: Node we want to go to.
        :return: A tuple with two elements. The first one is a boolean that indicates if we have to take stairs or elevator. The second one is a boolean that indicates if we have to go up or down.
        """
        ret = self.graph.nodes[predecessor]["floor"] != self.graph.nodes[to_node]["floor"]
        if ret:
            assert self.graph.is_elevator_or_stair(
                from_node
            ), f"{from_node} is not a stair or elevator"
            return ret, int(self.graph.nodes[predecessor]["floor"]) < int(
                self.graph.nodes[to_node]["floor"]
            )
        return ret, False

    def get_instructions(self):
        """Get the instructions."""
        return [i[0] for i in self.instructions]

    def get_images(self):
        """Get the images of the instructions."""
        return [i[1] for i in self.instructions]

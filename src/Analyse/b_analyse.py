from typing import List, Tuple

from Graph import BEdgeAttributes, BNodeAttributes, BuildingGraph


class Instruction:
    """Class to represent an instruction."""

    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2
    STAIRS = 3
    ELEVATOR = 4
    ARRIVED = 5


class BPathAnalyzer:
    """Class to analyse the path of in the graph."""

    def __init__(self, graph: BuildingGraph, path: list = []):
        """Constructor of the class."""
        self.graph: BuildingGraph = graph
        self.path = path
        self.IMAGES_DIR = "data/images/instructions3D/"
        self.IMAGES_EXT = ".png"
        self.text_instructions = {
            Instruction.STRAIGHT: "Allez tout droit",
            Instruction.LEFT: "Tournez à gauche",
            Instruction.RIGHT: "Tournez à droite",
            Instruction.STAIRS: [
                "Descendez les escaliers jusqu'à l'étage",
                "Montez les escaliers jusqu'à l'étage",
            ],
            Instruction.ELEVATOR: [
                "Prenez l'ascenseur jusqu'à l'étage",
                "Prenez l'ascenseur jusqu'à l'étage",
            ],
            Instruction.ARRIVED: "Vous êtes arrivé à la salle",
        }
        self.images_instructions = {
            Instruction.STRAIGHT: "go_straight",
            Instruction.LEFT: "go_left",
            Instruction.RIGHT: "go_right",
            Instruction.STAIRS: "take_stairs",
            Instruction.ELEVATOR: "take_lift",
            Instruction.ARRIVED: "arrived",
        }
        self.instructions = []
        if path:
            self.analyse()

    def set_path(self, path):
        """Set the path to analyse."""
        assert path, "The path must not be empty"
        self.path = path
        self.analyse()

    def analyse(self):
        """Transform a path into a sequence of instructions.

        :param graph: Building graph.
        :param path: The path to analyse. A path is a list of nodes.
        """
        pairs: List = [[self.path[i], self.path[i + 1]] for i in range(len(self.path) - 1)]
        print(self.path)
        predecessor = "null"
        for src, trg in pairs:
            direction = self.graph.edges[src, trg][BEdgeAttributes.DIRECTION]
            # If the direction is not a string it means that it has predecessors
            if type(direction) == dict:
                direction = direction[predecessor]
            instruction: Tuple[str, str]  # (Instruction, image)
            changed_floor, up = self.has_floor_changed(predecessor, src, trg)
            if changed_floor:  # user take elevator or stairs
                instruction_type = (
                    Instruction.STAIRS
                    if self.graph.get_type_from_id(src) == "stair"
                    else Instruction.ELEVATOR
                )
                instruction = self.get_instruction_and_image(
                    instruction_type, up, self.graph.nodes[trg][BNodeAttributes.FLOOR]
                )
            elif direction == "straight":
                instruction = self.get_instruction_and_image(Instruction.STRAIGHT)
            else:
                print("This is the direction", direction)
                assert direction in [
                    "left",
                    "right",
                ], f"The direction {direction} is not left or right"
                instruction_type = Instruction.RIGHT if direction == "right" else Instruction.LEFT
                instruction = self.get_instruction_and_image(instruction_type)

            node_name = self.graph.nodes[trg][BNodeAttributes.NAME]
            if [src, trg] == pairs[-1]:
                instruction = self.get_arrival_instruction(instruction, node_name)
            self.instructions.append(instruction)
            predecessor = src

    def get_arrival_instruction(
        self, instruction: Tuple[str, str], node_name: str
    ) -> Tuple[str, str]:
        """Get the arrival instruction for the last pair of nodes

        :param instruction: Instruction we already have
        :param node_name: Name of the node we are searching for
        :return: The instruction text and the image
        """
        if not instruction[0].startswith("Tournez"):
            text = f"La salle {node_name} est en face de vous"
        else:
            direction = (
                "droite" if instruction[0] == self.text_instructions[Instruction.RIGHT] else "gauche"
            )
            text = f"La salle {node_name} est sur votre {direction}"
        image = f"{self.IMAGES_DIR}{self.images_instructions[Instruction.ARRIVED]}{self.IMAGES_EXT}"
        return text, image

    def get_instruction_and_image(
        self, instruction_type: int, up: bool = False, floor: str = ""
    ) -> Tuple[str, str]:
        """Get the instruction text and image

        :param instruction_type: Type of the instruction (stairs, elevator, right, left, ...)
        :param up: If we go up or down
        :param floor: The floor we reach (only if we go up or down)
        :return: The corresponding instruction and image
        """
        text = self.text_instructions[instruction_type]
        print(f"This is the tedxt {text} for the instruction type {instruction_type}")
        if instruction_type in [Instruction.ELEVATOR, Instruction.STAIRS]:
            text = text[int(up)] + f" {floor}"
        image = f"{self.IMAGES_DIR}{self.images_instructions[instruction_type]}{self.IMAGES_EXT}"
        return text, image

    def has_floor_changed(self, predecessor: str, src: str, trg: str) -> Tuple[bool, bool]:
        """Check if the path goes through stairs or elevator.

        :param predecessor: Node before from_node.
        :param src: Actual node we are in.
        :param trg: Node we want to go to.
        :return: A tuple with two elements. The first one is a boolean that indicates if we have to take stairs or elevator.
            The second one is a boolean that indicates if we have to go up or down.
        """
        # If we are taking the stairs or the elevator, only the src must be one of those types
        # if there is no predecessor, we cant take stairs or elevator cause  we dont know where we go
        if (
            predecessor == "null"
            or self.graph.is_elevator_or_stair(trg)
            or self.graph.is_elevator_or_stair(predecessor)
        ):
            return False, False
        # True if the floors of the nodes are different
        ret = (
            self.graph.nodes[predecessor][BNodeAttributes.FLOOR]
            != self.graph.nodes[trg][BNodeAttributes.FLOOR]
        )
        if ret:
            assert self.graph.is_elevator_or_stair(src), f"{src} is not a stair or elevator"
            return ret, int(self.graph.nodes[predecessor][BNodeAttributes.FLOOR]) < int(
                self.graph.nodes[trg][BNodeAttributes.FLOOR]
            )
        return ret, False

    def get_instructions(self):
        """Get the instructions."""
        return [i[0] for i in self.instructions]

    def get_images(self):
        """Get the images of the instructions."""
        return [i[1] for i in self.instructions]

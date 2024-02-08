"""Main module. Entry point of the application.

:Author: Rayan Contuliano Bravo
:Date: 07/02/2024
:Description: This module is the entry point of the application. It is responsible for starting the application and 
loading the main window.
"""

import b_dijkstra
import json_to_graph


def main():
    """Main function. Entry point of the application."""

    graphs = json_to_graph.main()
    while True:
        # ask_building = input(f"Enter a building name, available buildings are {graphs.keys()}: ")
        ask_building = "P1"
        if ask_building == "exit":
            return
        assert ask_building in graphs, f"Building {ask_building} not found."
        graph = graphs[ask_building]
        while True:
            # ask_start = input(f"Enter a start node, available nodes are {graph.nodes()}: ")
            ask_start = "H1_01"
            if ask_start == "exit":
                return
            assert ask_start in graph.nodes(), f"Node {ask_start} not found."
            while True:
                # ask_end = input(f"Enter an end node, available nodes are {graph.nodes()}: ")
                ask_end = "E214_03"
                if ask_end == "exit":
                    return
                assert ask_end in graph.nodes(), f"Node {ask_end} not found."
                our_path = b_dijkstra.dijkstra(graph, ask_start, ask_end)
                networkx_path = json_to_graph.shortest_path(graph, ask_start, ask_end)
                assert our_path[1] == networkx_path, "The paths are different."
                b_dijkstra.analyse_path(graph, our_path[1])
                b_dijkstra.show_path(graph, our_path[1])
                return


if __name__ == "__main__":
    main()

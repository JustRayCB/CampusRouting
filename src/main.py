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
        if ask_building in graphs:
            graph = graphs[ask_building]
            while True:
                # ask_start = input(f"Enter a start node, available nodes are {graph.nodes()}: ")
                ask_start = "H1_01"
                if ask_start == "exit":
                    return
                if ask_start in graph.nodes():
                    while True:
                        ask_end = input(f"Enter an end node, available nodes are {graph.nodes()}: ")
                        if ask_end == "exit":
                            return
                        if ask_end in graph.nodes():
                            our_path = b_dijkstra.dijkstra(graph, ask_start, ask_end)
                            networkx_path = json_to_graph.shortest_path(graph, ask_start, ask_end)
                            print(f"Our path: {our_path}")
                            print(f"NetworkX path: {networkx_path}")
                            b_dijkstra.show_path(graph, our_path[1])
                        else:
                            print(f"Node {ask_end} is not in the graph.")
                else:
                    print(f"Node {ask_start} is not in the graph.")


if __name__ == "__main__":
    main()

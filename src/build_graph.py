import osmnx as ox
from osmnx import settings as ox_settings
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from haversine import haversine


def save_as_image(graph, filename):
    extension = ".png"
    path = "./data/images/" + filename + extension
    ox.plot_graph(graph, show=False, save=False, close=False, filepath=path)
    plt.savefig(path)


def save_as_osm(graph: nx.Graph, filename: str):
    # pas ouf que 2 lignes dont 1 avec ∞ caractères
    path = "./data/osm/" + filename + ".osm"
    # save graph to disk as .osm xml file
    ox.settings.all_oneway = True
    ox.settings.log_console = True
    # utn = ox_settings.useful_tags_node
    # oxna = ox_settings.osm_xml_node_attrs
    # oxnt = ox_settings.osm_xml_node_tags
    # utw = ox_settings.useful_tags_way
    # oxwa = ox_settings.osm_xml_way_attrs
    # oxwt = ox_settings.osm_xml_way_tags
    # utn = list(set(utn + oxna + oxnt))
    # utw = list(set(utw + oxwa + oxwt))
    # ox_settings.all_oneway = True
    # ox_settings.useful_tags_node = utn
    # ox_settings.useful_tags_way = utw
    ox.save_graph_xml(graph, path)


def save_as_graphml(graph: nx.Graph, filename: str):
    path = "./data/graphml/" + filename + ".graphml"
    ox.save_graphml(graph, path)


city_graph: nx.Graph = ox.graph_from_place("Solbosch University, Brussels, Belgium", network_type='walk', simplify=True)


# Dict that stores the coordinates of each node of the graph
nodes_coords = dict()
for node in city_graph.nodes:
    nodes_coords[node] = {'latitude': city_graph._node[node]['x'], \
                        'longitude':city_graph._node[node]['y']}
    
# given a user's location, we can find the closest node in the graph
# and then use the shortest path algorithm (Dijkstra) to find the shortest path to the destination
position = (4.383221,50.811969) # user's location will be given by the app [PUB]

closest_node = ox.nearest_nodes(city_graph, position[0], position[1], return_dist=False)
for node in nodes_coords:
    print(f"Node: {node}, Latitude: {nodes_coords[node]['latitude']}, Longitude: {nodes_coords[node]['longitude']}")
print(f"User's location: {position} and the closest node is: {closest_node}")
print("-------------------------------------------------------------")


# Or we compute the distance between the user's location and each node of the graph
# and then find the node with the smallest distance 
# credit : https://pypi.org/project/haversine/
closest_node = min(nodes_coords, key=lambda x: haversine(position, (nodes_coords[x]['latitude'], nodes_coords[x]['longitude'])))
print(f"User's location: {position} and the closest node is: {closest_node}")

for node in city_graph.nodes:
    if node == closest_node:
        city_graph.nodes[node]['color'] = 'red'
    else:
        city_graph.nodes[node]['color'] = 'blue'


ox.plot_graph(city_graph, show=True, save=False, close=False, node_color=[city_graph.nodes[node]['color'] for node in city_graph.nodes])

# city_graph: nx.Graph = ox.load_graphml("./data/graphml/bxl_bike.graphml")

# i = 0
# for node in city_graph.nodes:
#     if i == 10:
#         break
#     # city_graph.nodes[node]["x"] pour avoir l'attribut x du noeud node
#     i += 1

# To find the source node in the graph, we could use geopy ? or sanitize the address and find the closest node ?

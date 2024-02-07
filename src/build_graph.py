import osmnx as ox
from osmnx import settings as ox_settings
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib


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

ox.plot_graph(city_graph, show=True, save=False, close=False)

# city_graph: nx.Graph = ox.load_graphml("./data/graphml/bxl_bike.graphml")

# i = 0
# for node in city_graph.nodes:
#     if i == 10:
#         break
#     # city_graph.nodes[node]["x"] pour avoir l'attribut x du noeud node
#     i += 1

# To find the source node in the graph, we could use geopy ? or sanitize the address and find the closest node ?

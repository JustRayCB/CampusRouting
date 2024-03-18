from typing import List, Tuple

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Analyse import BAnalysePath, OAnalysePath
from dijkstra import Dijkstra
from Graph import BuildingGraph, OutsideGraph
from utils.constants import BUILDINGS_DATA_DIR, OUTSIDE_DATA_DIR

BUILDINGS = ["P1", "S"]

app = FastAPI()
origins = [
    "http://localhost:63342",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
graphs = {
    building: BuildingGraph(f"{BUILDINGS_DATA_DIR}{building}/{building}.json")
    for building in BUILDINGS
}
outside_graph = OutsideGraph(f"{OUTSIDE_DATA_DIR}solbosch_map_updated.json")


class PathRequestInside(BaseModel):
    start: str = None
    arrival: str = None


class PathRequestOutside(BaseModel):
    start: tuple = None
    arrival: str = None


class PathRequest(BaseModel):
    start: tuple = (-1, -1)  # Coordinates
    arrival: str = ""  # Room name


class PathRequestFromInside(BaseModel):
    start: str = ""  # Room name
    arrival: str = ""  # Room name


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/available_buildings")
def get_available_buildings():
    return {"buildings": list(graphs.keys())}


def get_building_name(room: str) -> str:
    return room.split(".")[0]


@app.post("/api/ask_from_inside")
def ask_from_inside(request: PathRequestFromInside) -> dict:
    """Compute the path from the user's room to the arrival room.

    :param request: User's data given by the frontend.
    :return: The path if the user wants to go to a room in the same building.
    :return: The path if the user wants to go to a room in another  building.
    """
    starting_room = request.start
    arrival_room = request.arrival
    starting_building = get_building_name(starting_room).upper()
    arrival_building = get_building_name(arrival_room).upper()
    if starting_building == arrival_building:
        # If the user is in the same building, we can use the building graph
        d = Dijkstra(graphs[starting_building])
        a = BAnalysePath(graphs[starting_building], d.dijkstra(starting_room, arrival_room)[1])
        return {
            "same_building": True,
            "path": [],
            "instructions": a.get_instructions(),
            "images": a.get_images(),
        }
    else:
        building_graph = graphs[starting_building]
        arrival_graph = graphs[arrival_building]
        entrances = building_graph.get_entrances()
        paths_to_entrances = []
        for entrance in entrances:
            d = Dijkstra(building_graph)
            paths_to_entrances.append(
                d.dijkstra(starting_room, entrance)
            )  # paths from the starting room to each entrance of starting building
        # best path from each entrances from the starting building to the arrival room
        best_paths = []
        for entrance in entrances:
            lat, long = outside_graph.get_lat_long(entrance)
            all_paths = get_all_paths(arrival_graph, lat, long, arrival_room)
            idx_min = min(range(len(all_paths)), key=lambda i: all_paths[i][0])
            best_paths.append(all_paths[idx_min])
        total_paths = []  # total distance from the user to the room
        for idx in range(len(paths_to_entrances)):
            total_paths.append(
                (
                    paths_to_entrances[idx][0] + best_paths[idx][0],
                    paths_to_entrances[idx][1],
                    best_paths[idx],
                )
            )
        idx_min = min(range(len(total_paths)), key=lambda i: total_paths[i][0])
        # first building path analyse
        fanalyse_in = BAnalysePath(building_graph, total_paths[idx_min][1])
        # analyse outside path
        analyse_out = OAnalysePath(outside_graph, total_paths[idx_min][2][1])
        # second building path analyse
        sanalyse_in = BAnalysePath(arrival_graph, total_paths[idx_min][2][2])
        return {
            "same_building": False,
            "first_instructions": fanalyse_in.get_instructions(),
            "first_building_images": fanalyse_in.get_images(),
            "outside_path": analyse_out.analyse(),
            "final_instructions": sanalyse_in.get_instructions(),
            "final_building_images": sanalyse_in.get_images(),
        }


def get_all_paths(
    building_graph: BuildingGraph, lat: float, long: float, room: str
) -> List[Tuple[float, List, List]]:
    """Compute all the possible path from the user to a room inside a building.

    :param building_graph: The graph of the building where the use wants to go.
    :param lat: Latitude of the user.
    :param long: Longitude of the user.
    :param room: Room the user wants to go to.
    :raises ValueError: If the length of the outside and inside path are not the same which could
        not happen normaly the number of entrances we can reach from the outside
        and the number of entrances we can reach from the inside should be the same.
    :return: a tuple which include the length of the path, the coordinates of the nodes of the outside path and the nodes of the inside path.
    """
    entrances = building_graph.get_entrances()  # exits/entrances
    node = outside_graph.find_closest_node((lat, long))  # find the closest node to the user
    outside_paths: List[Tuple[float, List]] = []
    inside_paths: List[Tuple[float, List]] = []
    for entrance in entrances:  # compute the path from the user to each building entrance
        d = Dijkstra(outside_graph)
        outside_paths.append(d.dijkstra(node, entrance))
    for entrance in entrances:  # compute the path from each entrance to the room
        d = Dijkstra(building_graph)
        inside_paths.append(d.dijkstra(entrance, room))
    total_paths = []
    # Compute the total distance from the user to the room and choose the shortest path
    if len(outside_paths) != len(inside_paths):
        raise ValueError("The number of entrances and inside paths should be the same")
    for idx in range(len(outside_paths)):
        total_paths.append(
            (
                outside_paths[idx][0] + inside_paths[idx][0],
                outside_paths[idx][1],
                inside_paths[idx][1],
            )
        )
    return total_paths


@app.post("/api/ask")
def ask(request: PathRequest) -> dict:
    """Compute the path from the user's location to the arrival room inside a building.

    :param request: User's data given by the frontend.
    :return: The path from the user's location to the arrival room, the instructions and the images when inside the building.
    """
    lat, long = int(request.start[0]), int(request.start[1])
    room = request.arrival  # e.g: P1.2.301
    building = get_building_name(room).upper()  # e.g: P1
    building_graph = graphs[building]
    total_paths = get_all_paths(building_graph, lat, long, room)
    idx_min = min(range(len(total_paths)), key=lambda i: total_paths[i][0])
    analyse_out = OAnalysePath(outside_graph, total_paths[idx_min][1])
    analyse_in = BAnalysePath(building_graph, total_paths[idx_min][2])

    # return : coordinates of each nodes, instruction inside, images
    return {
        "path": analyse_out.analyse(),
        "instructions": analyse_in.get_instructions(),
        "images": analyse_in.get_images(),
    }


@app.post("/api/ask_inside")
def read_item(request: PathRequestInside, re: Request):
    print("L'utilisateur veut aller de", request.start, "à", request.arrival)
    start = request.start
    arrival = request.arrival
    # graph = graphs[start.split("_")[0]]
    graph = graphs["P1"]
    if start not in graph.nodes() or arrival not in graph.nodes():
        return Response(status_code=404)
    d = Dijkstra(graph, start, arrival)
    a = BAnalysePath(graph, d.path)
    a.analyse()
    return {
        "path": d.path,
        "instructions": a.get_instructions(),
        "images": a.get_images(),
    }


@app.post("/api/ask_outside")
def get_path_for_outside(request: PathRequestOutside):
    print("L'utilisateur veut aller de", request.start, "à", request.arrival)
    start = request.start
    arrival = request.arrival
    if start is None or arrival is None:
        return Response(status_code=404)
    n = outside_graph.find_closest_node(start)
    d = Dijkstra(outside_graph, n, arrival)
    print("The path is : ", d.path)
    coordinates = [outside_graph.nodes[node]["position"] for node in d.path]
    return {
        "path": d.path,
        "coordinates": coordinates,
    }

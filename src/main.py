from typing import List, Tuple

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Analyse import BPathAnalyzer, OPathAnalyzer
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


class PathRequest(BaseModel):
    start: tuple = (-1, -1)  # Coordinates
    arrival: str = ""  # Room name


class PathRequestFromInside(BaseModel):
    start: str = ""  # Room name
    arrival: str = ""  # Room name


def get_building_name(room: str) -> str:
    return room.split(".")[0]


def get_all_paths(
    building_graph: BuildingGraph, lat: float, long: float, room: str
) -> List[Tuple[float, List, List]]:
    """Compute all the possible path from the user location to a room inside a building.

    :param building_graph: The graph of the building where the use wants to go.
    :param lat: Latitude of the user.
    :param long: Longitude of the user.
    :param room: Room the user wants to go to.
    :raises AssertionError: If the length of the outside and inside path are not the same which could
        not happen normaly the number of entrances we can reach from the outside
        and the number of entrances we can reach from the inside should be the same.
    :return: a tuple which include the length of the path, the coordinates of the nodes of the outside path and the nodes of the inside path.
    """
    entrances = building_graph.get_entrances()  # exits/entrances
    closest_node = outside_graph.find_closest_node((lat, long))  # find the closest node to the user
    d = Dijkstra(outside_graph)
    # compute the path from the user to each building entrance
    outside_paths: List[Tuple[float, List]] = [
        d.dijkstra(closest_node, entrance) for entrance in entrances
    ]
    d = Dijkstra(building_graph)
    # compute the path from each entrance to the room
    inside_paths: List[Tuple[float, List]] = [d.dijkstra(entrance, room) for entrance in entrances]
    # (total distance, outside path, inside path)
    total_paths = [
        (opath[0] + ipath[0], opath[1], ipath[1])
        for opath, ipath in zip(outside_paths, inside_paths)
    ]
    # Compute the total distance from the user to the room and choose the shortest path
    assert len(outside_paths) == len(
        inside_paths
    ), "The number of entrances and inside paths should be the same"
    return total_paths


def compute_path_inside_same_building(
    starting_room: str, arrival_room: str, building_graph: BuildingGraph
) -> dict:
    """Compute the path from the starting room to the arrival room inside the same building.

    :param starting_room: name of the starting room
    :param arrival_room: name of the arrival room
    :param building_graph: graph of the building
    :return: The path from the starting room to the arrival room, the instructions to get there and the images.
    """
    d = Dijkstra(building_graph)
    path = d.dijkstra(starting_room, arrival_room)[1]
    a = BPathAnalyzer(building_graph, path)
    return {
        "path": [],
        "instructions": a.get_instructions(),
        "images": a.get_images(),
    }


def getShortestPathIdx(paths: List[Tuple[float, List, List]]) -> int:
    """According to the total distance of each path, return the index of the shortest path.

    :param all_paths: List of paths with the total distance, the outside path and the inside path.
    :return: The index of the shortest path.
    """
    return min(range(len(paths)), key=lambda i: paths[i][0])


def compute_path_inside_different_building(
    starting_room: str, arrival_room: str, starting_building: str, arrival_building: str
):
    """Compute the path from the starting room to the arrival room inside different buildings.

    :param starting_room: Name of the starting room.
    :param arrival_room: Name of the arrival room.
    :param starting_building: Name of the starting building.
    :param arrival_building: Name of the arrival building.
    :return: The path to exit the first building , the path to get to the arrival building,
        the path to get to the arrival room and the corresponding instructions and images.
    """
    building_graph = graphs[starting_building]
    arrival_graph = graphs[arrival_building]
    entrances = building_graph.get_entrances()
    d = Dijkstra(building_graph)
    # paths from the starting room to each entrance of starting building
    paths_to_entrances = [d.dijkstra(starting_room, entrance) for entrance in entrances]
    # best path from each entrances from the starting building to the arrival room
    paths_to_rooms = []
    for entrance in entrances:
        lat, long = outside_graph.get_lat_long(entrance)
        all_paths = get_all_paths(arrival_graph, lat, long, arrival_room)
        # Get the index of the shortest path
        idx_min = getShortestPathIdx(all_paths)
        paths_to_rooms.append(all_paths[idx_min])
    # (total distance, path to entrance, path from entrance to arrival room)
    complete_paths = [
        (p1[0] + p2[0], p1[1], p2) for p1, p2 in zip(paths_to_entrances, paths_to_rooms)
    ]
    # Get the index of the shortest path
    idx_min = getShortestPathIdx(complete_paths)
    # first building path analyse
    fanalyse_in = BPathAnalyzer(building_graph, complete_paths[idx_min][1])
    # analyse outside path
    analyse_out = OPathAnalyzer(outside_graph, complete_paths[idx_min][2][1])
    # second building path analyse
    sanalyse_in = BPathAnalyzer(arrival_graph, complete_paths[idx_min][2][2])
    return {
        "first_instructions": fanalyse_in.get_instructions(),
        "first_building_images": fanalyse_in.get_images(),
        "outside_path": analyse_out.analyse(),
        "final_instructions": sanalyse_in.get_instructions(),
        "final_building_images": sanalyse_in.get_images(),
    }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/available_buildings")
def get_available_buildings_endpoint():
    return {"buildings": list(graphs.keys())}


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
        result = compute_path_inside_same_building(
            starting_room, arrival_room, graphs[starting_building]
        )
        return {"same_building": True, **result}
    else:
        result = compute_path_inside_different_building(
            starting_room, arrival_room, starting_building, arrival_building
        )
        return {"same_building": False, **result}


@app.post("/api/ask")
def ask(request: PathRequest) -> dict:
    """Compute the path from the user's location to the arrival room inside a building.

    :param request: User's data given by the frontend.
    :return: The path from the user's location to the arrival room, the instructions and the images when inside the building.
    """
    lat, long = float(request.start[0]), float(request.start[1])
    room = request.arrival  # e.g: P1.2.301
    building = get_building_name(room).upper()  # e.g: P1
    building_graph = graphs[building]
    total_paths = get_all_paths(building_graph, lat, long, room)
    idx_min = getShortestPathIdx(total_paths)
    analyse_out = OPathAnalyzer(outside_graph, total_paths[idx_min][1])
    analyse_in = BPathAnalyzer(building_graph, total_paths[idx_min][2])

    # return : coordinates of each nodes, instruction inside, images
    return {
        "path": analyse_out.analyse(),
        "instructions": analyse_in.get_instructions(),
        "images": analyse_in.get_images(),
    }

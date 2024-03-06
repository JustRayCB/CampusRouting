from typing import List, Tuple

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Analyse import BAnalysePath, OAnalysePath
from dijkstra import Dijkstra
from Graph import BuildingGraph, OutsideGraph
from utils.constants import BUILDINGS_DATA_DIR, OUTSIDE_DATA_DIR

BUILDINGS = ["P1"]

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/available_buildings")
def get_available_buildings():
    return {"buildings": list(graphs.keys())}


def get_building_name(room: str) -> str:
    return room.split(".")[0]


# TODO: Ask from inside


@app.post("/api/ask")
def ask(request: PathRequest):
    lat, long = int(request.start[0]), int(request.start[1])
    room = request.arrival  # e.g: P1.2.301
    building = get_building_name(room).upper()  # e.g: P1
    building_graph = graphs[building]
    entrances = building_graph.get_entrances()  # exits/entrances
    node = outside_graph.find_closest_node((lat, long))  # find the closest node to the user
    outside_paths: List[Tuple[int, List]] = []
    inside_paths: List[Tuple[int, List]] = []
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
    coordonates = [outside_graph.nodes[node]["position"] for node in d.path]
    return {
        "path": d.path,
        "coordonates": coordonates,
    }

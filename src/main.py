from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Analyse import BAnalysePath
from Graph import BuildingGraph, OutsideGraph
from dijkstra import Dijkstra
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/available_buildings")
def get_available_buildings():
    return {"buildings": list(graphs.keys())}


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

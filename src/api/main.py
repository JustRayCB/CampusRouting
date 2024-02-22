from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ..Graph import BuildingGraph
from ..Analyse import BAnalysePath
from ..dijkstra import Dijkstra


DATA_DIR = "../../data/plans/Solbosch/"
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
    building: BuildingGraph(f"{DATA_DIR}{building}/{building}.json") for building in BUILDINGS
}


class PathRequest(BaseModel):
    start: str = None
    arrival: str = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/available_buildings")
def get_available_buildings():
    return {"buildings": list(graphs.keys())}


@app.post("/api/ask")
def read_item(request: PathRequest,  re: Request):
    print("L'utilisateur veut aller de", request.start, "à", request.arrival)
    start = request.start
    arrival = request.arrival
    #graph = graphs[start.split("_")[0]]
    graph = graphs["P1"]
    if start not in graph.nodes() or arrival not in graph.nodes():
        return Response(status_code=404)
    d = Dijkstra(graph, start, arrival)
    a = BAnalysePath(graph, d.path)
    a.analyse()
    return {
        "start": start,
        "arrival": arrival,
        "path": d.path,
        "instructions": a.get_instructions(),
    }

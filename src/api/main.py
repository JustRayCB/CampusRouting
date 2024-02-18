from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from ..b_graph import BuildingGraph
from ..dijkstra import Dijkstra

app = FastAPI()
buildingGraph = BuildingGraph()


class PathRequest(BaseModel):
    start: str = None
    arrival: str = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ask")
def read_item(request: PathRequest,  re: Request):
    print("L'utilisateur veut aller de", request.start, "à", request.arrival)
    start = request.start
    arrival = request.arrival
    d = Dijkstra(buildingGraph, start, arrival)
    data = {
        "start": start,
        "arrival": arrival,
        "path": d.path
    }
    return Response(content=data)

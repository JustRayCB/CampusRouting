from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ..b_graph import BuildingGraph
from ..dijkstra import Dijkstra


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

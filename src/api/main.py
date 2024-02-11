from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PathRequest(BaseModel) :
    start : str = None
    arrival : str = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ask")
def read_item(request : PathRequest):
    print(f"L'utilisateur est à l'endroit suivant : {request.start}\n \
          L'utilisateur veut se rendre à l'endroit suivant : {request.arrival}")
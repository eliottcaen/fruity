import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException


class Fruit(BaseModel):
    name : str

class Fruits(BaseModel):
    fruits:List[Fruit]

class Category(BaseModel):
    name: str

class UpdateFruitRequest(BaseModel):
    old_fruit: Fruit
    new_fruit: Fruit

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

memorydb = {"fruits":[]}

@app.get("/fruits",response_model =Fruits)
def get_fruits():
    return Fruits(fruits=memorydb["fruits"])

@app.post("/fruits",response_model=Fruit)
def add_fruit(fruit:Fruit):
    memorydb["fruits"].append(fruit)
    return fruit

@app.put("/fruits",response_model=Fruit)
def update_fruit(update_request: UpdateFruitRequest):
    for i, fruit in enumerate(memorydb["fruits"]):
        if fruit.name == update_request.old_fruit.name:
            memorydb["fruits"][i] = update_request.new_fruit
            return update_request.new_fruit
    raise HTTPException(status_code=404, detail="Fruit not found")

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
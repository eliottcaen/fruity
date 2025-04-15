from fastapi import APIRouter
from config.database import collection_name
from models.fruits_model import Fruit, FruitOut, UpdateFruitRequest
from schemas.fruits_schemas import fruit_helper, fruits_helper
from bson import ObjectId

fruit_api_router = APIRouter()

@fruit_api_router.get("/")
async def get_fruits():
    fruits = fruits_helper(collection_name.find())
    return {"status":"ok","data":fruits}

@fruit_api_router.post("/")
async def add_fruit(fruit:Fruit):
    fruit_dict = fruit.dict()
    result = collection_name.insert_one(fruit_dict)
    return {
        "status": "ok",
        "id": str(result.inserted_id)
    }

@fruit_api_router.put("/")
async def update_fruit(update_request: UpdateFruitRequest):
    collection_name.update_one(
            {"_id":ObjectId(update_request.id)},
            {"$set": {
                "name":update_request.new_name}})
    return update_request.new_name

@fruit_api_router.delete("/{id}")
async def delete_fruit(id: str):
    fruit = fruit_helper(collection_name.find_one({"_id":ObjectId(id)}))
    collection_name.delete_one(
            {"_id":ObjectId(id)})
    return fruit["name"]

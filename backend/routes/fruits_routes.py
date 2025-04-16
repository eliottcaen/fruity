from fastapi import APIRouter, HTTPException
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
    if fruit.dict()["name"] == "":
        raise HTTPException(status_code=400, detail="Fruit name is required")

    try:
        result = collection_name.insert_one(fruit.dict())
        return {
            "status": "ok",
            "id": str(result.inserted_id),
            "name": fruit.dict()["name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while inserting the fruit: {str(e)}")


@fruit_api_router.put("/")
async def update_fruit(update_request: UpdateFruitRequest):
    if not update_request.id:
        raise HTTPException(status_code=400, detail="Fruit id is required")

    if not update_request.new_name:
        raise HTTPException(status_code=400, detail="Fruit name is required")

    try:
        collection_name.update_one(
                {"_id":ObjectId(update_request.id)},
                {"$set": {
                    "name":update_request.new_name}})
        return update_request.new_name

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the fruit: {str(e)}")


@fruit_api_router.delete("/{id}")
async def delete_fruit(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="Fruit id is required")

    try:
        fruit = fruit_helper(collection_name.find_one({"_id":ObjectId(id)}))
        collection_name.delete_one(
                {"_id":ObjectId(id)})
        return fruit["name"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the fruit: {str(e)}")
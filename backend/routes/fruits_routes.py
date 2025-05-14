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
            "name": fruit.dict()["name"],
            "price": fruit.dict()["price"],
            "supermarket": fruit.dict()["supermarket"]
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


@fruit_api_router.patch("/")
async def update_fruit(update_request: UpdateFruitRequest):
    # Build the update dictionary with non-null fields
    update_data = {}
    fruit_id = update_request.id

    if update_request.new_name:
        update_data["name"] = update_request.new_name
    if update_request.new_price:
        update_data["price"] = update_request.new_price
    if update_request.new_supermarket:
        update_data["supermarket"] = update_request.new_supermarket

    # If no fields were provided to update, raise an error
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # Perform the update operation on MongoDB
    result = collection_name.update_one(
        {"_id": ObjectId(fruit_id)},  # Find the fruit by its ObjectId
        {"$set": update_data}  # Update only the provided fields
    )

    # If no matching document is found
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Fruit not found")

    # Fetch the updated fruit from the database
    updated_fruit = collection_name.find_one({"_id": ObjectId(fruit_id)})

    # Return the updated fruit using the FruitOut model
    return {
        "status": "ok",
        "data": FruitOut(
            id=str(updated_fruit["_id"]),
            name=updated_fruit["name"],
            price=updated_fruit["price"],
            supermarket=updated_fruit["supermarket"]
        )
    }

@fruit_api_router.delete("/{id}")
async def delete_fruit(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="Fruit id is required")

    try:
        fruit = fruit_helper(collection_name.find_one({"_id": ObjectId(id)}))
        collection_name.delete_one({"_id": ObjectId(id)})
        return {
            "status": "ok",
            "deleted": fruit["name"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the fruit: {str(e)}")
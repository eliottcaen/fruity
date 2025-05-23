from fastapi import APIRouter, HTTPException
from config.database import products_collection, queries_collection
from models.product_model import Product, ProductOut, UpdateProductRequest
from schemas.product_schemas import product_from_db, products_from_db
from bson import ObjectId

product_api_router = APIRouter()

@product_api_router.get("/")
async def get_products():
    products = products_from_db(products_collection.find())
    return {"status": "ok", "data": products}


from fastapi import HTTPException


@product_api_router.get("/product")
async def get_products(tags: str, supermarket: str):
    products_cursor = products_collection.find({
        "tags": tags,  # matches if tag is in the list
        "supermarket": supermarket
    })
    products = products_from_db(products_cursor)

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    return {"status": "ok", "data": products}


@product_api_router.post("/")
async def add_product(product: Product):
    if product.name == "":
        raise HTTPException(status_code=400, detail="Product name is required")

    try:
        result = products_collection.insert_one(product.dict())
        return {
            "status": "ok",
            "id": str(result.inserted_id),
            "name": product.name,
            "price": product.price,
            "supermarket": product.supermarket,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while inserting the product: {str(e)}")


@product_api_router.patch("/")
async def update_product(update_request: UpdateProductRequest):
    update_data = {}
    product_id = update_request.id

    if update_request.new_name:
        update_data["name"] = update_request.new_name
    if update_request.new_price:
        update_data["price"] = update_request.new_price
    if update_request.new_supermarket:
        update_data["supermarket"] = update_request.new_supermarket
    if update_request.new_image_url:
        update_data["image_url"] = update_request.new_image_url
    if update_request.new_product_url:
        update_data["product_url"] = update_request.new_product_url

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = products_collection.find_one({"_id": ObjectId(product_id)})

    return {
        "status": "ok",
        "data": ProductOut(
            id=str(updated_product["_id"]),
            name=updated_product["name"],
            price=updated_product["price"],
            supermarket=updated_product["supermarket"],
            image_url=updated_product.get("image_url"),
            product_url=updated_product.get("product_url")
        )
    }


@product_api_router.delete("/{id}")
async def delete_product(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="Product id is required")

    try:
        product = product_from_db(products_collection.find_one({"_id": ObjectId(id)}))
        products_collection.delete_one({"_id": ObjectId(id)})
        return {
            "status": "ok",
            "deleted": product["name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the product: {str(e)}")

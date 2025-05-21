from fastapi import APIRouter, HTTPException
from services.search_services import fetch_products_from_api, search_and_store_products

search_api_router = APIRouter()

@search_api_router.get("/search")
async def search_products(query: str):
    try:
        result = fetch_products_from_api(query)
        return {"message": "Search complete", "results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@search_api_router.post("/search")
async def search_and_store(query: str):
    products = search_and_store_products(query)
    return {
          "message": "Products fetched and stored",
          "results": products
            }
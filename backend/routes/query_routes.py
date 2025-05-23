from fastapi import APIRouter, HTTPException
from config.database import queries_collection
from models.query_model import Query, QueryOut
from schemas.query_schemas import query_helper, queries_helper
from bson import ObjectId
from datetime import datetime

query_api_router = APIRouter()

@query_api_router.get("/")
async def get_queries():
    queries = queries_helper(queries_collection.find())
    return {"status": "ok", "data": queries}

@query_api_router.post("/")
async def add_query(query: Query):
    query_data = query.dict()
    query_data["timestamp"] = query_data.get("timestamp") or datetime.utcnow()

    try:
        result = queries_collection.insert_one(query_data)
        return {
            "status": "ok",
            "data": {
                "id": str(result.inserted_id),
                "search_term": query_data["search_term"],
                "supermarket": query_data["supermarket"],
                "timestamp": query_data["timestamp"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving query: {str(e)}")

import requests
from typing import List, Dict, Any
from config.database import products_collection, queries_collection
from schemas.product_schemas import product_from_api, product_from_db
from datetime import datetime


def fetch_products_from_api(search_term: str,supermarket:str ) -> Dict[str, Any]:
    """
    Call external API and return raw product results list.
    """
    if supermarket not in ['amazon']:
        raise Exception(f"{supermarket} not in the list [amazon]")

    url = f"https://api-to-find-grocery-prices.p.rapidapi.com/{supermarket}"
    querystring = {"query": search_term, "country": "us", "page": "1"}
    headers = {
        "x-rapidapi-host": "api-to-find-grocery-prices.p.rapidapi.com",
        "x-rapidapi-key": "64bf2b5510mshf45d3c72715ca7ep1fa095jsn7613ffd147d6"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")

    data = response.json()
    try:
        print(response.json())
        return data.get("products", data)
    except (KeyError, TypeError):
        raise ValueError(f"Unexpected API response structure: {data}")


def store_or_update_products(api_products: List[Dict[str, Any]], tag: str, supermarket: str) -> List[Dict[str, Any]]:
    """
    Insert new products or update existing products with new tags in MongoDB.

    Returns formatted products from DB.
    """

    results = []

    for item in api_products:
        name = item.get("name")
        if not name:
            continue

        existing = products_collection.find_one({"name": name})
        product_data = product_from_api(item, supermarket=supermarket, tag=tag)

        if existing:
            if tag not in existing.get("tags", []):
                products_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$addToSet": {"tags": tag}}
                )
            product_doc = products_collection.find_one({"_id": existing["_id"]})
            results.append(product_from_db(product_doc))
        else:
            inserted_id = products_collection.insert_one(product_data).inserted_id
            inserted_doc = products_collection.find_one({"_id": inserted_id})
            results.append(product_from_db(inserted_doc))

    return results

def search_and_store_products(search_term: str, supermarket: str) -> List[Dict[str, Any]]:
    queries_collection.insert_one({
        "search_term": search_term,
        "supermarket": supermarket,
        "timestamp": datetime.utcnow()
    })

    api_products = fetch_products_from_api(search_term, supermarket)
    return store_or_update_products(api_products, supermarket = supermarket, tag=search_term)


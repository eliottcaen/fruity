from typing import Dict, Any

def product_from_db(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a product document retrieved from MongoDB.
    """
    return {
        "id": str(product["_id"]),
        "name": product.get("name", ""),
        "price": product.get("price", None),
        "supermarket": product.get("supermarket", ""),
        "image_url": product.get("image_url", None),
        "product_url": product.get("product_url", None),
        "tags": product.get("tags", []),
    }

def products_from_db(products) -> list:
    """
    Format several products document retrieved from MongoDB.
    """
    return [product_from_db(product) for product in products]

def product_from_api(api_product: Dict[str, Any], supermarket: str, tag: str) -> Dict[str, Any]:
    """
    Build a product dictionary from raw external API data for MongoDB insertion.

    Extracts relevant fields from the API product data, converts price to float,
    and initializes tags with the provided tag.

    Args:
        api_product (dict): Raw product data from external API.
        supermarket (str): The name of the supermarket or source.
        tag (str): Tag to associate with the product (e.g., search query).

    Returns:
        dict: Product dictionary ready to be inserted into MongoDB.
    """
    # Convert price string like "$3.99" to float 3.99, default to None if fails
    try:
        price = float(api_product.get("price", "").replace("$", ""))
    except (ValueError, AttributeError):
        price = None

    return {
        "name": api_product.get("name", ""),
        "supermarket": supermarket,
        "price": price,
        "image_url": api_product.get("image", None),
        "product_url": api_product.get("amazonLink", None),
        "tags": [tag],
    }



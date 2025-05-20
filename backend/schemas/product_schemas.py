def product_helper(product: dict) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product.get("name", ""),
        "price": product.get("price", None),
        "supermarket": product.get("supermarket", ""),
        "image_url": product.get("image_url", None),
        "product_url": product.get("product_url", None),
        "tags": product.get("tags", [])
    }

def products_helper(products) -> list:
    return [product_helper(product) for product in products]

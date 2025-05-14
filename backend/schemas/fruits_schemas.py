def fruit_helper(fruit: dict) -> dict:
    return {
        "id": str(fruit["_id"]),
        "name": fruit.get("name", ""),
        "price": fruit.get("price", None),
        "supermarket": fruit.get("supermarket", "")
    }

def fruits_helper(fruits) -> list:
    return [fruit_helper(fruit) for fruit in fruits]
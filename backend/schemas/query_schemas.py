def query_helper(query: dict) -> dict:
    return {
        "id": str(query["_id"]),
        "search_term": query.get("search_term", ""),
        "timestamp": query.get("timestamp")
    }

def queries_helper(queries) -> list:
    return [query_helper(query) for query in queries]

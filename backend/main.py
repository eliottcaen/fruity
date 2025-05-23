import uvicorn
from fastapi import FastAPI
from routes.product_routes import product_api_router
from config.database import check_mongo_connection
from routes.query_routes import query_api_router
from routes.search_routes import search_api_router



app = FastAPI()
app.include_router(product_api_router, prefix="/products")
app.include_router(query_api_router, prefix="/queries")
app.include_router(search_api_router, prefix="/search")



@app.get("/")
def read_root():
    return {"message": "Welcome to the fruity API 🍍"}

# Vérification de la connexion à la base de données au démarrage
@app.on_event("startup")
async def startup():
    print("L'application démarre. Vérification de la connexion à MongoDB.")
    # Vérification de la connexion ici
    connection_status = check_mongo_connection()
    if connection_status["status"] == "error":
        raise Exception("MongoDB is not accessible at startup")
    print("Connexion MongoDB réussie.")


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
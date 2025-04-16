import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
from routes.fruits_routes import fruit_api_router
from config.database import  check_mongo_connection

app = FastAPI()
app.include_router(fruit_api_router, prefix="/fruits")

#origins = ["http://localhost:5173"]

#app.add_middleware(
 # CORSMiddleware,
  #  allow_origins = origins,
   # allow_credentials=True,
    #allow_methods=["*"],
    #allow_headers=["*"]
#)


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
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
from routes.fruits_routes import fruit_api_router


app = FastAPI()
app.include_router(fruit_api_router, prefix="/fruits")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the fruity API 🍍"}


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
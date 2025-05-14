from pydantic import BaseModel
from typing import Optional


class Fruit(BaseModel):
    """ To load a new fruit
    """
    name : str
    price : float
    supermarket: str

class FruitOut(BaseModel):
    """ To get the fruit name with their id given by mongodb"""
    id: str
    name: str
    price: float
    supermarket: str

class UpdateFruitRequest(BaseModel):
    id: str
    new_name: Optional[str] = None
    new_price: Optional[float] = None
    new_supermarket: Optional[str] = None

from pydantic import BaseModel

class Fruit(BaseModel):
    """ To load a new fruit
    """
    name : str

class FruitOut(BaseModel):
    """ To get the fruit name with their id given by mongodb"""
    id: str
    name: str

class UpdateFruitRequest(BaseModel):
    id: str
    new_name: str

from pydantic import BaseModel
from typing import Optional, List



class Product(BaseModel):
    name: str
    supermarket: str
    price: float
    image_url: str
    product_url: str
    tags: List[str]


class ProductOut(BaseModel):
    """To get the product info with its MongoDB ID"""
    id: str
    name: str
    price: float
    supermarket: str
    image_url: Optional[str] = None
    product_url: Optional[str] = None

class UpdateProductRequest(BaseModel):
    id: str
    new_name: Optional[str] = None
    new_price: Optional[float] = None
    new_supermarket: Optional[str] = None
    new_image_url: Optional[str] = None
    new_product_url: Optional[str] = None

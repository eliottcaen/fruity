from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Query(BaseModel):
    search_term: str
    supermarket: str
    timestamp: Optional[datetime] = None

class QueryOut(BaseModel):
    id: str
    search_term: str
    supermarket: str
    timestamp: Optional[datetime] = None


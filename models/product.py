from pydantic import BaseModel, Field
from typing import List

# -- Request Models --

class Size(BaseModel):
    size: str
    quantity: int

class ProductIn(BaseModel):
    name: str
    price: float
    sizes: List[Size]

# -- Response Models --

class ProductId(BaseModel):
    id: str

class ProductOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    price: float

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            "id": str
        }

class PageInfo(BaseModel):
    next: str | None
    limit: int
    previous: int

class ProductListResponse(BaseModel):
    data: List[ProductOut]
    page: PageInfo
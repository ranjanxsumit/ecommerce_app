from pydantic import BaseModel, Field
from typing import List
from .product import PageInfo

# -- Request Models --

class Item(BaseModel):
    productId: str
    qty: int

class OrderIn(BaseModel):
    userId: str = "user_1"
    items: List[Item]

# -- Response Models --

class OrderId(BaseModel):
    id: str

class ProductDetails(BaseModel):
    id: str
    name: str

class OrderItemDetail(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderOut(BaseModel):
    id: str = Field(..., alias="_id")
    items: List[OrderItemDetail]
    total: float

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            "id": str
        }

class OrderListResponse(BaseModel):
    data: List[OrderOut]
    page: PageInfo
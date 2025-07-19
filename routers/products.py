from fastapi import APIRouter, status, HTTPException
from typing import Optional
from crud import product as product_crud
from models.product import ProductIn, ProductId, ProductListResponse

router = APIRouter()

@router.post("/products", response_model=ProductId, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(product: ProductIn):
    return await product_crud.create_product(product)

@router.get("/products", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def list_products_endpoint(name: Optional[str] = None, size: Optional[str] = None, limit: int = 10, offset: int = 0):
    products = await product_crud.list_products(name, size, limit, offset)
    
    page_info = {
        "limit": len(products),
        "next": str(offset + limit) if len(products) == limit else None,
        "previous": offset - limit 
    }
    
    return {"data": products, "page": page_info}
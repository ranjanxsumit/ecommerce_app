from fastapi import APIRouter, status, HTTPException
from crud import order as order_crud
from models.order import OrderIn, OrderId, OrderListResponse

router = APIRouter()

@router.post("/orders", response_model=OrderId, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(order: OrderIn):
    try:
        return await order_crud.create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/orders/{user_id}", response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_orders_endpoint(user_id: str, limit: int = 10, offset: int = 0):
    orders = await order_crud.list_orders(user_id, limit, offset)
    
    page_info = {
        "limit": len(orders),
        "next": str(offset + limit) if len(orders) == limit else None,
        "previous": offset - limit 
    }
    
    return {"data": orders, "page": page_info}
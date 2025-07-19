from bson import ObjectId
from database import product_collection
from models.product import ProductIn

async def create_product(product: ProductIn):
    product_dict = product.dict()
    result = await product_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

async def list_products(name: str | None, size: str | None, limit: int, offset: int):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size
    
    products_cursor = product_collection.find(query).sort("_id").skip(offset).limit(limit)
    products = await products_cursor.to_list(length=limit)
    
    # Manually handle ObjectId to string conversion for Pydantic model compatibility
    for product in products:
        product["_id"] = str(product["_id"])
        
    return products
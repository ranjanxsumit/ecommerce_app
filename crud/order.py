from bson import ObjectId
from database import order_collection, product_collection
from models.order import OrderIn

async def create_order(order: OrderIn):
    # Convert product IDs from string to ObjectId for database query
    product_ids = [ObjectId(item.productId) for item in order.items]
    
    # Check if all products exist
    product_count = await product_collection.count_documents({"_id": {"$in": product_ids}})
    if product_count != len(product_ids):
        raise ValueError("One or more products not found")

    order_dict = order.dict()
    # Ensure productIds in the database are stored as ObjectIds if needed for lookups
    for item in order_dict["items"]:
        item["productId"] = ObjectId(item["productId"])

    result = await order_collection.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

async def list_orders(user_id: str, limit: int, offset: int):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "product_details"
            }
        },
        {"$unwind": "$product_details"},
        {
            "$group": {
                "_id": "$_id",
                "userId": {"$first": "$userId"},
                "items": {
                    "$push": {
                        "productDetails": {
                            "id": {"$toString": "$product_details._id"},
                            "name": "$product_details.name"
                        },
                        "qty": "$items.qty"
                    }
                },
                "total": {"$sum": {"$multiply": ["$items.qty", "$product_details.price"]}}
            }
        },
        {"$project": {"userId": 0}} # Exclude userId from final output
    ]
    
    orders = await order_collection.aggregate(pipeline).to_list(length=limit)

    for order in orders:
        order["_id"] = str(order["_id"])
            
    return orders
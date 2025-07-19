from bson import ObjectId
from database import order_collection, product_collection

async def list_orders(user_id: str, limit: int, offset: int):
    try:
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
            {
                "$unwind": {
                    "path": "$product_details",
                    "preserveNullAndEmptyArrays": True  # prevents crash if product not found
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "items": {
                        "$push": {
                            "productDetails": {
                                "id": {"$toString": "$product_details._id"},
                                "name": "$product_details.name"
                            },
                            "qty": "$items.qty"
                        }
                    },
                    "total": {
                        "$sum": {
                            "$multiply": [
                                "$items.qty",
                                { "$ifNull": [ "$product_details.price", 0 ] }
                            ]
                        }
                    }
                }
            }
        ]

        orders = await order_collection.aggregate(pipeline).to_list(length=limit)

        # Convert ObjectId to string for each order's id
        for order in orders:
            order["id"] = str(order["_id"])
            del order["_id"]

        return orders

    except Exception as e:
        print(f"❌ Error in list_orders: {e}")
        raise

from bson import ObjectId
from database import order_collection, product_collection
from models.order import OrderIn

async def create_order(order: OrderIn):
    try:
        print("📦 Incoming order:", order.dict())

        product_ids = [ObjectId(item.productId) for item in order.items]
        print("🔍 Converted product IDs:", product_ids)

        product_count = await product_collection.count_documents({"_id": {"$in": product_ids}})
        print("📊 Product count found:", product_count)

        if product_count != len(product_ids):
            raise ValueError("One or more products not found")

        order_dict = order.dict()
        for item in order_dict["items"]:
            item["productId"] = ObjectId(item["productId"])

        result = await order_collection.insert_one(order_dict)
        print("✅ Order inserted:", result.inserted_id)

        return {"id": str(result.inserted_id)}

    except Exception as e:
        print("❌ Error in create_order:", str(e))
        raise

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
                    "preserveNullAndEmptyArrays": True
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
                                {"$ifNull": ["$product_details.price", 0]}
                            ]
                        }
                    }
                }
            }
        ]

        orders = await order_collection.aggregate(pipeline).to_list(length=limit)

        for order in orders:
            order["id"] = str(order["_id"])
            del order["_id"]

        return orders

    except Exception as e:
        print("❌ Error in list_orders:", str(e))
        raise

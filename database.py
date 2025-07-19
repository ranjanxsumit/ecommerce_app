import motor.motor_asyncio
from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
db = client.get_database("ecommerce")
product_collection = db.get_collection("products")
order_collection = db.get_collection("orders")

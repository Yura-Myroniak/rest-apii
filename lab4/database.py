import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://localhost:27017"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "library_db"
)

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]


async def get_database():
    return database
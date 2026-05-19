import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "library_db")

client = MongoClient(MONGO_URL)
db = client[DATABASE_NAME]
books_collection = db["books"]
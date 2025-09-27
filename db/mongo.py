import os
from pymongo import MongoClient

def init_mongo():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URI)
    return client

from pymongo import MongoClient
from core.config import settings

def init_mongo():
    client = MongoClient(settings.MONGO_URI)
    return client
